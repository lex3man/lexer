server {
    server_name investexpert.pro www.investexpert.pro;
    root /master/www/investexpert.pro/root;
    index index.htm index.html;

    location / {
        try_files $uri $uri/;	
    }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/investexpert.pro/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/investexpert.pro/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = www.investexpert.pro) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = investexpert.pro) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    server_name investexpert.pro www.investexpert.pro;
    listen 80;
    return 404; # managed by Certbot




}