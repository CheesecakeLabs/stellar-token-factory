## Project Architecture

You can check the project architecture [here](./src/docs/ARCHITECTURE.md)

## Requirements

- [`NodeJS 16+`](https://nodejs.org/en/)
- [`NPM 6.14+`](https://www.npmjs.com/)
* [`Homebrew`](https://brew.sh/ "Installation")
* [`Make`](https://formulae.brew.sh/formula/make)
* [`Docker Desktop`](https://www.docker.com/products/docker-desktop/)

> We suggest use of [NVM](https://github.com/nvm-sh/nvm/blob/master/README.md) to manage your node versions.

## Getting Started 

### Running Locally

1. Copy the file `src/config/.env.example` to `src/config/.env.local`.

2. Install dependencies
```shell
$ make install-dev
```

3. Run
```shell
make start-dev
```

The application will be available at [http://localhost:3000/](http://localhost:3000/)

### Running with Docker

1. Copy the file `src/config/.env.example` to `src/config/.env.local`.

2. Run
```bash
make docker-up
```

The application will be available at [http://localhost:3000/](http://localhost:3000/)

Show lint erros:
```shell
make lint
```

Format code with prettier and fix the code style:
```shell
make format-code
```

## Creating a production build

The following command will generate an optimized production build. The statics files will be generated at `build/` folder.

````shell
make build
````

## Scripts

In the project directory, you can run all of [react-scripts](https://create-react-app.dev/docs/available-scripts) commands.

## Artifacts

The project has a `Dockerfile` that can be used to build Docker images. It has two targets:
* `dev`: used in local environment for development.
* `prod`: used in staging and production environments. When you choose this target, you need to send the `build args` required by the `Dockerfile` to build the image.
