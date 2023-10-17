# Maintenance

## Updating the repository to newer commits or other branches

To update the repository to newer commits or other branches, execute the following commands in the `yaptide` and/or `ui` directory:

```bash
git pull
```

update submodules (i.e. converter):

```bash
git submodule update --init --recursive
```


Then stop the containers:

```bash
docker compose down
```

and start them again:

```bash
docker compose up --detach --build
```

Note the `--build` flag. It is needed to rebuild the containers, as the source code has changed.


## Storage volume

The yaptide backend uses the docker volume named `yaptide_data` to store the data. It hosts SQLite database with following information:

  * user accounts
  * data related to simulations:
    * pending and completed jobs and tasks
    * simulation input files
    * simulation results and logs
  * list of supported clusters

The volume is created automatically (with empty database) when the backend containers are started for the first time.
To remove the volume and all data stored in it, stop the backend containers, by executing in the `yaptide` directory:

```bash
docker compose down --volumes
```

## SSL certificates

The SSL certificates are used to secure the communication for two cases:

  * between the user client and the machine serving the UI
  * between the user client and the machine serving the backend

Frontend uses Nginx to serve statically generated HTML, CSS and JavaScript files. 
Backend uses Nginx as a proxy to forward requests to the backend server.
Both Nginx instances are configured to use SSL certificates.

By default the self-signed certificates are used (usually not trusted by the browser). 
They are generated automatically when the containers are started for the first time.

To replace self-signed certificates with your own, stop the containers and replace the files according to the following recipe.

### Frontend

Ensure that `yaptide_ui` container is running.

Copy the files `server.key` containing the private key:

```bash
docker cp server.key yaptide_ui:/etc/nginx/conf.d/server.key
```

and `server.crt` containing the certificate:

```bash
docker cp server.crt yaptide_ui:/etc/nginx/conf.d/server.crt
```

also `rootca.crt` containing the root certificate:

```bash
docker cp rootca.crt yaptide_ui:/etc/nginx/conf.d/rootca.crt
```

Restart the container:

```bash
docker restart yaptide_ui
```

### Backend

Ensure that `yaptide_nginx` container is running.

Copy the files `server.key` containing the private key:

```bash
docker cp server.key yaptide_nginx:/etc/nginx/conf.d/server.key
```

and `server.crt` containing the certificate:

```bash
docker cp server.crt yaptide_nginx:/etc/nginx/conf.d/server.crt
```

and `rootca.crt` containing the root certificate:

```bash
docker cp rootca.crt yaptide_nginx:/etc/nginx/conf.d/rootca.crt
```

Restart the container:

```bash
docker restart yaptide_nginx
```

### Certificate inspection

To verify the certificate chain, execute the following command:

```bash
openssl verify -CAfile rootca.crt server.crt
```