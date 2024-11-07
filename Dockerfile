FROM python:3.12.7-alpine3.20
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/BaiduPCS-Go
RUN chmod +x /app/entrypoint.sh
ENV BAIDUPCS_GO_CONFIG_DIR=/config
EXPOSE 5000

ENV APP_ENV=development
ENTRYPOINT ["./entrypoint.sh"]