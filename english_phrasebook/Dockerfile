# pull official base image
FROM python:3.7.3-alpine

# set work directory
WORKDIR /usr/src/english_phrasebook

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # and Pillow dependencies
     jpeg-dev zlib-dev \
    # and magic dependencies
     libmagic

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/english_phrasebook/entrypoint.sh"]