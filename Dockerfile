FROM python:3.7-alpine
WORKDIR /webCamBackend
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]