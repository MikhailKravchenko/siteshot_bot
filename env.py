token = '885507314:AAE2iVUAjAkoZ8M5jIIuopf6bIx6FsqwUHY'
webhook = False
WEBHOOK_HOST = '217.163.29.237'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '217.163.29.237'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = '/home/lukas/cert/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/home/lukas/cert/webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(token)

DATABASE_HOST = "217.163.29.237"
DATABASE_PORT = "5432"
DATABASE_USERNAME = "utest2"
DATABASE_PASSWORD = "913SS@236"
DATABASE_NAME = "djangobot"

REDIS_HOST = "217.163.29.237"
REDIS_PORT = "6379"
REDIS_PASSWORD = "913sS@236"
