# Handling various simulators

By default, the backend will use the SHIELD-HIT12A demo version as particle transport simulator.
This is a limited version of the full SHIELD-HIT12A code, can calculate only up to 10000 primary particles.
Also it has no support for any type of parallelization (the random number generator is frozen at certain value).

## Downloading simulators from S3 storage

To deploy yaptide platform with other simulators one needs to provide a location of other simulators in the S3 storage infrastructure.
The easiest way to achieve that is to provide a `.env` file in the `yaptide` directory (the directory where backend repository was cloned).

An example of such file is following:

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

## Preparing Fluka distribution

This instruction describes how to prepare Fluka distribution for usage with yaptide platform. This will cover procedure for GNU/Linux OS as Fluka is not supported on Windows OS.

### Prerequisites

To download fluka distribution one needs to register on [fluka website](https://fluka.cern/download/registration) and accept the license agreement.

After registration one can download the Fluka distribution from [fluka website](https://fluka.cern/download/latest-fluka-release).

### Building Fluka from prebuild files

To build Fluka user need to install additional dependencies described in [Installation manual](https://fluka.cern/documentation/installation). Especially matching gcc and gfortran compilers are required.
More detailed instruction is available on [Linux installation](https://fluka.cern/documentation/installation/fluka-linux-macos).

As we only want to build Fluka distribution, we are only interested in steps before and including `make` command.

After building Fluka with make command, we will have a `fluka` file located in:

#### Example

Having Fluka directory `fluka-4-3.4.x86-Linux-gfor9/fluka4-3.4/` (referred in Fluka instruction as `pathtofluka/`) which contains `bin` and `src` directories.

We are making a fluka executable by running:
```bash
cd /pathtofluka/src/
make
```

Fluka executable `fluka` will be located in `/pathtofluka/bin/` directory.

### Uploading Fluka to S3 storage

Having Fluka executable `fluka` located in `/pathtofluka/bin/` directory, we can compress and upload `pathtofluka/` directory to S3 storage.

To compress `pathtofluka/` directory we can use `tar` command:

```bash
tar -zcvf pathtofluka.tar.gz pathtofluka/
```

For our example it will take form of:

```bash
tar -zcvf fluka-4-3.4.x86-Linux-gfor9-bin.tgz fluka-4-3.4.x86-Linux-gfor9/fluka4-3.4/
```

Having compressed archive `fluka-4-3.4.x86-Linux-gfor9-bin.tgz` we can upload it to S3 storage.
For security reasons we will also want to encrypt our archive.

For both of these steps we can use script available in [Yaptide repository](https://github.com/yaptide/yaptide/blob/master/yaptide/admin/simulator_storage.py).

Script uses environment variables to access S3 storage, so we need to set them before running script:

```bash
export S3_ENDPOINT="https://s3p.cloud.cyfronet.pl"
export S3_ACCESS_KEY="plgs3p-plggyaptide-plg<USERNAME>"
export S3_SECRET_KEY="<MY_VERY_SECRET_KEY>"
export S3_ENCRYPTION_PASSWORD="<ENCRYPTION_PASSWORD>"
export S3_ENCRYPTION_SALT="<ENCRYPTION_SALT>"

export S3_FLUKA_BUCKET=fluka
export S3_FLUKA_KEY=fluka-4-3.4.x86-Linux-gfor9-bin.tgz
```

Then we can use script to upload and encrypt our archive:

```bash
python3 yaptide/admin/simulators.py upload --encrypt --bucket $S3_FLUKA_BUCKET --file ./path_to_fluka_archive/fluka-4-3.4.x86-Linux-gfor9-bin.tgz --endpoint $S3_ENDPOINT --access_key $S3_ACCESS_KEY --secret_key $S3_SECRET_KEY --password $S3_ENCRYPTION_PASSWORD --salt $S3_ENCRYPTION_SALT
```

#### Download Fluka from S3 storage to verify checksum

```bash
python3 yaptide/admin/simulators.py download-fluka --dir ./downloaded --bucket $S3_FLUKA_BUCKET --key $S3_FLUKA_KEY --endpoint $S3_ENDPOINT --access_key $S3_ACCESS_KEY --secret_key $S3_SECRET_KEY --password $S3_ENCRYPTION_PASSWORD --salt $S3_ENCRYPTION_SALT
```

```bash
md5sum ./fluka-4-3.4.x86-Linux-gfor9/fluka4-3.4/bin/fluka
md5sum ./downloaded/fluka/fluka4-3.2/bin/fluka
```

Files should be identical.
