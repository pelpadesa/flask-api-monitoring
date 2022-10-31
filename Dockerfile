FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY .env ./
COPY tag-server.py ./

COPY . .

EXPOSE 80/tcp

CMD [ "python", "./tag-server.py" ]