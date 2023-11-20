# ABOUT

Development environment featuring convenient tools (tools/devious) exposed as a command line application to develop applications and configure remote machines for deployment.

Currently supports the following application types:

-   Microservice (configures remote machine with nginx as reverse proxy, deploys microservice(s) as docker container(s))
-   DjangoApp (docker compose, nginx as reverse proxy)

## USAGE

-   For usage as private repository, use the `dev update` command instead of syncing the fork (it's not possible to fork privately).
-   (Optional) Configure devcontainer in .devcontainer/.env file (e.g. Python version).
-   Create your application with (see "dev create -h")
-   Register your application in tools/devious/src/devious/registered_targets.py (TODO: Possibly automate with user input.)
-   Under some conditions (e.g. remote container without WSL2), the `initializeCommand.sh` must be executed manually on the target system for the first time
-   For remote containers via SSH, usage of `ssh-agent` is useful to cache your identities on a system
    -   Windows: `Get-Service ssh-agent | Set-Service -StartupType Automatic -PassThru | Start-Service`, `start-ssh-agent.cmd`, `ssh-add`

## CONFIGURATION

Set configuration variables in .devcontainer/.env file:

-   DOCKER: true or false depending on if you want docker installed inside your devcontainer (docker in docker).
-   GPP_VERSION: false or g++ version (e.g. "11") to install C/C++ build tools (currently no supported application types in devious).
-   CUSTOM_PYTHON_VERSION: "default" for ubuntu distribution default or specific version (e.g. "3.10.6") to build from source.
-   UBUNTU_VERSION: Specific version (e.g. "22.04")

Set user aliases

-   Put custom user aliases in .devcontainer/.config/.user_aliases if needed
