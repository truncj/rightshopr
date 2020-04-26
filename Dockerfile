FROM python:3.7
ADD check.py requirements.txt cookie.txt stores.json  ./
RUN pip install -r requirements.txt
CMD [ "python", "-u", "check.py"]

