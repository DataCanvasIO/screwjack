# {{ Name }}

# VERSION : {{ Version }}

FROM {{ BaseImage }}
# MAINTAINER Your_name, Your_email_address

RUN apt-get install -y python-simplejson

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
