#!/usr/bin/env bash

# docker build --no-cache -t fergalmoran/bitchns .
    # --platform linux/arm/v7,linux/amd64 \

docker buildx build \
    --push \
    --platform linux/arm/v7,linux/amd64 \
    -t fergalmoran/bitchmin-web .
