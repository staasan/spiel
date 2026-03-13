FROM python:3.14
WORKDIR /backend
COPY . . 
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8000
RUN chmod +x ./entry.sh
ENTRYPOINT ["./entry.sh"]
CMD ["gunicorn", "Spiel.wsgi:application", "--bind", "0.0.0.0:8000"]
