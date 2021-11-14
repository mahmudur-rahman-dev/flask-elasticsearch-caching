FROM python:3.8-slim-buster

WORKDIR /app
EXPOSE 5005
COPY . .
COPY .env .env
#COPY requirements.txt requirements.txt
RUN pip3 install elasticsearch[async]>=7.8.0
RUN pip3 install -r requirements.txt

RUN export FLASK_APP=APP

#CMD ["gunicorn", "-w", "4","--timeout","500","-b","0.0.0.0:5005", "src.routes:createApp()"]
# CMD ["gunicorn", "-w", "4","-b","0.0.0.0:5005", "src.routes:createApp()"]
CMD ["python3" ,"-m","flask", "run", "--host=0.0.0.0","--port=5005"]
# CMD ["gunicorn", "-w", "4","--timeout","500","-b","0.0.0.0:5005", "src.routes:createApp()"]
