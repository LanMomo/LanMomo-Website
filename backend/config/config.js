var nodemailer = require('nodemailer');
var smtpTransport = require('nodemailer-smtp-transport');
var P = require('bluebird');
var extend = require('extend');

//Public and private config
var config = require('./config.' + process.env.NODE_ENV + '.js');
var pub = require('./config.pub');
extend(config, pub);

//Email tranporter config
var transporter = P.promisifyAll(nodemailer.createTransport(smtpTransport(config.mailer.transportOptions)));
config.transporter = transporter;

//Logger config
switch(process.env.NODE_ENV) {
  case 'dev':
    config.logger.level = 'debug';
    break;
  case 'prod':
    config.logger.level = 'info';
}

module.exports = config;
