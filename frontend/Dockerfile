# Dockerfile (Production)
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN VITE_API_URL=$VITE_API_URL npm run build
RUN npm run build

# 👇 only static files
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["sh", "-c", "while :; do sleep 2073600; done"]
