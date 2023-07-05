### BASE STAGE ###
ARG UBUNTU_VERSION
FROM ubuntu:${UBUNTU_VERSION} AS devcontainer_base
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Berlin \
    LANG=C.UTF-8
RUN echo $TZ > /etc/timezone \
    && apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    bash \
    ca-certificates \
    curl \
    file \
    git \
    git-lfs \
    gnupg \
    less \
    lsb-release \
    locales \
    make \
    nano \
    openssh-client \
    sudo \
    unzip \
    vim \
    wget \
    xz-utils \
    zip \
    zsh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### PYTHON STAGE ###
FROM devcontainer_base AS devcontainer_python
ARG CUSTOM_PYTHON_VERSION
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
RUN if [ ${CUSTOM_PYTHON_VERSION} == false ]; then \
    apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-venv \
    python3-wheel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    ;else \
    sed -i '/deb-src/s/^# //' /etc/apt/sources.list \
    && apt-get update \
    && apt-get build-dep -y python3 \
	&& apt-get install -y --no-install-recommends \
    build-essential \
    gdb \
    lcov \
    pkg-config \
    libbz2-dev \
    libffi-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline6-dev \
    libsqlite3-dev \
    libssl-dev \
    lzma \
    lzma-dev \
    tk-dev \
    uuid-dev \
    zlib1g-dev \
    && cd /usr/src \
    && wget https://www.python.org/ftp/python/${CUSTOM_PYTHON_VERSION}/Python-${CUSTOM_PYTHON_VERSION}.tgz \
    && tar xzf Python-${CUSTOM_PYTHON_VERSION}.tgz \
    && cd Python-${CUSTOM_PYTHON_VERSION} \
    && ./configure --with-lto --with-ensurepip=install \
    # TODO: Possibly enable optimizations
    # --enable-optimizations \
    && make -j \
    && make install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/src/* \
    && update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3 100 \
    && update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3 100 \
    && ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python$(echo ${CUSTOM_PYTHON_VERSION} | sed "s/..$//")/site-packages/lsb_release.py \
    ;fi
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 100 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 100


### DOCKER STAGE ###
FROM devcontainer_python AS devcontainer_docker
ARG DOCKER
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
RUN if [ ${DOCKER} == true ]; then \
    apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
    && mkdir -p /etc/apt/keyrings \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
	&& echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
         "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null\
	&& apt-get update\
	&& apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    ;fi

### CPP STAGE ###
FROM devcontainer_docker AS devcontainer_cpp
ARG GPP_VERSION
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
RUN if [ ${GPP_VERSION} != false ]; then \
    apt-get update && apt-get install -y --no-install-recommends \
    g++-${GPP_VERSION} \
    gcc-${GPP_VERSION} \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-${GPP_VERSION} 100 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-${GPP_VERSION} 100 \
    && update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-${GPP_VERSION} 100 \
    ;fi

### COMMON DEVELOPMENT TOOLS ###
FROM devcontainer_cpp AS devcontainer_utilities
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    cloc \
    cppcheck \
    direnv \
    doxygen \
    gdb \
    net-tools \
    nmap \
    shellcheck \
    shfmt\
    valgrind \
    iproute2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --ignore-installed \
    pytest \
    pytest-cases \
    pytest-cov \
    pylint \
    pylint-django \
    pre-commit \
    pip-licenses \
    pipdeptree \
    && pipdeptree -w fail
COPY ../tools/devtools/requirements.txt requirements.txt
RUN pip install --no-cache-dir --ignore-installed -r \
    requirements.txt \
    && pipdeptree -w fail \
    && rm -f requirements.txt
COPY ../tools/devtools/src/devtools/targets/django_app/requirements.txt requirements.txt
RUN pip install --no-cache-dir --ignore-installed -r \
    requirements.txt \
    && pipdeptree -w fail \
    && rm -f requirements.txt
COPY ../tools/devtools/src/devtools/targets/microservice/requirements.txt requirements.txt
RUN pip install --no-cache-dir --ignore-installed -r \
    requirements.txt \
    && pipdeptree -w fail \
    && rm -f requirements.txt

### FINAL STAGE ###
FROM devcontainer_utilities AS devcontainer
ARG USER
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
RUN useradd -s /bin/bash -U -m ${USER} && \
    echo ${USER} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER} && \
    chmod 0440 /etc/sudoers.d/${USER}
USER ${USER}
ENV USER_HOME=/home/${USER}
RUN mkdir -p ${USER_HOME}/.cache
RUN mkdir -p ${USER_HOME}/.config
RUN curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "/home/${USER}/powerlevel10k" \
    && git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git "${ZSH_CUSTOM:-"/home/${USER}/.oh-my-zsh/custom"}/plugins/zsh-syntax-highlighting" \
    && git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions "${ZSH_CUSTOM:-"/home/${USER}/.oh-my-zsh/custom"}/plugins/zsh-autosuggestions" \
    && "/home/${USER}/powerlevel10k/gitstatus/install"
RUN mkdir -p ${USER_HOME}/.local/share/fonts && cd ${USER_HOME}/.local/share/fonts \
    && curl -fLO https://github.com/ryanoasis/nerd-fonts/raw/HEAD/patched-fonts/DroidSansMono/DroidSansMNerdFont-Regular.otf
USER root
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8
COPY .devcontainer/.config/.zshrc \
    .devcontainer/.config/.p10k.zsh \
    ${USER_HOME}/
RUN mkdir -p ${USER_HOME}/.config/direnv/
RUN printf '[whitelist]\nprefix = [ "/workspace" ]\n' > ${USER_HOME}/.config/direnv/config.toml
RUN chown -R ${USER}:${USER} ${USER_HOME}
WORKDIR ${USER_HOME}
ENV USER=$USER
USER ${USER}
CMD ["/bin/bash"]
