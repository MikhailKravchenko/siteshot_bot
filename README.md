# Jepeger bot for Telegram
����� �էݧ� ���٧էѧߧڧ� �ӧ֧�-��ܧ�ڧߧ�����.
�����ҧ� ���ݧ��ڧ�� ��ܧ�ڧߧ��� - �����ѧӧ��� URL �ѧէ�֧� ��ѧۧ��. 
���ѧ��ڧާ֧�, wikipedia.org.

? �� ���ާ���� �ҧ��� �ӧ� �ާ�ا֧�� ����ӧ֧���� ���է�٧�ڧ�֧ݧ�ߧ�� ����ݧܧ�. (���ۧ�ڧݧ�ԧԧ֧��, ��ڧ�ڧߧԧ�ӧ�� �ӧ֧�-��ѧۧ��, ��ܧ�ڧާ֧�� �� ��.��)

? ���� ��ѧܧا� �ާ�ا֧�� �է�ҧѧӧڧ�� �ާ֧ߧ� �� ��ӧ�� ��ѧ��, �� �� ��ާ�ԧ� ����ӧ֧���� ����ݧܧ�, �ܧ������ �����ѧӧݧ��� ���ݧ�٧�ӧѧ�֧ݧ�

#Get Started:

git@github.com:MikhailKravchenko/siteshot_bot.git

����ѧߧ�ӧڧ�� ��֧�֧ާ֧ߧߧ�� ��ܧ��ا֧ߧڧ�:

- �էݧ� ����ѧӧܧ� �� webhook https://dvmn.org/encyclopedia/about-chatbots/webhook/

webhook = True
    
    ������֧ҧ�֧���  ��ܧѧ٧ѧ�� token = ''
    + �է���ݧߧڧ�֧ݧ�ߧ� ��ܧѧ٧ѧ�� ��֧��ڧ�ڧܧѧ�� ssl �� ��ѧ�ѧާ֧��� ��֧�ӧ֧��
    WEBHOOK_HOST = '0.0.0.0'
    WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key

webhook = False

    ������֧ҧ�֧��� ���ݧ�ܧ� ��ܧѧ٧ѧ�� token = ''

 ����ҧڧ�ѧ֧� ��ҧ�ѧ٧�:

    docker-compose -f docker-compose.yml up -d --build
