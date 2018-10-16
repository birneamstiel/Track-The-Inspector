Track the Inspector
==============================================

Installation
------------
first, make sure you have pipenv isntalled (`brew install pipenv` if on MacOS) or have a look [here](https://docs.pipenv.org/install/)

clone the repo

`cd Track-The-Inspector/bot/src` 

`pipenv install`

afterwards, create a `.env` file in the `src` directory to store the telegram api key: `echo TELEGRAM_API_KEY=<your api key> > .env`

run the bot using `pipenv run python bot.py`
