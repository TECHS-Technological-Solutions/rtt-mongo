FROM python:3.9-buster

ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

ADD . /opt/app
RUN pip install pipenv

WORKDIR /opt/app/src

# https://pipenv.kennethreitz.org/en/latest/basics/#pipenv-install
RUN pipenv install --deploy --dev --ignore-pipfile