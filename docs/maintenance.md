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


## Yaptide platform storage

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

