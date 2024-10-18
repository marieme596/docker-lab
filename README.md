# Simple doctor API
This is a Flask-backend API for managing doctor infos.

MySQL is the database used to communicate with the API and to do the following requests :
- add a doctor (POST request)
- get his/her informations (first name, last name, specialty, experience years and contact number of the doctor)
- get all doctors with their infos
- update doctor information except of the specialty
- suppress a doctor
- 
When running the API, a table named `doctors` is automatically created whatever request you send.

## How to run the application with Docker ?
You can either pull the Docker image `marieme27/flask-app:v3.0.0` from Docker Hub or build it locally.

Create a network with the command :
```
docker network create my-network
```
Then, run MySQL docker image :
```
docker run -d -p 27017:27017 --name database \
--net my-network \
-e MYSQL_ROOT_PASSWORD=root \
-e MYSQL_DATABASE=my_db \
mysql:<tag>
```
For next steps, it will depend on the method you choose to run the app.

### Running the app using Docker Hub Image

```
docker run -d -p 5000:5000 --name flask-app \
--net my-network \
-e MYSQL_HOST=database \
-e DATABASE_PORT=27017 \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=root \
marieme27/flask-app:v3.0.0
```
Do not use previous versions of the app image. There were some issues, fixed on the third version.

### Run the app locally

First, clone the github projet :
```
git clone https://github.com/marieme596/docker-lab.git
cd docker-lab
```

```
docker build -t flask-app .
```

```
docker run -d -p 5000:5000 --name flask-app \
--net my-network \
-e MYSQL_HOST=database \
-e DATABASE_PORT=27017 \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=root \
flask-app:latest
```

## How to run the application with Docker-compose ?

### With Docker Hub Image
You have to clone the project and be in docker-lab directory before running the following command :

```
docker-compose up
```

### With local flask-app
In this case, after cloning the project and changing directory you have to modify `docker-compose.yml` file.

On flask-app service replace these 3 lines :

```
image: marieme27/flask-app:v3.0.0
restart: unless-stopped
container_name: flask-app 
```

By this line which indicates to the docker-compose file to build the app with Dockerfile located on the same directory :

```
build: .
```
After that you can use the same command :

```
docker-compose up
```

To stop docker-compose, it is very easy :

```
docker-compose down 
```

This command will delete all containers and networks.
