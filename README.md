# Marvel Impossible Travel
[Igor Santos Brito](https://www.linkedin.com/in/igor-brito-916a60b1/)

## Requirements
* Python 3.8
* make package (You must be able to execute make command, you can install the package at windows, linux or mac.)
* Docker Compose version v2.19.1

## Configure the Enviroment
At the root directory of the project

Copy the content of the .env.example to a new file called .env inside the directory the path must be:
```
/marvel_populate_heros/code/.env
```
The database connection variables are the ones used at the local container.

Go to [Marvel`s Developer Portal](https://developer.marvel.com/) to get your API keys (PUBLIC_KEY, PRIVATE_KEY) and place the values at the .env file.

At the root directory of the project:

Create the local virtual environment, activate it and install python requirements from requeriments.tct
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Create the task container
```
$ make docker_build_task
```
initiate the MySQL container
```
$ make run_database
```
Create tables at the database
```
$ make docker_create_database_tables
```

## Execute the task
The MySQL database must be running, if it is not run:
```
$ make run_database
```

Run the task to populate the database
```
$ make run_task
```
## Custom Command
At the code directory we have the run_custom.py file. Here we can't add any code to query database data, to analyse the data information.

To run this file at the container execute the following at the root directory:
```
$ make run_custom
```
