FROM ubuntu:22.04

RUN apt update -y \
    && apt install -y python3 python3-dev python3-pip \
    && rm -rf /var/lib/apt/lists

WORKDIR /work
COPY pyproject.toml poetry.lock ./

RUN pip3 install -U pip \
    && pip3 install poetry \
    && poetry install

CMD ["/bin/bash"]
