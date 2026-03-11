FROM python:3.14
WORKDIR /Spiel
COPY . . 
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "Spiel.wsgi:application", "--bind", "0.0.0.0:8000"]
