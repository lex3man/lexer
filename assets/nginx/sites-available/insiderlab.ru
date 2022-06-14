server {
    server_name insiderlab.ru www.insiderlab.ru;
    root /home/master/www/insiderlab.ru/root;
    index index.html index.htm;

    location / {
        try_files $uri $uri/;
    }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/insiderlab.ru/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/insiderlab.ru/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = www.insiderlab.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = insiderlab.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    server_name insiderlab.ru www.insiderlab.ru;
    listen 80;
    return 404; # managed by Certbot




}