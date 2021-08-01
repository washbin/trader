# Trader

A stock trading simulation app created using python flask framework<br>

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/washbin/trader/Python%20application)

# Running Yourself

> You could do both development and deployment without docker but this readme doesn't cover that part as of now.

- Make sure you have docker and docker-compose installed.
- If you do not have docker, you could follow the instructions at [Getting started with docker](https://www.docker.com/get-started)
- Create a .env file with your secrets, following the template.env structure
  > - The API_KEY could be obtained from [IEX Cloud](https://www.iexcloud.io/)<br>
  > - View info about SECRET_KEY at [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY)<br>
  > - DATABASE_URL as the name suggests just points to your database, for development you could use something simple like `DATABASE_URL="sqlite:///local.db"`

### Initializing database

During first run of both development and deployment part, follow these after step 1

- Locate the flask container by doing `docker ps -a` <br>
  > The container is likely named `trader_flask-app_1` <br>
- Do a `docker exec -it {your container name} /bin/bash` <br>
  > You should be inside the container shell now so type
- ```sh
    export FLASK_APP=run.py
    flask shell
  ```

  > You should be prompted at a python REPL now

- ```py
    from trader import db
    db.create_all()
    exit()
  ```

  > Now the database initialization phase is complete so type exit to exit out of container shell and go back into your host shell

## Development

1. Do a `docker-compose up -d`
2. Your site should now be served at port 5000 and reflect any changes you make to the code.

## Deployment

> You may want to make some changes in nginx configuration and hide postgres credintials from docker-compose-prod.yml file.

1. Do a `docker-compose -f docker-compose-prod.yml up -d`
2. Your site should now be served at port 80 in your ip.

# Acknowledgments

> This project is basically a clone of [CS50's finance project](https://finance.cs50.net/)

# License

Licensed under the [MIT License](./LICENSE).