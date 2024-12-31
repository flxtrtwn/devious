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
