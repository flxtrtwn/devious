# ABOUT

Devcontainer for VSCode in WSL2 environment.

## USAGE

-   Configure OS and tool versions for devcontainer in .devcontainer/.env file.

## CONFIGURATION

Set configuration variables in .devcontainer/.env file:

-   DOCKER: true or false depending on if you want docker installed in your devcontainer.
-   GPP_VERSION: false or g++ version (e.g. "11") to install C/C++ build tools.
-   CUSTOM_PYTHON_VERSION: "default" for ubuntu distribution default or specific version (e.g. "3.10.6") to build from source.
-   UBUNTU_VERSION: Specific version (e.g. "22.04")