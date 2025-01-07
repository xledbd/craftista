FROM node:slim
WORKDIR /app
COPY . .
RUN npm install
ENTRYPOINT ["node", "app.js"]
EXPOSE 3000