FROM node:20

WORKDIR /app/frontend

RUN mkdir -p /app/backend

COPY package*.json ./
RUN npm install

COPY vite.config.ts tsconfig.json ./
COPY src/* ./src/