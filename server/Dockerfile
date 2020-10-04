FROM python:3.8
COPY server /

# Updating YAML Python package
RUN pip install -U PyYAML

RUN mkdir /config
ENTRYPOINT ["/bin/sh"]