FROM gorialis/discord.py

RUN apt-get update \
    && apt-get -y install git \
    gcc \ 
    firefox-esr \
    python3-dev \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    fonts-ipafont-mincho \ 
    fonts-ipafont-gothic \
    fonts-unfonts-core

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./
CMD ["bash", "./run.sh"]