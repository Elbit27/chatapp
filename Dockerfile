FROM python:3.12.3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN chmod 755 .
RUN  chown -R www-data:www-data /home/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

COPY . .

