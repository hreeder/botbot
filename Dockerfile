FROM python:3.6

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

# See https://stackoverflow.com/questions/46503947/how-to-get-pipenv-running-in-docker#49705601
RUN pip install pipenv \
  && pipenv install --deploy --system --ignore-pipfile

COPY . ./

EXPOSE 4434
CMD ["pipenv", "run", "python", "run.py"]
