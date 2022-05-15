# proxy6-middleware

[![Build Status](https://travis-ci.org/MailfTrue/proxy6-middleware.svg?branch=master)](https://travis-ci.org/MailfTrue/proxy6-middleware)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Intermediate layer between the buyer and proxy6.net for commission calculation. Check out the project's [documentation](http://MailfTrue.github.io/proxy6-middleware/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
