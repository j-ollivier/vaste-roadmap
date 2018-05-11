# vaste-roadmap

## Overview
This repo is a django application developed on my free time to manage my different projects.
It's meant to be plugged on a django project.
Requirements : Python3

## Disclaimer
The app is viable but I am still working on it, I will add new functionalities ASAP.

## Installation
DL this repo in your django project
Add 'roadmap' to your INSTALLED_APPS variable in /<project-name>/settings.py

python3 manage.py makemigrations

python3 manage.py migrate

If you're working on production already (which you shouldn't mind you) you have to add this step :

python3 manage.py collecstatic