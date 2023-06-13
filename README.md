# ABOUT

Development environment featuring convenient tools (tools/devtools) exposed as a command line application to develop applications and configure remote machines for deployment.

Currently supports the following application types:

-   Microservice (configures remote machine with nginx as reverse proxy, deploys microservice(s) as docker container(s))
-   DjangoApp (docker compose, nginx as reverse proxy)

## USAGE

-   If you want to use this for private repositories and still sync with this upstream (public) repository, refer to
-   (Optional) Configure devcontainer in .devcontainer/.env file (e.g. Python version).
-   Create your application with (see "dev create -h")
-   Register your application in tools/devtools/src/devtools/registered_targets.py (TODO: Possibly automate with user input.)

## CONFIGURATION

Set configuration variables in .devcontainer/.env file:

-   DOCKER: true or false depending on if you want docker installed inside your devcontainer (docker in docker).
-   GPP_VERSION: false or g++ version (e.g. "11") to install C/C++ build tools (currently no supported application types in devtools).
-   CUSTOM_PYTHON_VERSION: "default" for ubuntu distribution default or specific version (e.g. "3.10.6") to build from source.
-   UBUNTU_VERSION: Specific version (e.g. "22.04")

Set user aliases

-   Put custom user aliases in .devcontainer/.config/.user_aliases if needed
