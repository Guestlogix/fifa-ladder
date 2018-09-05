 ## Getting Started

Ensure pipenv is installed
```
brew install pipenv
```

Install requirements
```
pipenv install
```

Init Database
```
pipenv run python ./app/manage.py db init
```

Make the migrates
```
pipenv run python ./app/manage.py db migrate
```

Migrate
```
pipenv run python ./app/manage.py db upgrade
```

Run the server
````
pipenv run python ./app/manage.py runserver
```

## Deployment

Ensure Heroku cli
```
brew install heroku/brew/heroku
```

Create Heroku app
```
heroku create
```

Push to deploy
```
git push heroku master
```