FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get install -y \
		build-essential \
		git \
		libglib2.0-dev \
		libfdt-dev \
		libpixman-1-dev \
		zlib1g-dev \
		python3 \
	&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/espressif/qemu.git /source

WORKDIR /build
CMD git -C /source checkout 0ff3da8d3c797dcf33a45c419204f39f684376cf \
	&& /source/configure --target-list=xtensa-softmmu --enable-debug --enable-sanitizers --disable-strip --disable-user --disable-capstone --disable-vnc --disable-sdl --disable-gtk --static \
	&& make -j8
