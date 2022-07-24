FROM python:3.8

RUN apt-get update && apt-get install -y --no-install-recommends vim htop
RUN apt-get install -y python3-pip
# Pyppeteer сразу скачиваем и устанавливаем, что бы не ждать при первом запросе и исключить связанные с этим ошибки
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY ./ ./src/
WORKDIR /src/
EXPOSE 80
CMD ["python", "./core.py"]