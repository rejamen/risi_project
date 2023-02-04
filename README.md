# Risi Project
The goal of this project is to create a basic CRUD for users, using Flask, SQLALchemy and other technologies.

# How to use it?
* Clone this repo 
* Create an .env file in the project folder to store some credentials:
```
# /risi_project/.env file content
POSTGRES_USER=<your_db_user>
POSTGRES_PASSWORD=<your_db_password>
POSTGRES_DB=<your_db_name>
```
* Run the following command
```
docker compose up
```
* When it's done you can go to your app on `http://localhost:5001`

# Troubleshooting
* If the port `5001` is used in your computer. You can change the port on the `docker-compose.yml` file in the section: 
```
web:
    build: .
    ports:
      - "5001:5000"
```