FROM node:20.19.0 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

# copie de la configuration Nginx personnaosée pr gérer le routage SPA
COPY nginx.conf /etc/nginx/conf.d/default.conf

# copie des fichiers buildés de l'appli
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]