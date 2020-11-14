#!/usr/bin/env bash

docker buildx build \
    --push \
    --platform linux/arm/v7 \
    -t fergalmoran/bitchmin-api .
