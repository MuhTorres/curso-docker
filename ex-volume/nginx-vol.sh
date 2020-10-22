docker run \
--name nginx-vol \
-p 8080:80 \
-v $(pwd)/html:/usr/share/nginx/html \
nginx:latest