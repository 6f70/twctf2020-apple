#!/bin/sh
set -e

cd $(dirname "$0")

mkdir -p build
echo "Running 'docker build'......"
IMAGEID=$(docker build -q .)
echo "Running 'docker run'......"
docker run -v "${PWD}/build":/source/build --rm -it "${IMAGEID}"
#docker image rm "${IMAGEID}"
