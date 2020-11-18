#!/usr/bin/env bash

docker buildx build \
    --push \
    --platform linux/arm/v7,linux/amd64 \
    -t fergalmoran/bitchmin-web .
