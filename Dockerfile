FROM ubuntu:bionic

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update       \
  && apt-get install -y  \
    wget \
    openjdk-8-jre \
    vim \
  && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

ENV HOME=/home/root
RUN conda create -n py38 python=3.8
RUN activate py38
COPY . /home/root/EvoCraft-py
WORKDIR /home/root/EvoCraft-py
RUN python -m pip install -r requirements.txt

# gets eula but fails. change to true
RUN java -jar spongevanilla-1.12.2-7.3.0.jar
RUN python edit_file.py --file_path=eula.txt