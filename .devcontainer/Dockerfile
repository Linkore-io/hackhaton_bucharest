FROM mcr.microsoft.com/devcontainers/base:jammy

RUN apt-get update

RUN usermod -a -G sudo vscode

RUN apt-get install -y \
    bear \
    ^clang.*15.* \
    ^llvm.*15.* \
    ^llvm.*15.* \
    cmake \
    mono-complete