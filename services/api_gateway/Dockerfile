FROM node:23-slim

WORKDIR /appp

COPY package*.json ./

RUN npm install --omit=dev

ENV NODE_ENV=docker
COPY .env.docker .env

COPY . .

EXPOSE 8080

CMD ["node", "server.js"]

