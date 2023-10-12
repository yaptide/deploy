# Handling various simulators

By default, the backend will use the SHIELD-HIT12A demo version as particle transport simulator.
This is a limited version of the full SHIELD-HIT12A code, can calculate only up to 10000 primary particles.
Also it has no support for any type of parallelization (the random number generator is frozen at certain value).

## Downloading simulators from S3 storage

To deploy yaptide platform with other simulators one needs to provide a location of other simulators in the S3 storage infrastructure.
The easiest way to achieve that is to provide a `.env` file in the `yaptide` directory (the directory where backend repository was cloned).

An example of such file dedicated is following:

```
S3_ENDPOINT=https://endpoint_of_s3_storage
S3_ACCESS_KEY=access_key
S3_SECRET_KEY=secret_key
S3_SHIELDHIT_BUCKET=bucket_name_with_shieldhit12a_binary
S3_SHIELDHIT_KEY=filename_of_shieldhit12a_binary
S3_ENCRYPTION_PASSWORD=mysecret_password_to_decrypt_simulator_binary
S3_ENCRYPTION_SALT=salt_to_decrypt_simulator_binary
```

This contents of this file are following:

* `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY` - credentials to access S3 storage
* `S3_SHIELDHIT_BUCKET`, `S3_SHIELDHIT_KEY` - location of SHIELD-HIT12A binary in S3 storage
* `S3_ENCRYPTION_PASSWORD`, `S3_ENCRYPTION_SALT` - password and salt to decrypt SHIELD-HIT12A binary

## How to deploy backend with other simulators

Stop the backend containers:

```
docker compose down
```

Create `.env` file with the contents described above.

Start the backend containers:

```
docker compose up --detach
```

Inspect logfiles of the worker container to see if the SHIELD-HIT12A binary was downloaded and decrypted:

```
docker logs --follow yaptide_worker
```

Check which version of SHIELD-HIT12A was deployed:

```
docker exec -it yaptide_worker shieldhit --version
```

## Parallel simulation execution

By default the CPU usage of the worker container will be limited by default to a single CPU core.
To allow for usage of multiple cores one needs to set MAX_CORES environment variable.

The easiest way is to provide it during execution of `docker compose up` command. For example to allow for usage of 4 cores:

=== "Linux"

    ```bash
    MAX_CORES=4 docker compose up --detach
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:MAX_CORES=4; docker compose up --detach
    ```

Another way is to add following line to the `.env` file:

```
MAX_CORES=4
```

then stop the backend containers:

```bash
docker compose down
```

and start them again:

```bash
docker compose up --detach
```

## TOPAS support
In future we plan to add support for TOPAS simulator. Right now it could be installed in the worker container, but TOPAS simulations cannot be executed. To allow installation of TOPAS set following additional variables in the .env file.

```
S3_TOPAS_BUCKET=bucket_name_with_topas_binary
S3_TOPAS_KEY=filename_of_topas_binary
S3_TOPAS_VERSION=version_of_topas
S3_GEANT_BUCKET=bucket_name_with_geant4_files
```

* `S3_TOPAS_BUCKET`, `S3_TOPAS_KEY` - location of TOPAS binary in S3 storage
* `S3_TOPAS_VERSION` - version of TOPAS to be downloaded
* `S3_GEANT_BUCKET` - location of Geant4 files in S3 storage (required for TOPAS)
