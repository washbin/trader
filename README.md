# Trader

A stock trading simulation app created using python flask framework<br>

<!-- ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/washbin/trader/Python%20application) -->

# Running Yourself

> You could do both development and deployment without docker but this readme doesn't cover that part as of now.

- Make sure you have docker and docker-compose installed.
- If you do not have docker, you could follow the instructions at [Getting started with docker](https://www.docker.com/get-started)
- Create a .env file at the root of project directory with your secrets, \
  following the template.env structure and source it.
  > - The API_KEY could be obtained from [IEX Cloud](https://www.iexcloud.io/)<br>
  > - View info about SECRET_KEY at [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY)<br>
  > - DATABASE_URL as the name suggests just points to your database \
    > For development you could use something simple like `DATABASE_URL="sqlite:///local.db"`, \
    > For production you will likely define it in docker-compose file in compose_production directory

## Development

1. Change directory into the main_app directory
2. Do a `docker-compose up -d`
3. Your site should now be served at port 5000 and reflect any changes you make to the code.

## Deployment

> You may want to make some changes in nginx configuration and \
> hide postgres credintials from compose_production/docker-compose.yml file.

1. Change directory into the compose_prduction directory
2. Do a `docker-compose -f docker-compose.yml up -d`
3. Your site should now be served at port 80 in your ip.

# Acknowledgments

> This project is basically a clone of [CS50's finance project](https://finance.cs50.net/)

# License

Licensed under the [MIT License](./LICENSE).
