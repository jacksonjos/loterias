FROM python:3.6-alpine3.7

RUN apk -U add gcc libffi-dev python3-dev ca-certificates libxml2-dev \
        libxslt-dev musl-dev openssl-dev py-imaging py-pip curl \
  && update-ca-certificates \
  && rm -rf /var/cache/apk/* \
  && pip install --upgrade pip \
  && pip install Scrapy IPython

RUN mkdir -p /data

VOLUME /data

# WORKDIR /data

# COPY entrypoint.sh /runtime/entrypoint.sh
# RUN chmod +x /runtime/entrypoint.sh

# ENTRYPOINT ["/bin/sh"]

CMD ["/bin/sh"]
