# Instagram

## Dependencies
Following must be available locally:

* Python 3.6 - [Python 3.6 install here](https://www.python.org/downloads/)

This app ships with a Dockerfile that allows you to run Postgres within a Docker container. 
* [Docker CE install here](https://www.docker.com/community-edition#/download)

## Building the Microservice

* Create a Python Virtual Environment, using Python 3.6:
    * ```python3 -m venv ./venv```
* Activate your virtual environment and install dependencies:
    * Linux/Mac:
        * ```. ./venv/bin/activate```
        * ```pip3 install -r requirements.txt```
        
## Build and run the Postgres Dockerfile 

* From the root of the project:
    * ```docker build -t instagram-db ./devops/docker```
* You can now run the image (this will run Postgres in a docker container, with port 5432 mapped to localhost):
    * ```docker run --name instagram -d -p 5432:5432 instagram-db```
* Confirm the image is running successfully:
    * ```docker ps```
* If you want to remove the docker container:
    * ```docker kill $(docker ps -q) && docker rm instagram```
* If you want to access the docker container:
    * ```docker exec -it instagram psql -U postgres```


## Creating the DB
With everything now setup We use [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) to create the database from the migrations directory.

Create the database as follows:
```
python3 manage.py db upgrade
```

## Run Tests Locally
Run the bash script tests.sh:
```
./tests.sh
```
Please note that the test cases should be run before the seeding,
since the tests resets and rollback the DB after any change happened locally by the tests.

## Seeding the DB
Run the bash script seed_db.sh:
```
./seed_db.sh
```

## Running Locally
Finally we can run the application, as follows:

```
python3 manage.py runserver -d
```
