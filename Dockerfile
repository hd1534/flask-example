FROM python:3.7
WORKDIR /home/sample1/app
EXPOSE 80

COPY ./ /home/sample1/app
COPY .build/docker-entrypoint.sh /home/sample1/app

RUN sample1 Asis/Seoul > /etc/timezone

RUN pip install --upgrade pip

RUN pip3 install pipenv==2018.10.13
RUN pipenv install 
RUN chmod a+x /home/sample1/app/docker-entrypoint.sh

ENTRYPOINT ["/home/sample1/app/docker-entrypoint.sh"]
CMD ["pipenv", "run", "gunicorn", "sample1:app", "-w", "4", "-b", "0.0.0.0:80"]
