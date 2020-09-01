FROM nginx:latest
ARG APP_NAME
ARG APP_PORT
ARG LISTEN_PORT
ARG HOST_NAME

RUN rm -rf /etc/nginx/conf.d/default.conf &&\
    rm -rf /etc/nginx/conf.d/nginx.conf &&\
    touch /etc/nginx/conf.d/default.conf &&\
    echo "                                                                                      \
            proxy_cache_path /etc/nginx/cache levels=1:2 keys_zone=${APP_NAME}_cache:128m;      \   
            upstream $APP_NAME {                                                                \
                zone $APP_NAME 64k;                                                             \
                server nginx-unit:$APP_PORT;                                                    \
            }                                                                                   \
            server {                                                                            \
                server_name $HOST_NAME;                                                         \
                listen $LISTEN_PORT;                                                            \
                charset utf-8;                                                                  \
                proxy_cache ${APP_NAME}_cache;                                                  \
                proxy_cache_valid 200 60m;                                                      \
                location / {                                                                    \
                    proxy_pass http://$APP_NAME;                                                \
                    proxy_redirect off;                                                         \
                }                                                                               \
                location /static/ {                                                             \
                    alias /static/;                                                             \
                }                                                                               \
                location /media/ {                                                              \
                    alias /media/;                                                              \
                }                                                                               \
            }                                                                                   \
            server_tokens off;                                                                  \
        "                                                                                       \ 
> /etc/nginx/conf.d/default.conf
