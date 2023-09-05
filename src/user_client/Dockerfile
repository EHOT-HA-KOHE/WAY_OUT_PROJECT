FROM python:3.10
WORKDIR /WAY_OUT_PROJECT/src/user_client
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONPATH=/WAY_OUT_PROJECT
CMD ["python3", "user_client_main.py"]