FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY tag-server.py ./

COPY . .

ARG SERVE_PORT=80
ENV SERVE_PORT ${SERVE_PORT}
EXPOSE ${SERVE_PORT}/tcp

CMD ["sh", "-c", "python ./tag-server.py ${SERVE_PORT}"]