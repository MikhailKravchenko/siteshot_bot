# Jpeger bot for Telegram
Bot for creating web screenshots.
To get a screenshot - send the URL of the site.
For example, wikipedia.org.

• With the help of a bot you can check suspicious links. (IP loggers, phishing websites, screamers, etc.)

• You can also add me to your chats so I can check the links that users send

# documentation

Useful commands:

    /start - Welcome
    /admin - Command for admin chat displays information about the commands available to the administrator
    /setadminchat - sets current chat as admin chat
    /statistic - getting statistics about the bot's work (access only in the admin chat)



# Get Started:

To start, you need to create docker containers and run them.
If Docker is not installed on the server, then it's time to install it:

https://docs.docker.com/engine/install/ubuntu/
https://docs.docker.com/compose/install/compose-plugin/#installing-compose-on-linux-systems

Clone the repository to a convenient location:

    git@github.com:MikhailKravchenko/siteshot_bot.git

Set environment variables:

    src/env.py

- for help about webhook https://dvmn.org/encyclopedia/about-chatbots/webhook/

webhook=true
    
    You will need to specify token = ''
    + additionally specify ssl certificates and server parameters
    WEBHOOK_HOST = '0.0.0.0'
    WEBHOOK_PORT = 443 # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0' # In some VPS you may need to put here the IP addr
    WEBHOOK_SSL_CERT = 'webhook_cert.pem' # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem' # Path to the ssl private key

webhook = False

    You only need to specify token = ''

 Collecting images:

    docker-compose -f docker-compose.yml up -d --build

#Information
Development history:
https://github.com/users/MikhailKravchenko/projects/1