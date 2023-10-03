# Handling various simulators

By default, the backend will use the SHIELD-HIT12A demo version as particle transport simulator.
This is a limited version of the full SHIELD-HIT12A code, can calculate only up to 10000 primary particles.
Also it has no support for any type of parallelization (the random number generator is frozen at certain value).

## Downloading simulators from S3 storage

To deploy yaptide platform with other simulators one needs to provide a location of other simulators in the S3 storage infrastructure.
The easiest way to achieve that is to provide a `.env` file in the `yaptide` directory (the directory where backend repository was cloned).

An example of such file dedicated to SHIELD-HIT12A is following:

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
docker compose up -d
```

Inspect logfiles of the worker container to see if the SHIELD-HIT12A binary was downloaded and decrypted:

```
docker logs -f yaptide_worker
```