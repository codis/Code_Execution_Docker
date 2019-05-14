FROM python:3-alpine

RUN pip3 install rq-dashboard

COPY . /dashboard
WORKDIR /dashboard

EXPOSE 9181

CMD ["rq-dashboard"]