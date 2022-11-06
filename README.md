# Verb games support bot
This bot created as a first level techical support.

## How to install
clone repo, get in root dir:
```sh
git clone https://github.com/ilyashirko/verb_games_support_bot && cd verb_games_support_bot
```
create virtual environment and install dependencies (you need poetry 1.2.0 and python 3.8)
```sh
python3 -m venv env
```
create [service account](https://console.cloud.google.com/apis/credentials) and put generated credential keys into `credential.json` (you can see example in `credential.json.example)