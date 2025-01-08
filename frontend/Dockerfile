FROM node:slim
WORKDIR /app
COPY package.json .
RUN --mount=type=cache,target=/root/.npm npm install
COPY . .
ENTRYPOINT ["node"]
CMD ["app.js"]
EXPOSE 3000