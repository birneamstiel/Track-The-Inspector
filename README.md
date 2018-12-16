# Track the Inspector
<img width="1042" alt="screen shot 2018-12-16 at 02 00 49" src="https://user-images.githubusercontent.com/5410949/50050968-8b34b780-00d6-11e9-85ab-107b8a074161.png">

## Setup

first, make sure you have pipenv isntalled (`brew install pipenv` if on MacOS) or have a look [here](https://docs.pipenv.org/install/) and clone the repo

### Running the backend locally
``` bash
cd Track-The-Inspector/
pipenv install
export FLASK_APP=server.py
pipenv run flask run 
```

### Installing the telegram bot locally

`cd Track-The-Inspector/bot/src` 

`pipenv install`

afterwards, create a `.env` file in the `src` directory to store the telegram api key: `echo TELEGRAM_API_KEY=<your api key> > .env`

run the bot using `pipenv run python bot.py`
