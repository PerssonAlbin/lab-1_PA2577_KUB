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

RUN npm run generate

# Production Stage
FROM nginx:stable-alpine as production-stage

ENV APP_HOME=/usr/src/app

COPY --from=build-stage $APP_HOME/.output/public /usr/share/nginx/html

RUN chown nginx:nginx /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
