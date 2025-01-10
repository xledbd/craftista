FROM node:slim

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
ENTRYPOINT ["node"]
CMD ["app.js"]
EXPOSE 3000