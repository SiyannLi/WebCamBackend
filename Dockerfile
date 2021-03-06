FROM python:3.10-alpine
WORKDIR /webCamBackend
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]