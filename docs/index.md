# Local deployment

## Requirements

To be able to run the application locally, you need to have following software installed:

  * [Docker](https://docs.docker.com/get-docker/)
  * [Docker Compose](https://docs.docker.com/compose/install/)
  * [Git](https://git-scm.com/downloads)

These products could be installed on Linux and Windows. Docker for Windows usually uses WSL2 (Windows Subsystem for Linux ) backend.
The commands listed below can be executed on plain Powershell, there is no need to run them inside WSL2.

## Prerequisites

First we need to clone both backend:

```bash
git clone --recurse-submodules https://github.com/yaptide/yaptide.git
```

and frontend repositories:
```bash
git clone --recurse-submodules https://github.com/yaptide/ui.git
```

Note `--recurse-submodules`. This is needed as the converter package is included as a submodule in both repositories.

Local deployment allows only for job execution on Celery worker. To be able to submit jobs to the HPC cluster, one needs to have access to the

## Deploying backend

Lets start with deploying backend using docker compose. This should take couple of minutes to complete.

First go to the directory where backend was cloned:
```bash
cd yaptide
```

Following command would start couple of containers in the background:
```bash
docker compose up --detach
```

Most of the time consuming process is download and installation of python requirements needed to run flask server and worker. When created, the worker container should automatically download the `SHIELD-HIT12A` demo executable and be ready to accept jobs.

The `yaptide_nginx` container serves as a proxy and is exposing the REST API on following ports:

  * port 5000, using plain HTTP
  * port 8443, using HTTPS with self-signed certificate (which may be untrusted by your browser)

## Deploying frontend

In a similar way as for backend, the frontend can be deployed using docker compose. This should take couple of minutes to complete.

First go to the directory where frontend was cloned:
```bash
cd ui
```

Following command would start in the UI container in the background:

```bash
docker compose up --detach
```

The `yaptide_ui` container serves static version of the frontend using nginx, on following ports:

  * port 80, using plain HTTP
  * port 443, using HTTPS with self-signed certificate (which may be untrusted by your browser)

Frontend is configured to use the backend REST API exposed on port 5000, using plain HTTP.

## Creating first user

At this point there is no single user in the database, so we need to create one. This can be done using the following command:

```bash
docker exec yaptide_flask ./yaptide/admin/db_manage.py add-user admin --password password
```

## Running first simulation

Now we are ready to run our first simulation. First we need to login to the frontend. Open your browser and navigate to [http://localhost:80](http://localhost:80) or [https://localhost:443](https://localhost:443).
Login with the credentials created in the previous step.
