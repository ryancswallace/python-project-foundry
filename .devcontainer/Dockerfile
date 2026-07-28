# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.14
ARG DEBIAN_VERSION=bookworm
ARG UV_VERSION=0.11.23

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-bin

FROM mcr.microsoft.com/devcontainers/python:${PYTHON_VERSION}-${DEBIAN_VERSION}

ARG DEBIAN_FRONTEND=noninteractive

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy

# Node is installed by a devcontainer feature, so a preconfigured Yarn APT
# source is unnecessary and can make apt updates fail if its key is stale.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        bubblewrap \
        build-essential \
        ca-certificates \
        curl \
        git \
        jq \
        less \
        make \
        openssh-client \
        procps \
        ripgrep \
        shellcheck \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv-bin /uv /uvx /usr/local/bin/
