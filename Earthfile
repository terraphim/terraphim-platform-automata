VERSION 0.7
PROJECT applied-knowledge-systems/terraphim-cloud-dependencies
FROM ghcr.io/applied-knowledge-systems/redis-stack:bionic

build-automata:
    ENV DEBIAN_FRONTEND noninteractive
    ENV DEBCONF_NONINTERACTIVE_SEEN true
    RUN apt-get update && apt-get install -yqq --no-install-recommends build-essential git ca-certificates curl gnupg
    RUN update-ca-certificates
    RUN apt-get install -yqq --no-install-recommends software-properties-common
    RUN add-apt-repository ppa:deadsnakes/ppa -y
    RUN apt update && apt install -yqq --no-install-recommends python3.9 python3-pip python3-setuptools python3.9-dev python3.9-venv
    RUN pip3 install wheel
    WORKDIR /code
    GIT CLONE git@github.com:terraphim/terraphim-platform-automata.git terraphim-platform-automata
    COPY proprietary/* terraphim-platform-automata
    RUN python3.9 -m venv /code/venv_terraphim
    RUN /bin/bash -c "source /code/venv_terraphim/bin/activate && pip3 install -r terraphim-platform-automata/requirements.txt"
    WORKDIR /code/terraphim-platform-automata
    RUN mkdir ./automata
    RUN /bin/bash -c "source /code/venv_terraphim/bin/activate && python3 parse_wand_taxonomy_to_automata.py"
    SAVE ARTIFACT automata AS LOCAL automata