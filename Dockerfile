FROM ubuntu:22.04

# Installiere grundlegende Pakete
RUN apt-get update && apt-get install -y \
    git \
    curl \
    sudo \
    bash \
    python3 \
    python3-pip \
    && apt-get clean

# Optional: neuer User (damit nicht immer root verwendet wird)
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /workspaces

