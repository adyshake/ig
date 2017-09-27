var chalk = require('chalk')
var readlineSync = require('readline-sync')
var resolve = require('path')
var homedir = require('os')
var fs = require('fs-promise')
var Client = require('instagram-private-api').V1;

let file = resolve.resolve(homedir.homedir(), '.ig.json');

function checkFile(file) {
  let fileExists;
  try {
    fileExists = fs.readFileSync(file, 'utf8');
  } catch (err) {}

  if (fileExists) {
    console.log(`${chalk.red('Already login - try `ig logout`')}`);
    process.exit();
  } else {
    fs.writeFile(resolve(homedir(), '.ig.json'), '{}');
  }
}

var device = new Client.Device('ig');
const storage = new Client.CookieFileStorage(file);
const username = readlineSync.question('Enter your username: ');
const password = readlineSync.question('Enter your password: ', {
  hideEchoBack: false
});

Client.Session.create(device, storage, username, password).then(session => {
    session.getAccount().then(function(account) {
      console.log(`${chalk.cyan(`Welcome ${account.params.fullName} !`)}`);
    });
  });