# ================= SERVICE PROXY TEMPLATE =================

# HTTP → HTTPS redirect
server {
    listen 80;
    listen [::]:80;

    server_name [DOMAIN_NAME];
    return 301 https://$host$request_uri;
}

# HTTPS reverse proxy
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name [DOMAIN_NAME];

    # 🔐 Wildcard SSL (acme.sh + Namecheap DNS-01)
    ssl_certificate     /etc/nginx/ssl/arpansahu.space/fullchain.pem;
         proxy_set_header Connection "upgrade";
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/arpansahu.me/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/arpansahu.me/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}