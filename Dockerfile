FROM joyzoursky/python-chromedriver:3.7-alpine3.8

ADD check.py utils.py authy.py requirements.txt ./
RUN pip install -r requirements.txt
CMD [ "python", "-u", "check.py"]

