token = ''
webhook = False
WEBHOOK_HOST = '0.0.0.0'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(token)

DATABASE_HOST = "postgres"
DATABASE_PORT = "5432"
DATABASE_USERNAME = "jpeger_user"
DATABASE_PASSWORD = "JpE34g487ER!"
DATABASE_NAME = "jpeger"
