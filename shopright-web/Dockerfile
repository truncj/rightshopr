FROM python:3.7-stretch

ADD web.py requirements.txt ./
RUN pip install -r requirements.txt
#CMD [ "python", "-u", "web.py"]
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "web:app", "--bind", "0.0.0.0:5000"]
