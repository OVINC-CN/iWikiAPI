## iWikiAPI

iWikiAPI provides API for iWiki

### Deployment

Build image

```shell
docker build . -t <IMAGE_NAME>
```

Prepare the environment variables and store them in the .env file.

```shell
# UWSGI configuration, PROCESSES is usually the number of CPU cores, THREADS can be set to 5 * CPU.
UWSGI_PROCESSES=2
UWSGI_THREADS=10
# Celery Worker
WORKER_COUNT=2
# Whether to enable DEBUG mode, please disable it for production environment deployment.
DEBUG=False
# Log Level
LOG_LEVEL=INFO
# Please register the relevant APP configuration information in the OVINC UNION API first.
APP_CODE=
APP_SECRET=
# Backend HOST, excluding the HTTP protocol and path, such as api.<your domain>.cn.
BACKEND_HOST=
# Frontend access address, excluding the path, such as https://<your domain>.cn.
FRONTEND_URL=
# DB Config
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
# Redis Config
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_DB=
# SESSION configuration, usually configured as a root domain with a dot, such as .<your domain>.cn.
SESSION_COOKIE_DOMAIN=
# The access address for OVINC UNION API is like https://api.<your domain>.cn.
OVINC_API_DOMAIN=
# Tencent Cloud configuration is not required if the image file upload functionality is not being used.
QCLOUD_SECRET_ID=
QCLOUD_SECRET_KEY=
QCLOUD_COS_BUCKET=
QCLOUD_COS_URL=
```

Deploy Service

```shell
docker run --rm -itd --env-file=.env -p 8020:8020 <IMAGE_NAME> bin/run.sh
```
