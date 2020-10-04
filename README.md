# social_media

This is a repository for a web application developed with Django.

### API documentation

API documentation can be found following these links

```shell script
# Redoc documentation
<api_url>/docs
```

## Test environment

* Use `coverage` to measure test coverage. This can be integrated with your PyCharm IDE

# Development

Following are instructions on setting up your development environment.

The recommended way for running the project locally and for development is using Docker.

It's possible to also run the project without Docker.

1. Install Docker:
   - Linux - [get.docker.com](https://get.docker.com/)
   - Windows or MacOS - [Docker Desktop](https://www.docker.com/products/docker-desktop)
1. Clone this repo and `https://github.com/fastik17/social_media`

1. Use `.env.example` to create `.env`:
   ```sh
   $ cp .env.example .env
   ```
1. Start up the containers:

   ```sh
   $ docker-compose-dev up
   ```
  
   This will build the necessary containers and start them, including the web server on the host and port you specified in `.env`.

   Current (project) directroy will be mapped with the container meaning any edits you make will be picked up by the container.

1. Seed the Postgres DB (in a separate terminal):
   ```sh
   $ docker-compose-dev exec web python3 manage.py makemigrations
   $ docker-compose-dev exec web python3 manage.py migrate
   ```
1. Create a superuser if required:
   ```sh
   $ docker-compose-dev exec web python3 manage.py createsuperuser
   ```
   You will find an activation link in the server log output.
   

## Local Setup (Alternative to Docker)

1. [Postgresql](https://www.postgresql.org/download/)
2. [Python](https://www.python.org/downloads/release/python-385/)

### Installation


1. Clone this repo and `https://github.com/fastik17/social_media`
2. Run `pipenv install` to get all packages.
3. Run `cp .env.example .env`
4. Update .env file `DATABASE_URL` with your `database_name`, `database_user`, `database_password`, if you use postgresql.
   Can alternatively set it to `sqlite:////tmp/my-tmp-sqlite.db`, if you want to use sqlite for local development.

### Getting Started

1. Run `python manage.py makemigrations`
2. Run `python manage.py migrate`
3. Run `python manage.py createsuperuser`
4. Run `python manage.py runserver`
