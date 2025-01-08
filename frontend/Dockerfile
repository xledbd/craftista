FROM node:slim
WORKDIR /app
COPY . .
RUN npm install
ENTRYPOINT ["node"]
CMD ["app.js"]
EXPOSE 3000