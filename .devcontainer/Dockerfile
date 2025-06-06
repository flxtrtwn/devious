### BASE STAGE ###
ARG UBUNTU_VERSION
FROM ubuntu:${UBUNTU_VERSION} AS devcontainer_base
ARG USER
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
    gettext \
    git \
    git-lfs \
    gnupg \
    less \
    lsb-release \
    locales \
    make \
    nano \
    openssh-client \
    openssh-server \
    sudo \
    unzip \
    vim \
    wget \
    xz-utils \
    zip \
    zsh \
    x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -s /bin/bash -U -m ${USER} && \
    echo ${USER} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER} && \
    chmod 0440 /etc/sudoers.d/${USER}
USER ${USER}
ENV USER_HOME=/home/${USER}
RUN mkdir -p ${USER_HOME}/.cache
RUN mkdir -p ${USER_HOME}/.config
RUN chown -R ${USER}:${USER} ${USER_HOME}


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


### FLUTTER STAGE ###
FROM devcontainer_cpp as devcontainer_flutter
ARG USER
# Set environment variables used by the Android SDK
ENV ANDROID_SDK_HOME /home/$USER/android-sdk-linux
ENV ANDROID_SDK_ROOT /home/$USER/android-sdk-linux
ENV ANDROID_HOME /home/$USER/android-sdk-linux
ENV ANDROID_SDK /home/$USER/android-sdk-linux
ENV DEBIAN_FRONTEND noninteractive
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]

# COPY provisioning/docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
# COPY provisioning/ndkTests.sh /usr/local/bin/ndkTests.sh
# RUN chmod +x /usr/local/bin/*
# COPY provisioning/51-android.rules /etc/udev/rules.d/51-android.rules

#ENV JAVA_VERSION="8"
ENV ANDROID_TOOLS_URL="https://dl.google.com/android/repository/commandlinetools-linux-6858069_latest.zip"
ENV ANDROID_VERSION="29"
ENV ANDROID_BUILD_TOOLS_VERSION="29.0.3"
ENV ANDROID_ARCHITECTURE="x86_64"
#ENV FLUTTER_WEB_PORT="8090"
#ENV FLUTTER_DEBUG_PORT="42000"
#ENV FLUTTER_EMULATOR_NAME="flutter_emulator"
ENV PATH="$ANDROID_SDK_ROOT/cmdline-tools/tools/bin:$ANDROID_SDK_ROOT/emulator:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/platforms:$PATH"

