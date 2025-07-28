# Dockerfile (Prod)
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN echo "VITE_API_URL=$VITE_API_URL" > .env.production
RUN npm run build

# deploy static files
FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["sh", "-c", "while :; do sleep 2073600; done"]
