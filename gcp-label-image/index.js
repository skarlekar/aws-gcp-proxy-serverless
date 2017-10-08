'use strict';

// Imports the Google Cloud client library
const Vision = require('@google-cloud/vision');

// Instantiates a client
const vision = Vision();

// The name of the image file to annotate
const myImageUri = 'https://goo.gl/NrGHLW';

// Prepare the request object
const req = {
  source: {
    imageUri: myImageUri
  }
};

exports.detect = (request, response) => {
  var retVal = 'Image Results:';
  var responseStatus = 200;
  //req.source.imageUri = request.param('imageUri', 'https://goo.gl/NrGHLW');
  req.source.imageUri = request.query['imageUri'] || 'https://goo.gl/27gclq';
  console.log("Image request IS: %j", req);
  // Performs label detection on the image file
  vision.labelDetection(req)
    .then((results) => {
      console.log("Image request was: %j", req);
      const labels = results[0].labelAnnotations;
      labels.forEach((label) =>       {
              retVal += ' ' + label.description;
            });
    })
    .catch((err) => {
      responseStatus = 500;
      console.log("Inside Error: Image request was: %j", req);
      console.error('ERROR:', err);
    })
    .then(function (fulfilled){
      console.log("From fulfilled. Retval is: " + retVal);
      response.status(responseStatus).send(retVal);
    });

};

exports.event = (event, callback) => {
  callback();
};
