<!-- PROJECT LOGO -->
<br />
<p align="center">
    <img width="50%" src="https://images.sympla.com.br/5d11137d98ce3.png" alt="Logo">
</p>

# Cheesecake Stellar Token Factory

Cheesecake Stellar Token Factory is composed by:

- [Frontend](./frontend): React web application
- [Backend](./backend): Python with Django

# Topics

- [Cheesecake Stellar Token Factory](#cheesecake-stellar-token-factory)
- [Topics](#topics)
- [Getting started](#getting-started)
  - [Requirements](#requirements)
  - [Docker Desktop Recommendations](#docker-desktop-recommendations)
  - [Running application locally](#running-application-locally)
    - [Running with Docker](#running-with-docker)
  - [Infrastructure Architecture](#infrastructure-architecture)

# Getting started

## Requirements

- [`Docker Desktop`](https://www.docker.com/products/docker-desktop/)
- [`Make`](https://formulae.brew.sh/formula/make)

## Docker Desktop Recommendations

To run this project, there are some recommendations about the Docker Desktop resources configuration. You can find how to edit the resources settings [here](https://docs.docker.com/desktop/settings/mac/#resources).
* CPUs: 1
* Memory: 1GB

## Running application locally

### Running with Docker

To start all the applications locally, follow these steps:

**1.** To change and overide pre-defined environment variables, you can create a `.env` file in the `KEY=VALUE` pair format in the project's root directory, so Docker can pass these environment variables to the running applications. Check the `.env.example` to see available environment variables.

**2.** Start the applications:

```bash
$ make docker-run
```

This will download, build the applications and configure all the infrastructure needed to run them, which will respond in the following routes:

- Frontend: [`http://localhost:3000`](http://localhost:3000)
- Backend: [`http://localhost:8000`](http://localhost:8000)

**3.** To stop the applications:

```bash
$ make docker-stop
```

### Running components with Docker

If you want to, you can run the components separatly. For example, if you want to start only the Frontend, you can run:

```bash
$ make docker-run-frontend
```

You can find all possible ways of running the components in the Makefile:

```bash
$ make help
```

## Infrastructure Architecture

![Alt text](docs/infrastructure-architecture.png?raw=true "Infrastructure Architecture")
