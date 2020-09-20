#!/bin/sh
set -e

cd $(dirname "$0")

mkdir build
IMAGEID=$(docker build -q .)
docker run -v "${PWD}/build":/build --rm -it "${IMAGEID}"
docker image rm "${IMAGEID}"
