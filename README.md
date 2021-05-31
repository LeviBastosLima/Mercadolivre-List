# Mercadolivre-List

Project for the test of real trends, which integrates the free market, returning the ten biggest sellers and the ten most expensive sales, together with OAuth.


## Heroku

Follow the link with the project on heroku: https://realtrends-test.herokuapp.com/


## Run Project

1 - After you have cloned the project, create an .env file and insert the environment variables found in the .env.example file

Example:

```
APP_ID=3092289227935085
SECRET_KEY=xWceHEsZwhEJr48i7IEgXKnD9mAZ03GA
FREE_MARKET_API_URL = https://api.mercadolibre.com/
FREE_MARKET_AUTH_URL = http://auth.mercadolibre.com.ar/
SECRET_KEY_DJANGO=@vr^&ew$i0p6r*nup76su(r8bo%0^$ug^86&lqk@#r@a!ee8t3
DEBUG=True
```

2 - If you do not have pipenv installed, run the following command
```
$ pip install pipenv
```

3 - With pipenv installed, run:

```
$ pipenv install
$ pipenv run python manage.py runserver
```
Pipenv will create a virtualenv and install all dependencies on it. The second command will start the python server.
