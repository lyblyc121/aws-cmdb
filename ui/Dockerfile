## build frontend dist
FROM 871006737058.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-base-js:latest as build-stage
COPY src /app
RUN npm run build


## frontend image
FROM 871006737058.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-base-js:base as production

RUN rm -rf  /var/www/cmdb


COPY cmdb_frontend.conf  /etc/nginx/conf.d/cmdb_frontend.conf
COPY dist  /var/www/cmdb
WORKDIR /var/www/cmdb/

EXPOSE 80
EXPOSE 443

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
