FROM python:3.11
WORKDIR /usr/src/app

COPY requirements.txt ./

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic --noinput
RUN python3 manage.py makemigrations
