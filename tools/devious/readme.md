# What is Devious?

Devious is a command line utility to manage the lifecycle of applications in a mono repository.
It is developed in the context of a VSCode-based development container template (see [devious](https://github.com/flxtrtwn/devious)).

# What can I do with Devious?

-   `create`, `build`, `test`, `debug` applications locally
-   `deploy`, `run` and `stop` applications (e.g. on remote machines)
-   Manage remote machines and `install` infrastructure

# What kind of applications does Devious support?

Devious features an extensible target model and can provide functionality for any application type that implements the `Target` interface.
It currently supports `microservice` and `django_app` targets and can manage their lifecycle.
