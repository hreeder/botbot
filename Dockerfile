FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
# RUN pip install --no-cache-dir tornado==4.5.2
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python", "run.py"]
