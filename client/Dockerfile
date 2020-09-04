FROM node:14-stretch as build-stage


WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Create the container from the alpine linux image
FROM alpine:3.7 as production-image

# Add nginx and nodejs
RUN apk add --update nginx

# Create the directories we will need
RUN mkdir -p /var/log/nginx
RUN mkdir -p /var/www/html

# Copy the respective nginx configuration files
COPY .nginx/nginx.conf /etc/nginx/nginx.conf
COPY .nginx/default.conf /etc/nginx/conf.d/default.conf

# copy the built app to our served directory
COPY --from=build-stage /app/dist /var/www/html

# make all files belong to the nginx user
RUN chown nginx:nginx /var/www/html

EXPOSE 80

# start nginx and keep the process from backgrounding and the container from quitting
CMD ["nginx", "-g", "daemon off;"]
