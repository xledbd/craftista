FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["gunicorn"]
CMD ["app:app", "--bind", "0.0.0.0:5000"]
EXPOSE 5000