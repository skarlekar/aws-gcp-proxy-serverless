# aws-gcp-proxy-serverless

A demonstration of using Serverless Framework to Deploy & Manage Serverless Micro-services
across AWS and Google Cloud Platforms.

Code Repository can be found [here](https://github.com/skarlekar/aws-gcp-proxy-serverless).

# Introduction

This is an simple tutorial to demonstrate how to deploy multiple services on different cloud providers using the Serverless Framework.

More specifically, this tutorial walks you through deploying an image detection service on Google Cloud Platform (GCP) and managing it using a proxy service running on Amazon Web Service. Both the services on either platform is 100% serverless.

The image detection service running on GCP uses  Google's FaaS solution viz., Cloud Functions and the proxy running on AWS uses Amazon's FaaS solution viz., Lambda.

In a typical scenario, you will use a service such as this to detect the contents of an image uploaded to a S3 bucket and take appropriate actions based on the result. For instance, you could use it to blur/reject the image based on the vulgarity or get the image labels and chain it to other services that will translate the labels to multiple languages to cater to your customer needs.

# Setup

## Setup Amazon AWS
1. Sign into your AWS account or [sign-up](https://console.aws.amazon.com/console/home?region=us-east-1) for one.

2. Setup your AWS credentials by following the instructions from [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).

## Install node.js and Serverless framework
Serverless framework is a node.js application. To use Serverless framework and run the tutorial you need to install node.js. Follow the [instructions](https://serverless.com/framework/docs/providers/aws/guide/installation/) from Serverless website to install both node.js and the Serverless framework.

Ensure your Serverless framework is operational using the following:

    $ serverless --version

## Testing your Serverless Setup
Now that you have setup AWS, it is time to test your Serverless setup by creating a mock function using the Serverless framework.

Create a test directory. In the test directory, create a Lambda function from the default template as follows:

    $ mkdir sls-tester
    $ cd sls-tester
    $ sls create --template aws-python --name sls-test

This should create two files in the current directory:

> serverless.yml
>
> handler.py

The *serverless.yml* declares a sample service and a function. The *handler.py*  returns a message stating that your function executed successfully.

To deploy the function, simply type:

    $ sls deploy --verbose

This should deploy the function. The verbose option provides extra information.

To test your function, type:

    $ sls invoke --function hello

If you get the following message, your Serverless setup is working.

    {
        "body": "{\"input\": {}, \"message\": \"Go Serverless v1.0! Your function executed successfully!\"}",
        "statusCode": 200
    }

To check the logs for your function, type:

    $ sls logs -f hello

To keep a continuous check of the logs for your function, type:

    $ sls logs -f hello -t

## Setup Google Cloud

1. Sign up for a new Google account at http://accounts.google.com. If you already have an account you can skip this step.
2. Sign up for a Google Cloud trial at http://console.cloud.google.com/start. If you already have Google Cloud privileges on  your Google account, you can skip this step.
3. Create a new project and call it serverless-project (or a name of your choice).
4. Select *Credentials* in *API & Services* section of the Google Cloud console.
5. Under *Create Credentials*, create a new *Service Account Key*. **Download the JSON key file to a secure place as you will need that in subsequent steps**.
6. In the *API & Services* dashboard, enable *Google Cloud Vision API, Google Cloud Functions API, Google Cloud Deployment Manager API, Google Cloud Storage & Stackdriver Logging*.

# Image Detector

## gcp-label-image

The gcp-label-image is the service that will deployed on GCP. It is a node.js based service that takes an image url passed through the HTTP request and sends it to Google Vision to detect the contents of the image and return a list of tags describing the content of the image.

The image URL should be passed as an HTTP parameter named **imageUri**. If this parameter is missing the service uses a default image to detect and return the contents.

### Deploying the Image Detector Service

1. **Location**: Go to the *gcp-label-image* subdirectory in the folder where you cloned the Git repository.
2. **Project**: Replace the *your-gcp-project-id* in the *serverless.yml* file with your Google Cloud project id.
3. **Credentials**: Replace the */path/to/your/gcp/credentials/json* in the *serverless.yml* file with the path to the JSON credentials that you saved in the GCP setup.
4. **Deploy**: In the service home directory, run the following command to deploy the *detectLabel* service on GCP. Make a note of the endpoint created. This endpoint is a URL that will end with *detect* as shown below.
```shell
$ sls deploy --verbose
...
Deployed functions
detectLabel
  https://your-region-your-project-id.cloudfunctions.net/detect
...
```
5. **Verify**: You can check your Google Cloud Functions [dashboard](https://console.cloud.google.com/functions) to ensure that your Cloud Function is deployed.
6. **Invoke@theTerminal**: Invoke the function *detectLabel* as follows:
```shell
$ sls invoke -f detectLabel
Serverless: ekvy90t28px8 Image Results: landmark historic site sky tourist attraction ancient rome ancient history ancient roman architecture medieval architecture night building
$
```
7. **Invoke@theBrowser**: Copy and paste the URL from the result of your *sls deploy* into the browser and add the *imageUri* parameter as follows:
  ```Far
  https://your-region-your-project-id.cloudfunctions.net/detect?imageUri=https://goo.gl/27gclq
  ```

# Image Detector Proxy

## aws-gcp-proxy
The aws-gcp-proxy is the service that will be deployed on AWS. It is a Python-based service that will take an image URL passed through the HTTP request and send it to the *Cloud Function* deployed on GCP.

In a typical use, you will use it to detect the content of an image uploaded to a S3 bucket and take appropriate actions based on the result. For instance, you could use it to blur/reject the image based on the vulgarity or get the image label and chain it to another service that will translate the labels to multiple languages to cater to your customer needs.

The image URL should be passed as an HTTP parameter named **imageUri**. If this parameter is missing the service uses a default image URL to detect and return the contents.

### Deploying the Image Detector Proxy Service

1. **Location**: Go to the *aws-gcp-proxy* subdirectory in the folder where  you cloned the Git repository.
2. **Environment Variable**: Edit the *setEnv.sh* file to point update the GFUNC_URL to point to your image detector service running on GCP.
3. **Deploy**: In the service home directory, run the following command to deploy the *proxy* service. Make a note of the AWS Gateway endpoint created. You will use this endpoint to test your service.
```shell
$ sls deploy -v
...
GET - https://urmileagemaydiffer.execute-api.us-east-1.amazonaws.com/dev/detect
...
```
4. **Verify**: You can check your AWS Lambda [dashboard](https://console.aws.amazon.com/lambda/home) to ensure that the Lambda function was created and the environment variable is being passed.
5. **Invoke**: Copy and paste the AWS Gateway API URL into the browser and add the *imageUri* parameter as follows:
```Far
https://urmileagemaydiffer.execute-api.us-east-1.amazonaws.com/dev/detect?imageUri=https://goo.gl/27gclq
```

# Conclusion

Serverless Framework makes it painless to deploy services across multiple cloud providers without having to deal with the idiosyncrasies of various providers allowing you to focus on your application. Additionally, the framework allows you to use the right provider for the right service, cuts the time spent on deployment while allowing you to manage the code and infrastructure across multiple providers.