# install all dependencies
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update \
  && apt-get install --yes --no-install-recommends openjdk-17-jdk curl unzip sed git bash xz-utils libglvnd0 ssh xauth x11-xserver-utils libpulse0 libxcomposite1 libgl1-mesa-glx sudo libgtk-3-dev pkg-config \
  && rm -rf /var/lib/apt/lists/*

USER $USER
# android sdk
RUN mkdir -p $ANDROID_SDK_ROOT \
  && mkdir -p $ANDROID_SDK_ROOT/.android \
  && touch $ANDROID_SDK_ROOT/.android/repositories.cfg \
  && curl -o $ANDROID_SDK_ROOT/android_tools.zip $ANDROID_TOOLS_URL \
  && unzip -qq -d "$ANDROID_SDK_ROOT" $ANDROID_SDK_ROOT/android_tools.zip \
  && rm $ANDROID_SDK_ROOT/android_tools.zip \
  && mkdir -p $ANDROID_SDK_ROOT/cmdline-tools/tools \
  && mv $ANDROID_SDK_ROOT/cmdline-tools/bin $ANDROID_SDK_ROOT/cmdline-tools/tools \
  && mv $ANDROID_SDK_ROOT/cmdline-tools/lib $ANDROID_SDK_ROOT/cmdline-tools/tools \
  && echo y | sdkmanager "build-tools;$ANDROID_BUILD_TOOLS_VERSION" \
  && echo y | sdkmanager "platforms;android-$ANDROID_VERSION" \
  && echo y | sdkmanager "platform-tools" \
  && echo y | sdkmanager "emulator" \
  && echo y | sdkmanager "system-images;android-$ANDROID_VERSION;google_apis_playstore;$ANDROID_ARCHITECTURE" \
  && echo y | sdkmanager "cmdline-tools;latest"

USER root
# android dev dependencies
RUN apt-get update \
  && apt-get install --yes --no-install-recommends clang cmake ninja-build \
  && rm -rf /var/lib/apt/lists/*

USER $USER
# Install Flutter
ARG FLUTTER_VERSION=3.19.0
ARG FLUTTER_URL=https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz
ENV FLUTTER_HOME="/home/$USER/flutter"
ENV PATH="$FLUTTER_HOME/bin:$PATH"
RUN mkdir -p $FLUTTER_HOME \
  && curl -o $FLUTTER_HOME/flutter.tar.xz $FLUTTER_URL \
  && tar xf $FLUTTER_HOME/flutter.tar.xz -C /home/$USER \
  && rm $FLUTTER_HOME/flutter.tar.xz
RUN flutter config --no-analytics \
  && flutter precache \
  && yes | flutter doctor --android-licenses || test $? -eq 141 \
  && flutter doctor \
  && flutter emulators --create \
  && flutter update-packages

#COPY entrypoint.sh /usr/local/bin/
#COPY chown.sh /usr/local/bin/
#COPY flutter-android-emulator.sh /usr/local/bin/flutter-android-emulator
#ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

USER root
#Android Studio
ARG ANDROID_STUDIO_ROOT="/opt/android-studio"
RUN sudo dpkg --add-architecture i386 \
    && sudo apt-get update \
    && sudo apt-get upgrade --yes
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    libc6:i386 \
    libncurses5:i386 \
    libstdc++6:i386 lib32z1 \
    libbz2-1.0:i386 \
    # Android Studio
    build-essential git neovim wget unzip sudo \
        libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386 \
        libxrender1 libxtst6 libxi6 libfreetype6 libxft2 xz-utils vim \
        qemu qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils libnotify4 libglu1 libqt5widgets5 openjdk-8-jdk openjdk-11-jdk openjdk-17-jdk xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# RUN groupadd -g 1000 -r ${USER}
RUN adduser ${USER} libvirt
RUN adduser ${USER} kvm
RUN usermod -aG plugdev ${USER}
RUN mkdir -p $ANDROID_STUDIO_ROOT
RUN mkdir -p $ANDROID_STUDIO_ROOT/Android/Sdk
RUN mkdir -p $ANDROID_STUDIO_ROOT/profile/android

ARG ANDROID_STUDIO_VERSION=2023.2.1.24
ARG ANDROID_STUDIO_URL=https://r1---sn-h0jeenld.gvt1.com/edgedl/android/studio/ide-zips/${ANDROID_STUDIO_VERSION}/android-studio-${ANDROID_STUDIO_VERSION}-linux.tar.gz
RUN wget "$ANDROID_STUDIO_URL" -O android-studio.tar.gz && tar xzvf android-studio.tar.gz -C $ANDROID_STUDIO_ROOT && rm android-studio.tar.gz
RUN chown ${USER}:${USER} $ANDROID_STUDIO_ROOT
ENV ANDROID_EMULATOR_USE_SYSTEM_LIBS=1


### COMMON DEVELOPMENT TOOLS ###
FROM devcontainer_flutter AS devcontainer
ARG USER
USER root
SHELL ["/bin/bash", "-euco", "pipefail"]
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    cloc \
    cppcheck \
    direnv \
    doxygen \
    gdb \
    gh \
    iproute2 \
    net-tools \
    nmap \
    shellcheck \
    shfmt \
    valgrind \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER ${USER}
RUN curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "/home/${USER}/powerlevel10k" \
    && git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git "${ZSH_CUSTOM:-"/home/${USER}/.oh-my-zsh/custom"}/plugins/zsh-syntax-highlighting" \
    && git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions "${ZSH_CUSTOM:-"/home/${USER}/.oh-my-zsh/custom"}/plugins/zsh-autosuggestions" \
    && "/home/${USER}/powerlevel10k/gitstatus/install"
RUN mkdir -p ${USER_HOME}/.local/share/fonts && cd ${USER_HOME}/.local/share/fonts \
    && curl -fLO https://github.com/ryanoasis/nerd-fonts/raw/HEAD/patched-fonts/DroidSansMono/DroidSansMNerdFont-Regular.otf
ENV PATH=$PATH:${USER_HOME}/.local/bin
RUN curl -sSL https://install.python-poetry.org | python -
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
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
