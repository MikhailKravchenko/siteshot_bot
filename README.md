# Jpeger bot for Telegram
Бот для создания веб-скриншотов.
Чтобы получить скриншот - отправьте URL адрес сайта. 
Например, wikipedia.org.

• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)

• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи

# Documentation

Полезные команды:

    /start - Приветствие
    /admin - Команда для админского чата выводит информацию о командах доступных для администратора
    /setadminchat - назначает текущий чат административным
    /statistic - получение статистики о работе бота (доступ только в админском чате)



# Get Started:

Для запуска понадобится сформировать докер контейнеры и запустить их. 
Если на сервере не установлен Docker, то самое время его установить:

https://docs.docker.com/engine/install/ubuntu/
https://docs.docker.com/compose/install/compose-plugin/#installing-compose-on-linux-systems

Клонировать репозиторий в удобное место:

    git@github.com:MikhailKravchenko/siteshot_bot.git

Установить переменные окружения:

    src/env.py

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

# Information
История разработки:
https://github.com/users/MikhailKravchenko/projects/1
