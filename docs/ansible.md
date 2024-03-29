# Deploy of the yaptide platform to the OpenStack cloud platform

## The aim

The aim of this project it to provide an automated deploy of the yaptide platform to the OpenStack cloud platform.
The deployment is managed by the ansible playbooks. In this project two major playbooks are used:
 - `cloud_instance.yml` - for creating (and teardown) a cloud instance
 - `site.yml` - for deploying the yaptide platform

## Local deployment

1. Install requirements necesary for running the ansible playbooks:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

In our projects we use `ansible` Python package. It uses SSH to connect to the remote machines.
As for now the `ansible` package does not work natively on Windows.
The only way to run it from Windows is to use the `WSL` (Windows Subsystem for Linux).

2. Deploy the yaptide platform on the local machine.

The simulator binaries are copied from S3 or other types of storage at the moment when remote docker containers are starting.
```bash
ansible-playbook site.yml -i environments/local
```

3. To remove the yaptide platform from the instance, run:

```bash
ansible-playbook site.yml -i environments/local -e mode=clean
```

## Instructions

1. Downloand the `openrc.sh` file from the OpenStack dashboard and source it. If it asks for a password, use the one from the dashboard.

```
. plgrid-ext-plggyaptide-openrc.sh
```

2. Install requirements necesary for running the ansible playbooks:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

In our projects we use `ansible` Python package. It uses SSH to connect to the remote machines.
As for now the `ansible` package does not work natively on Windows.
The only way to run it from Windows is to use the `WSL` (Windows Subsystem for Linux).

3. Query the dynamic inventory:

```bash
ansible-inventory --graph
```

To print public IPs of all instances in the dynamic inventory:

```bash
ansible -m debug -a "var=hostvars[inventory_hostname].ansible_host" all
```

4. Create an instance on OpenStack cloud:

This step may take about 3-4 minutes, so be patient. Once it is completed, a machine named `yaptide` will be created on the OpenStack cloud.

```bash
ansible-playbook cloud_instance.yml
```

Once the instance is created, you can optionally run time consuming package upgrade task on it. This step may take about 10-15 minutes, so be patient.

```bash
ansible yaptide -m apt -a "update_cache=yes upgrade=dist" --become
ansible yaptide -m reboot --become
```

In case you have an existing snaphot image, you can use it to create an instance.
This will save you some time, as the image will be used instead of installing all the packages from scratch.

```bash
ansible-playbook cloud_instance.yml -e "image_name='Ubuntu 20.04 LTS Snapshot 20230404'"
```

To get larger flavor with more CPUs or RAM, use the following command:

```bash
ansible-playbook cloud_instance.yml -e "flavor_name='h2.large'"
```

You can combine both options:

```bash
ansible-playbook cloud_instance.yml -e "image_name='Ubuntu 22.04 LTS Snapshot (20230404)'" -e "flavor_name='h2.large'"
```


To create an instance with a different name, use the following command:

```bash
ansible-playbook cloud_instance.yml -e "instance_name='yaptide2'"
```

5. Deploy the yaptide platform on the instance.
At this stage necessary packages will be installed and respective repositories cloned.
The backend will be served on port 5000 and the frontend on port 80.
This step is time consuming and may take more than 10 minutes.

The simulator binaries are copied from S3 or other types of storage at the moment when remote docker containers are starting.

```bash
ansible-playbook site.yml
```

To perform deployment on a specific branch, use the following command:

```bash
ansible-playbook site.yml -e backend_repo_version='backend-branch-name' -e frontend_repo_version='frontend-branch-name'
```

To specify different IP of the backend and frontend:

```bash
ansible-playbook site.yml -e frontend_backend_hostname='149.156.182.181' -e frontend_ui_hostname='149.156.182.181' -e backend_repo_version='backend-branch-name' -e frontend_repo_version='frontend-branch-name'
```
or

```
ansible-playbook site.yml -e frontend_backend_hostname='yap-dev.c3.plgrid.pl' -e frontend_backend_url='https://yap-dev.c3.plgrid.pl:5000' -e frontend_ui_hostname='yap-dev.c3.plgrid.pl' -e frontend_ui_hostname='https://yap-dev.c3.plgrid.pl'
```

or

```
ansible-playbook site.yml -e @yap_dev_vars.yml
```

You can also run only few stages of the deployment. For example to perform only installation of necessary packages, use the following command:

```bash
ansible-playbook site.yml --tags "setup"
```

To deploy on an instance with a different name, use the following command:

```bash
ansible-playbook site.yml -e "variable_host='yaptide2'"
```

Once the `yaptide` platform is deployed, you can access it by visiting the public IP of the instance in your browser.
The password to the admin account can be found in the file `roles/backend/files/password` in the repository.

6. To remove the yaptide platform from the instance, run:

```bash
ansible-playbook site.yml -e mode=clean
```

7. Tear down the instance.

```bash
ansible-playbook cloud_instance.yml -e mode=clean
```
