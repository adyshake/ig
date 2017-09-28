import json
import codecs
import datetime
import os.path
import logging
import argparse
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='login callback and save settings demo')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(client_version))

    device_id = None
    try:

        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print('Unable to find file: {0!s}'.format(settings_file))

            # login new
            api = Client(
                args.username, args.password,
                on_login=lambda x: onlogin_callback(x, args.settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                args.username, args.password,
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username, args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.expires_earliest
    print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    # Call the api
    results = api.direct_v2_inbox()
    unseen_count = results["inbox"]["unseen_count"]

    message_threads = results["inbox"]["threads"]

    #results = api.get_v2_threads()

    margesha_thread = 340282366841710300949128170938113262944
    #results = api._call_api('direct_v2/threads/{0}'.format(margesha_thread))
    
    #with open("marg__full_personal_chat.txt", "w") as f:
    #    f.write(json.dumps(results, indent = 4))

    #----------------
    #personal_thread = results["thread"]
    #other_person_name = personal_thread["users"][0]["username"]
    #other_person_id = personal_thread["users"][0]["pk"]

    # for message in personal_thread["items"]:
    #     if message["user_id"] == other_person_id:
    #         print(other_person_name)
    #     else:
    #         print("Shake!")
    #     if message["item_type"] == "text":
    #         print(message["text"])
    #     elif message["item_type"] == "media":
    #         print("personal media sent")
    #     elif message["item_type"] == "link":
    #         print(message["link"]["text"])
    #     elif message["item_type"] == "placeholder":
    #         print(message["placeholder"]["message"])
    #     elif message["item_type"] == "media_share":
    #         media_type = "Post"
    #         if message["media_share"]["media_type"] == 1:
    #             media_type = "Photo"
    #         #TODO - Verify media type codes 
    #         elif message["media_share"]["media_type"] == 2:
    #             media_type = "Video"

    #         caption = message["media_share"]["caption"]
    #         try:
    #             caption = caption["text"].encode("utf-8")
    #         except:
    #             caption = "null"
    #         print(media_type + " by " + message["media_share"]["user"]["username"])
    #         print("Caption: " + caption)

    #     print("")

    endpoint = 'direct_v2/threads/broadcast/text/'
    params = {
             'text': "yoyo",
             'client_context': api.phone_id,
             'recipient_users ': ' [ [1324264181] ]',
             'action': 'send_item'
         }
    params.update(api.authenticated_params)
    print(params)


    res = api._call_api(endpoint, params=params)


    #if api.auto_patch:
    #    ClientCompatPatch.comment(res['comment'], drop_incompat_keys=api.drop_incompat_keys)
    print(res)


    # for user in message_threads:
    #     print(user["thread_title"] + "\t" + user["thread_id"])
    #     if((user["items"][0]["item_type"]).encode("utf-8") == "text"):
    #         print((user["items"][0]["text"]).encode("utf-8"))
    #     elif((user["items"][0]["item_type"]).encode("utf-8") == "media_share"):
    #         print("Post by " + (user["items"][0]["media_share"]["user"]["username"]))
    #     print("")

    