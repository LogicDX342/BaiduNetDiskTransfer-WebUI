FROM python:3.12.7-alpine3.20
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/BaiduPCS-Go
ENV BAIDUPCS_GO_CONFIG_DIR=/config
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]