FROM node:alpine

COPY package.json ./
COPY package-lock.json ./

COPY src src
COPY public public

RUN npm install --silent
RUN npm build

CMD ["npm", "start"]