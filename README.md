## Introduction

Social Networking is a dockerized application that facilitates user account creation, login, and the exchange of friend requests.

## Features

- **Login:**
  Authenticate users using credentials and receive access and refresh tokens.

- **List Users:**
  Display a list of all users.

- **Send Friend Request:**
  Allow users to send friend requests to others.

- **List Friend Requests:**
  Provide a list of friend requests received.

- **Accept or Reject:**
  Enable users to accept or reject received friend requests.

- **List All Friends:**
  Display a list of users who have accepted friend requests.

## Prerequisites

- **Language:** Python
- **Framework:** Django, Django RestFramework
- **Database:** PostgreSQL

## Getting Started

1. Add a `.env` file to the repository with all necessary values.
2. Build and run the project using the following command:

```bash
docker-compose up --build
```
## Docker Setup

1. [Install Docker](https://docs.docker.com/get-docker/)
```bash
# Build the Docker image
docker-compose up --build
# Run the Docker container
docker-compose up
# Run bash shell
docker-compose exec social-networking bash
```
