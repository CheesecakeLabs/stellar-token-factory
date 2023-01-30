[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# tokenfactory_stellar_back

Boilerplate project using Django and Django REST Framework.
Currently supporting only Python 3.x.

# Requirements

* [`Python (3.10.*)`](https://www.python.org/downloads/ "Installation")
* [`Homebrew`](https://brew.sh/ "Installation")
* [`Make`](https://formulae.brew.sh/formula/make)
* [`Docker Desktop`](https://www.docker.com/products/docker-desktop/)

## Getting Started 

### Running Locally

1. Copy the file `src/api/core/local.example.env` to `src/api/core/local.env`.

2. Install and activate Virtual Environment
```bash
$ make install-venv
$ source venv/bin/activate
```

3. Install requirements
```bash
$ make install-req     
$ make install-dev-req 
$ make install-test-req
```

4. Collect Static
```bash
$ make collect-static
```

5. Run
```bash
$ make run
```

The application will be available at [http://localhost:8000/](http://localhost:8000/)

### Running with Docker

Follow the instructions in the project root folder.

## Tests and lint

First, install requirements:
```bash
$ make install-req     
$ make install-dev-req 
$ make install-test-req
```

Test the application:
```bash
make test
```

Show lint errors:
```bash
make lint
```

Show code format errors:
```bash
make code-formatter-check
```

Try to fix code format errors:
```bash
make code-formatter-fix
```

## Install Black code formatter to your editor

Check code syntax and style before committing changes.

Pre-commit hook may be installed using the following steps:

```bash
$ make install-dev-req 
$ make install-pre-commit
```

## How to setup Sentry
Go to `src/api/core/local.env` and add your Sentry DSN value in `SENTRY_DSN` var.

## Handling Business Error

```python
from helpers.business_errors import BusinessException, EXAMPLE_ERROR
...
if logic_check:
    raise BusinessException(error_code=EXAMPLE_ERROR)
```

`BusinessException` extends `APIException` (Django Rest Framework) and `ValidationError` (Django), so it is handled by their middlewares by default.

## CloudWatch Logger
The CloudWatch logger is used to create more personalized and specific logs, unlike Sentry that logs any error generated in the system, CloudWatch logs only when called.

##### Checklist for setup
- [ ] Set the permissions on the AWS task.
- [ ] Update `local.env`
- [ ] Update Django `settings.py`
- [ ] Call logger

### Update `local.env`
To enable CloudWatch, you must go to `src/api/core/local.env` and   put the name of the log group defined in AWS in `AWS_LOG_GROUP_NAME` and also put the AWS region on the `AWS_REGION`

### Update `settings.py`
By default we have a generic logger called "cloud_watch", which if the variable `AWS_CLOUDWATCH_LOG_GROUP_NAME` is not set, it only logs in the terminal.

To create new loggers, you must create both `handlers` and `loggers` inside `LOGGING`

Handler example:
```json
"handler_name": {  
    "boto3_client": boto3_logs_client,  
	"class": "logging.handlers.CloudWatchLogHandler",  
	"level": "INFO",  
	"filters": ["require_debug_false"],  
	"formatter": "main_formatter",  
	"log_group": env.str("AWS_CLOUDWATCH_LOG_GROUP_NAME"),  
	"stream_name": "sub_folder_name",
    }
```
**Note**: `stream_name` is the parameter that will name the subfolder where the logs will be inside the `log_group`, if it doesn't exist, it will be created automatically. If you don't pass this value by parameter, a subfolder will be created with a random hash

Logger example:
```json
"logger_name": {
	"level": "INFO", 
	"handlers": ["handler_name"], 
	"propagate": False
},
```

### Call logger
Now to be able to log your message just call the logger anywhere as follows:
```python
import logging  

logger = logging.getLogger("logger_name")
logger.info("Message")
# or
logger.info(json)
```

## Artifacts

The project has a `Dockerfile` that can be used to build Docker images. It has two targets:
* `dev`: used in local environment for development.
* `prod`: used in staging and production environments. You don't need to create a `local.env` to run this image in staging or production environments, just pass the values as environment variables.
