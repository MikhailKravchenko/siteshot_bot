# Jpeger bot for Telegram
Бот для создания веб-скриншотов.
Чтобы получить скриншот - отправьте URL адрес сайта. 
Например, wikipedia.org.

• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)

• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи

#Get Started:

git@github.com:MikhailKravchenko/siteshot_bot.git

Установить переменные окружения:

- для справки о webhook https://dvmn.org/encyclopedia/about-chatbots/webhook/

webhook = True
    
    Потребуется  указать token = ''
    + дополнительно указать сертификаты ssl и параметры сервера
    WEBHOOK_HOST = '0.0.0.0'
    WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key

webhook = False

    Потребуется только указать token = ''

 Собираем образы:

    docker-compose -f docker-compose.yml up -d --build
