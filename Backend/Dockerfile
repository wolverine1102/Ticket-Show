FROM python:3.9.10-alpine3.14
WORKDIR /home/Ticket-Show/Backend
ADD . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]