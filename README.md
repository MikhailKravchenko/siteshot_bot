# Jepeger bot for Telegram
§¢§à§ä §Õ§Ý§ñ §ã§à§Ù§Õ§Ñ§ß§Ú§ñ §Ó§Ö§Ò-§ã§Ü§â§Ú§ß§ê§à§ä§à§Ó.
§¹§ä§à§Ò§í §á§à§Ý§å§é§Ú§ä§î §ã§Ü§â§Ú§ß§ê§à§ä - §à§ä§á§â§Ñ§Ó§î§ä§Ö URL §Ñ§Õ§â§Ö§ã §ã§Ñ§Û§ä§Ñ. 
§¯§Ñ§á§â§Ú§Þ§Ö§â, wikipedia.org.

? §³ §á§à§Þ§à§ë§î§ð §Ò§à§ä§Ñ §Ó§í §Þ§à§Ø§Ö§ä§Ö §á§â§à§Ó§Ö§â§ñ§ä§î §á§à§Õ§à§Ù§â§Ú§ä§Ö§Ý§î§ß§í§Ö §ã§ã§í§Ý§Ü§Ú. (§¡§Û§á§Ú§Ý§à§Ô§Ô§Ö§â§í, §æ§Ú§ê§Ú§ß§Ô§à§Ó§í§Ö §Ó§Ö§Ò-§ã§Ñ§Û§ä§í, §ã§Ü§â§Ú§Þ§Ö§â§í §Ú §ä.§á)

? §£§í §ä§Ñ§Ü§Ø§Ö §Þ§à§Ø§Ö§ä§Ö §Õ§à§Ò§Ñ§Ó§Ú§ä§î §Þ§Ö§ß§ñ §Ó §ã§Ó§à§Ú §é§Ñ§ä§í, §Ú §ñ §ã§Þ§à§Ô§å §á§â§à§Ó§Ö§â§ñ§ä§î §ã§ã§í§Ý§Ü§Ú, §Ü§à§ä§à§â§í§Ö §à§ä§á§â§Ñ§Ó§Ý§ñ§ð§ä §á§à§Ý§î§Ù§à§Ó§Ñ§ä§Ö§Ý§Ú

#Get Started:

git@github.com:MikhailKravchenko/siteshot_bot.git

§µ§ä§Ñ§ß§à§Ó§Ú§ä§î §á§Ö§â§Ö§Þ§Ö§ß§ß§í§Ö §à§Ü§â§å§Ø§Ö§ß§Ú§ñ:

- §Õ§Ý§ñ §ã§á§â§Ñ§Ó§Ü§Ú §à webhook https://dvmn.org/encyclopedia/about-chatbots/webhook/

webhook = True
    
    §±§à§ä§â§Ö§Ò§å§Ö§ä§ã§ñ  §å§Ü§Ñ§Ù§Ñ§ä§î token = ''
    + §Õ§à§á§à§Ý§ß§Ú§ä§Ö§Ý§î§ß§à §å§Ü§Ñ§Ù§Ñ§ä§î §ã§Ö§â§ä§Ú§æ§Ú§Ü§Ñ§ä§í ssl §Ú §á§Ñ§â§Ñ§Þ§Ö§ä§â§í §ã§Ö§â§Ó§Ö§â§Ñ
    WEBHOOK_HOST = '0.0.0.0'
    WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key

webhook = False

    §±§à§ä§â§Ö§Ò§å§Ö§ä§ã§ñ §ä§à§Ý§î§Ü§à §å§Ü§Ñ§Ù§Ñ§ä§î token = ''

 §³§à§Ò§Ú§â§Ñ§Ö§Þ §à§Ò§â§Ñ§Ù§í:

    docker-compose -f docker-compose.yml up -d --build
