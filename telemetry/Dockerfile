FROM python:3.6
RUN mkdir /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
copy . /usr/src/app
CMD ["python", "api.py"]