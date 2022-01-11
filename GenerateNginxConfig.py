from GenerateIOs import readConfig

CONTENT_80 = '''
server {
    listen 80;
    server_name cyclonejoker.xyz;
    rewrite ^(.*)$ https://$host$1 permanent;
}
'''

CONTENT_443 = '''
server {
    listen 433 ssl;
    server_name miniserver;

    ssl_certificate /home/yunjies/ssl/cyclonejoker.xyz/1_cyclonejoker.xyz_bundle.crt;
    ssl_certificate_key /home/yunjies/ssl/cyclonejoker.xyz/2_cyclonejoker.xyz.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location /wss/ {
        proxy_pass https://192.168.1.224:8443;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_read_timeout 86400;
    }

    location / {
        proxy_pass https://192.168.1.224:8443/; # The Unifi Controller Port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
    }
}
'''

TEMPLATE_SERVER = '''
server {{
    listen {} ssl;
    server_name cyclonejoker.xyz;

    ssl_certificate /home/yunjies/ssl/cyclonejoker.xyz/1_cyclonejoker.xyz_bundle.crt;
    ssl_certificate_key /home/yunjies/ssl/cyclonejoker.xyz/2_cyclonejoker.xyz.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    
    location / {{
        proxy_pass {}://{}{};{}
    }}
}}
'''

CONFIG_PATH = '/etc/nginx/conf.d/cyclonejoker.xyz.conf'

def main():
    configs = readConfig()
    data = [CONTENT_80, CONTENT_443]
    for config in configs:
        if 'source_ip' in config:
            port = config['port']
            https = 'https' if config['https'] == True else 'http'
            source_ip = config['source_ip']
            source_port = (':' + config['source_port']) if 'source_port' in config else ''
            addition_location = config['addition_location'] if ('addition_location' in config) else ''
            data.append(TEMPLATE_SERVER.format(port, https, source_ip, source_port, addition_location))
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.writelines(data)
        

if __name__ == "__main__":
    main()
