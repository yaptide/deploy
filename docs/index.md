# Local deployment

## Prerequisites

First we need to clone both backend and frontend repositories:

```bash
git clone --recurse-submodules https://github.com/yaptide/yaptide.git
git clone --recurse-submodules https://github.com/yaptide/ui.git
```

Note `--recurse-submodules`. This is needed as the converter package is included as a submodule in both repositories.

Local deployment allows only for job execution on Celery worker. To be able to submit jobs to the HPC cluster, one needs to have access to the 

## Deploying backend

Lets start with deploying backend using docker compose. This should take couple of minutes to complete. Following command would start couple of containers in the background:

```bash
cd yaptide
docker compose up -d
```

Most of the time consuming process is download and installation of python requirements needed to run flask server and worker. When created, the worker container should automatically download the `SHIELD-HIT12A` demo executable and be ready to accept jobs.

The `yaptide_nginx` container serves as a proxy and is exposing the REST API on following ports:
  * port 5000, using plain HTTP
  * port 8443, using HTTPS with self-signed certificate (which may be untrusted by your browser)



## Deploying frontend

In a similar way as for backend, the frontend can be deployed using docker compose. This should take couple of minutes to complete. Following command would start couple of containers in the background:

```bash
cd ui
docker compose up -d
```

This will start 