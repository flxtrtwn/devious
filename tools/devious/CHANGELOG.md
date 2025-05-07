# 0.16.0 (2025-01-19)

## Feat

-   Test deployment (e.g., test cert)

# 0.15.0 (2025-01-19)

## Feat

-   (webapp) Generic deployment

# 0.13.1 (2025-01-19)

## Fix

-   (webapp) Full debug mode as flag

# 0.13.0 (2025-01-19)

## Feat

-   (webapp) Full debug mode with docker compose

# 0.12.3 (2025-01-12)

## Fix

-   (webapp, django-app) Let gunicorn listen to locations outside of the container

# 0.12.2 (2025-01-12)

## Fix

-   (webapp) Expose only application port

# 0.12.1 (2025-01-11)

## Fix

-   Fix Docker compose build in webapp target

# 0.12.0 (2025-01-03)

## Feat

-   Docker compose build in webapp target

# 0.11.0 (2024-12-31)

## Feat

-   New Webapp target

# 0.10.2 (2024-12-27)

## Fix

-   Allow SSH agent; avoid unusability for more than one key present

# 0.10.1 (2024-12-21)

## Fix

-   Not copy over not existing requirements.txt in microservices

# 0.10.0 (2024-12-20)

# Feat

-   Install apps in microservices

## Fix

-   Copy over app dir before trying to modify nginxconfig in microservices

# 0.9.1 (2024-12-20)

## Fix

-   Dockerfile template for Microservice contained unescaped "$"

# 0.9.0 (2024-11-9)

## Feat

-   Always pull latest dependencies

# 0.8.1 (2024-11-9)

## Bugfix

-   (django-app) Create superuser for test db on app creation, not on app debug

# 0.8.0 (2024-11-9)

## Features

-   (django-app) Create superuser for test db on app creation

# 0.7.0 (2024-11-9)

## Features

-   Improvements for microservices main module

## Bugfixes

-   Sqlite DB is created on `create` for Django projects
