# Gabe Pokedex!

![image](https://github.com/gabrielCavazos/pokedex/assets/65939447/17c3ecbb-95af-47d2-bd93-23570a358bdb)


Welcome to the Gabe Pokedex project! This project consists of a frontend and backend application running with Docker containers.

The project utilizes the PokeAPI to fetch information about all the current Pokémon and displays them in a table. You have the ability to add Pokémon to your favorites and view detailed information about each Pokémon.

The backend is build with Django and djangorestframework
The forntend is build with React


### Note 

I have tested the project on a Windows environment. However, I have not been able to test it on macOS or Linux. If you encounter any issues with the Docker image on those operating systems, please let me know. Unfortunately, I do not have access to devices running macOS or Linux for testing purposes. 

## Prerequisites

- Docker [https://www.docker.com/products/docker-desktop/]

## Getting Started

To get started with the project, follow the steps below:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. You can start and build all the project just running.

   ```shell
   docker-compose up --build
   ```
4. If the project is already build, just run :

   ```shell
   docker-compose up
   ```

### Accessing the Application

Once the backend and frontend containers are running, you can access the application in your web browser:

Frontend: http://localhost:3000
Backend: http://localhost:8000

   
### Backend

The backend application runs on port 8000.

1. Navigate to the `root` directory.
2. Access to the docker container shell

   ```shell
   docker-compose exec backend bash
   ```
3. The project run the migration by default but if is needed to run standalone run inside the backend bash 
Start the backend container:

    ```shell
    docker-compose exec backend bash
    python3 manage.py migrate
    ```


### Frontend

1. Navigate to the `root` directory.
2. Access to the docker container shell

   ```shell
   docker-compose exec frontend bash
   ```
3. The project dont have live reload (i tried but it doesnt works) so if is needed take down the frontend docker and start standalone


   ```shell
   docker-compose down frontend
   cd frontend
   npm install
   npm start
   ```

### Database
The database used is PostgreSQL and runs on port 5432.

Database Name: mydatabase
Username: myuser
Password: mypassword

1. Navigate to the `root` directory.
2. Access to the docker container shell

   ```shell
   docker-compose exec frontend bash
   ```

### Note about the approach

In this project, I have adopted an approach to optimize API calls to the PokeAPI and enhance the overall performance of the application. Instead of making frequent API calls to fetch information for each request, I store the necessary data in my local database. This strategy reduces the reliance on external API calls, especially considering factors such as potential API request limits or costs associated with each call.

By preloading and saving the required information in my database, I can simplify tasks such as pagination, querying Pokémon data, and managing favorites. This approach streamlines the application's functionality and ensures a smoother user experience.

While some sections of the code could potentially be replaced with serializers, I have chosen to handle data manipulation manually. This decision was made to accommodate the dynamic nature of the data and the fact that I do not synchronize all Pokémon data at once. The manual approach allows me to have more control and flexibility over the data management process.

The tradeoff is that the first time you visit a page will take a little longer to load because we are fetching the pokemon detail, but in the next time you visit it will be faster (this help thinking multimple users use the same application)

Another way to do it where to update the pokemons with a task every day for example but i wasnt want to go really deep and need to add celery or another tools in order to do it
