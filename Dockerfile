# Reproduction package for the article TODO,
# by Mohamed-Amine Baazizi, Dario Colazzo, Giorgio Ghelli, Carlo Sartiani, and Stefanie Scherzinger.
#
# Copyright 2021, Stefan Klessinger <stefan.klessinger@uni-passau.de>
# SPDX-License-Identifier: GPL-3.0

FROM ubuntu:20.04

MAINTAINER Stefan Klessinger <stefan.klessinger@uni-passau.de>

ENV DEBIAN_FRONTEND noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"

# Install packages for experiments
RUN apt-get update && apt-get install -y --no-install-recommends \
		fonts-liberation \
		git \
		maven \
		openjdk-11-jdk \
		openjdk-11-jre \
		pip \
		python3

# Install dev packages
RUN apt-get install -y --no-install-recommends \
		nano \
		sudo

# Add user
RUN useradd -m -G sudo -s /bin/bash repro && echo "repro:repro" | chpasswd
RUN usermod -a -G staff repro
USER repro
WORKDIR /home/repro

# Add artifacts directory (from host) to home directory
COPY --chown=repro:repro artifacts/ /home/repro
RUN chmod +x *.sh && chmod +x scripts/*.sh && chmod +x charts/evaluate.py
RUN pip install -r charts/requirements.txt
