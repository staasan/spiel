FROM python:3.14
WORKDIR /endspielbot
COPY . . 
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python","main.py"]
