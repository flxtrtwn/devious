# ABOUT

Development environment featuring a development command line application (tools/devious) to develop applications and configure remote machines for deployment.
Note: `devious` is developed in the context of this project and also available from PyPI.

Currently supports the following application types:

-   Microservice: Configures remote machine with nginx as reverse proxy, deploys microservice(s) as docker container(s).
-   DjangoApp: Docker compose deployment with nginx as reverse proxy

## USAGE

-   For usage as private repository, use the `devious update` command instead of syncing the fork, because it is not possible to fork privately due to git intrinsics.
    This detaches your repository from its remote (the `devious` repo), remove the `devious` development artifacts to facilitate integration of upstream changes (`devious` changes more rapidly and in a more complex way than the rest and should be fetched from PyPI instead) and leave the original devious remote configures as `devious_upstream`.
-   You can still get updates from the rest of the `devious` repo (excluding the `tools/devious` folder) with `devious update`.
-   (Optional) Configure devcontainer in .devcontainer/.env file (e.g. Python version).
-   Create your application with (see "dev create -h")
-   Register your applications in `registered_targets.py`.
-   Under some conditions (e.g. remote container without WSL2), the `initializeCommand.sh` must be executed manually on the target system for the first time
-   For remote containers via SSH, usage of `ssh-agent` is useful to cache your identities on a system
    -   Windows: `Get-Service ssh-agent | Set-Service -StartupType Automatic -PassThru | Start-Service`, `start-ssh-agent.cmd`, `ssh-add <private key>`
    -   Ubuntu: `ssh-agent`, `ssh-add <private key>`

## CONFIGURATION

Set configuration variables in .devcontainer/.env file:

-   DOCKER: true or false depending on if you want docker installed inside your devcontainer (docker in docker).
-   GPP_VERSION: false or g++ version (e.g. "11") to install C/C++ build tools (currently no supported application types in devious).
-   CUSTOM_PYTHON_VERSION: "default" for ubuntu distribution default or specific version (e.g. "3.10.6") to build from source.
-   UBUNTU_VERSION: Specific version (e.g. "22.04")

Set user aliases

-   Put custom user aliases in .devcontainer/.config/.user_aliases if needed
