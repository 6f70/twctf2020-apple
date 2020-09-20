FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get install -y \
		build-essential \
		git \
		wget \
		flex \
		bison \
		gperf \
		python3 \
		python3-pip \
		python3-setuptools \
		cmake \
		ninja-build \
		ccache \
		libffi-dev \
		libssl-dev \
		libusb-1.0-0 \
	&& rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# v3.3.3
WORKDIR /esp-idf
RUN git clone https://github.com/espressif/esp-idf.git . \
	&& git checkout 95c7b26cdde5aff5663b6e25363bb5ddefda4954 \
	&& git submodule update --init --recursive

RUN ./install.sh

COPY patch.diff /esp-idf
RUN patch -p0 < patch.diff

COPY source /source

WORKDIR /source
CMD bash -c '. /esp-idf/export.sh && idf.py build && ./make-flash-img.sh challenge flash_image.bin && cp flash_image.bin build'
