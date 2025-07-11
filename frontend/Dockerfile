# Dockerfile
FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN echo "🧪 BUILD: VITE_API_URL = $VITE_API_URL"

RUN echo "VITE_API_URL=$VITE_API_URL" > .env.production

RUN npm run build

# Nginx
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
