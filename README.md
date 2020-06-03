## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Launch](#launch)

## General info
This is the repository of blog app's api. This project allow you to create simple blog with posts and comments.

## Technologies
Project is created with:
* [django](https://www.djangoproject.com)
* [django rest framework](https://www.django-rest-framework.org)
* [pipenv](https://github.com/pypa/pipenv)
* [postgresql as DB Engine](https://www.postgresql.org)
* [docker](https://www.docker.com)

#Launch
[Pipenv](https://github.com/pypa/pipenv) is a package-manager tool of the project.


1. Create appropriate directory for the project and inside generate virtual environment

'''
$ cd ../project_directory
$ pipenv --python 3.8
'''


2. Activate virtual environment, clone repository to your local machine and install depedencies from Pipfile.lock

'''
$ pipenv shell
$ git clone https://github.com/adamjanas/blog_api.git
$ pipenv install
'''


3. If you need help or more informations about pipenv, run:

'''
$ pipenv --help
'''