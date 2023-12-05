FROM node:18-alpine

WORKDIR /react-app

COPY frontend/package.json /react-app/
COPY frontend/public/ /react-app/public/
COPY frontend/src/ /react-app/src/

RUN npm install

ENTRYPOINT ["npm", "start"]