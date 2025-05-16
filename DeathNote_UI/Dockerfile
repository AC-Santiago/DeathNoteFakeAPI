FROM nginx:alpine

COPY DeathNote.html DeathNote.css DeathNote.js /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
