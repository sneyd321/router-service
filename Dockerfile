FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=$PORT


COPY . .

#CMD ["python", "./main.py"]
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
