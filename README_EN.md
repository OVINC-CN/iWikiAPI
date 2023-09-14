## iWikiAPI

iWikiAPI 为 iWiki 提供 API 服务

### Deployment

构建镜像

```shell
docker build . -t <IMAGE_NAME>
```

准备环境变量，并存储到 `.env` 文件中

```shell
# UWSGI 配置，PROCESSES 一般为 CPU 核心数，THREADS 可以为 5 * CPU
UWSGI_PROCESSES=2
UWSGI_THREADS=10
# 是否开启 DEBUG 模式，生产环境部署请关闭
DEBUG=False
# 日志等级
LOG_LEVEL=INFO
# APP 配置相关信息，请先在 OVINC UNION API 中注册
APP_CODE=
APP_SECRET=
# 后端 HOST，不包含 HTTP 协议以及路径，如 api.<your domain>.cn
BACKEND_HOST=
# 前端访问地址，不包含路径，如 https://<your domain>.cn
FRONTEND_URL=
# DB 配置
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
# Redis 配置
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_DB=
# SESSION 配置，一般配置为带 . 的根域名，如 .<your domain>.cn
SESSION_COOKIE_DOMAIN=
# OVINC UNION API 访问地址，如 https://api.<your domain>.cn
OVINC_API_DOMAIN=
# 腾讯云相关配置，如不使用图片文件上传功能可以不配置
QCLOUD_SECRET_ID=
QCLOUD_SECRET_KEY=
QCLOUD_COS_BUCKET=
QCLOUD_COS_URL=
```

部署服务

```shell
docker run --rm -itd --env-file=.env -p 8020:8020 <IMAGE_NAME> bin/run.sh
```
