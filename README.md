# Deploy
Ansible playbooks for cloud deploy

1. Fill the clouds.yaml with credentials needed to access OpenStack cloud

2. Install necessary requirements:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Query the dynamic inventory:

```
ansible-inventory --graph
```