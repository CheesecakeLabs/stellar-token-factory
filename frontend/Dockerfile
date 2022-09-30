FROM node:16.13-bullseye-slim AS builder
WORKDIR /usr/src/app
COPY . .

FROM builder AS dev
RUN npm ci
ENTRYPOINT [ "npm", "run", "start:dev" ]

FROM builder AS dev-docker
RUN npm ci
ENTRYPOINT [ "npm", "run", "start:dev-docker" ]

FROM builder AS builder-prod
RUN npm ci --production
ARG REACT_APP_API_URL
ARG REACT_APP_SENTRY_DSN
ARG REACT_APP_USERNAME
ARG REACT_APP_PASSWORD
ARG REACT_APP_NETWORK
ENV REACT_APP_API_URL=${REACT_APP_API_URL:?"ERR: REACT_APP_API_URL not set in Dockerfile"}
ENV REACT_APP_SENTRY_DSN=${REACT_APP_SENTRY_DSN:?"ERR: REACT_APP_SENTRY_DSN not set in Dockerfile"}
ENV REACT_APP_USERNAME=${REACT_APP_USERNAME:?"ERR: REACT_APP_USERNAME not set in Dockerfile"}
ENV REACT_APP_PASSWORD=${REACT_APP_PASSWORD:?"ERR: REACT_APP_PASSWORD not set in Dockerfile"}
ENV REACT_APP_NETWORK=${REACT_APP_NETWORK:?"ERR: REACT_APP_NETWORK not set in Dockerfile"}
RUN npm run build

FROM node:16.13-bullseye-slim AS prod
WORKDIR /usr/src/app
RUN npm install -g serve
COPY --from=builder-prod /usr/src/app/build/ /usr/src/app/build/
ENTRYPOINT [ "serve", "-l", "8000", "-s", "build" ]