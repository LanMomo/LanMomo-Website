var config = require('../config/config');
var User = require('../models/user');
var EmailVerification = require('../models/email-verification');
var crypto = require('crypto');

var validateBody = function (body) {
  var emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  var phoneRegex = /^([+]?1[. -]?)?[(]?[0-9]{3}[)]?[. -]?[0-9]{3}[. -]?[0-9]{4}$/i;
  
  return emailRegex.test(body.email) && phoneRegex.test(body.phone)
    && body.username && body.firstname && body.lastname && config.types.indexOf(body.type) >= 0
};

exports.index = function (req, res) {
  res.sendFile('index.html', {root: __dirname + '/../../public/'});
};

exports.getAll = function (req, res) {
  User.find({active:true}).select('username firstname lastname type').exec()
  .then(function (users) {
    res.json(users);
  })
  .reject(function (err) {
    console.log(err);
    res.status(500).json({message:"Une erreur interne est survenue lors de la recherche des participants"});
  });
};

exports.getMax = function (req, res) {
  var type = req.params.type;
  res.json({maxUsers:config.maximum[type]});
};

exports.subscribe = function (req, res) {
  if (validateBody(req.body)) {
    var type = req.body.type;
    User.where({active:true}, {"type":type}).count().exec()
    .then(function (count) {
      if (count >= config.maximum[type]) {
        res.status(402).json({message:"Le nombre maximum de participants sur " + type + " a été atteint."});
      } else {
        req.body.active = false;
        var confirmId = crypto.randomBytes(42).toString('hex');
        User.create(req.body)
        .then(function (user) {
          var data = {
            userId: user._id,
            emailId: confirmId
          };
          EmailVerification.create(data)
          .then(function (emailVerification) {
            var url = config.url.root + '/api/verify/' + emailVerification.emailId;
            var mail = {
              from: config.mailer.from,
              to: req.body.email,
              subject: 'Vérification de courriel',
              html: 'Veuillez confirmer votre courriel en cliquant <a href="' + url + '">ici</a>'
            };
            config.transporter.sendMailAsync(mail)
            .then(function (info) {
              console.log(info);
              res.status(200).json({message:"Veuillez confirmer votre inscription en allant dans votre boîte de réception."});
            })
            .catch(function (err) {
              console.log(err);
              res.status(500).json({message: "Une erreur interne est survenue lors de l'envoi du courriel de validation"});
            });
          })
          .reject(function (err) {
            console.log(err);
            res.status(500).json({message: "Une erreur interne est survenue de la création du courriel de validation"});
          });
        })
        .reject(function (err) {
          console.log(err);
          res.status(500).json({message:"Une erreur est survenue lors de la création d'un participant"});
        });
      }
    })
    .reject(function (err) {
      console.log(err);
      res.status(500).json({message: "Une erreur est survenue lors de la recherche des participants"});
    });
  } else {
    return res.status(400).json({message:'Les informations données sont invalides ou incomplètes'});
  }
};

exports.verify = function (req, res) {
  if (req.params.emailId) {
    EmailVerification.findOne({emailId: req.params.emailId}).exec()
    .then(function (emailVerification) {
      console.log(emailVerification);
      User.update({_id: emailVerification.userId}, {active: true}).exec()
      .then(function () {
        var url = config.url.root + '/congratulations';
        console.log(url);
        res.redirect(url);
      })
      .reject(function (err) {
        console.log(err);
        res.status(500).json({message:'Erreur lors de la modification de l\'utilisateur'});
      });
    })
    .reject(function (err) {
      console.log(err);
      res.status(400).send('Mauvaise url');
    });
  } else {
    res.status(400).send('Mauvais paramètre');
  }
};
