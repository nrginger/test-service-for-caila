# ner-test-service-for-caila

This repository is a test named entity recogintion service for [Caila](https://app.caila.io/) based on HF ML model.

> Caila is a platform for hosting microservices based on ML models.
> It is a powerful tool that can cover every aspect of your solution’s lifecycle, from model training and QA to deployment and monitoring.

## Get started

Start by getting yourself acquainted with the contents of [`main.py`](./src/main.py).
In terms of features, this is a service for recognition of names and surmanes (NER PER) in English texts, based on [flair/ner-english-fast model](https://huggingface.co/flair/ner-english-fast):

- It has no `fit` method, so it can’t be trained.
- Its `predict` method returns a list of names and surnames found in the text of the query.

The service relies on the Caila [Python SDK](https://github.com/just-ai/mlp-python-sdk) to expose its functionality to the platform.

## Get API token on Hugging Face

To run this service locally you do not need an API token, the model will be installed on your computer in the cache.

See [How to use the model](https://huggingface.co/flair/ner-english-fast/blob/main/README.md#demo-how-to-use-in-flair).

To run this service on [Caila](https://app.caila.io/) platform:

- Sign in [Hugging Face](https://huggingface.co/) or sign up for a new account.
  
- Go to *Your profile* --> *Access Tokens*.

- Click *Create new token*.

## Build Docker image

To build the service locally, run `./build.sh` in the project root.
You need to have [Docker Engine](https://docs.docker.com/engine/install/) installed and running.

The build script will create a Docker image, push it to the [public Caila Docker registry](https://docker-pub.caila.io/), and print the image URL to the console:

```txt
--------------------------------------------------
Docker image: docker-pub.caila.io/caila-public/mlp-hello-world-service-xxxxxxxxxxxxxxxx:main
--------------------------------------------------
```

You will need this URL to configure your service in Caila.

> ⚠ The public Caila Docker registry has a limited storage time and is intended for educational purposes only.
> Do not use it for production.

## Create Caila service

1. Sign in to [Caila](https://app.caila.io/) or sign up for a new account.
2. Go to *My space* and select *Images* in the sidebar.
    > 🛈 If you don’t see this tab, go to *My space* → *Services*, select *Create service*, and submit a request for access.
    > Our customer support team will get back to you shortly.
3. Select *Create image*. Provide the image name and the URL you got from the build script.
4. On the image description page, select *Create service*. Provide the service name and leave the other settings at their defaults.
5. You should now see your service in the *Services* tab. Go to its details page and select *Diagnostics*.
6. Select *Add instance*. Wait for the instance to start (the status indicator should turn from yellow to green).
7. Go to the *Testing* and try sending a request with a JSON body like 
`{"text": "Pushkin was born into the Russian nobility in Moscow. His father, Sergey Lvovich Pushkin, belonged to an old noble family. One of his maternal great-grandfathers was Major-General Abram Petrovich Gannibal, a nobleman of African origin who was kidnapped from his homeland by the Ottomans, then freed by the Russian Emperor and raised in the Emperor's court household as his godson."}`.

If you see response
`{
  "person_names": [
    "Pushkin",
    "Sergey Lvovich Pushkin",
    "MajorGeneral Abram Petrovich Gannibal"
  ]
}` 

in the output, congratulations!
Your service is up and running.

> ℹ️ If your service is not working try deleting and iserting spaces after dots manually or improve preprocessing of the text in [`main.py`](./src/main.py).
   Also note, that there is a limit of the query size: 1000 characters.

If you would like to learn more about Caila, check out our official [documentation](https://docs.caila.io/).

## License

This project is licensed under Apache License 2.0.
