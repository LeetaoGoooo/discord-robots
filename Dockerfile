FROM gorialis/discord.py

RUN apt-get update \
    && apt-get -y install git \
    gcc \ 
    python3-dev

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./
CMD ["bash", "./run.sh"]