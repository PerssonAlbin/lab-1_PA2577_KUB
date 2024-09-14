# Build Stage
FROM node:lts-alpine as build-stage

#ENV NODE_ENV=production
ENV APP_HOME=/usr/src/app

RUN mkdir -p $APP_HOME

COPY . $APP_HOME

RUN cd $APP_HOME && npm install \
  --prefer-offline \
  --pure-lockfile \
  --non-interactive

WORKDIR $APP_HOME

EXPOSE 3000

CMD ["node", "index.js"]
