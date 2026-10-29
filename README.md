# VPS Bootstrap with Ansible

Automated VPS preparation and application deployment using Ansible, Docker Compose, Nginx, and PostgreSQL.

## Overview

This project automates the configuration of a remote Ubuntu VPS and deploys a containerized login application. It uses reusable Ansible roles to make deployments repeatable and easier to maintain.

## Architecture

- **Ansible:** Server configuration and deployment automation
- **Docker Compose:** Application container orchestration
- **Nginx:** Frontend delivery and reverse proxy
- **Python / Flask:** Backend login API
- **PostgreSQL:** Persistent user data storage
- **Ansible Vault:** Encryption of sensitive variables

## Project Structure

```text
vps-bootstrap/
├── ansible.cfg
├── requirements.yml
├── inventories/
│   ├── local/
│   └── production/
├── playbooks/
│   ├── bootstrap.yml
│   └── deploy.yml
└── roles/
    ├── common/
    ├── docker/
    ├── nginx/
    └── application/
```

## Ansible Roles

| Role | Responsibility |
|---|---|
| `common` | Install basic system packages |
| `docker` | Install and configure Docker |
| `nginx` | Configure the Nginx reverse proxy |
| `application` | Deploy the frontend, backend, and PostgreSQL using Docker Compose |

The project uses Ansible variables, Jinja2 templates, handlers, conditional tasks, registered results, and idempotent configuration.

## Prerequisites

- Ansible installed on the control node
- SSH access to the target VPS
- A supported Ubuntu target server
- Docker Engine and the Docker Compose plugin, installed or configured by the bootstrap workflow
- Python and the required Ansible modules on the managed host
- Git

Install the required Ansible collection:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Configuration

1. Configure the production inventory in `inventories/production/hosts.ini`.
2. Replace example values with your own server address and SSH username.
3. Store application credentials in the encrypted Vault variables file.
4. Never commit plaintext credentials, private keys, or the Vault password.

Create or edit the encrypted variables file:

```bash
ansible-vault create inventories/production/group_vars/webservers.vault.yml
```

If the encrypted file already exists, edit it instead:

```bash
ansible-vault edit inventories/production/group_vars/webservers.vault.yml
```

Use the variable names expected by the application role, including `app_db_password` and `app_demo_password`.

## Usage

Run commands from the project root on the Ansible control node.

### 1. Prepare the VPS

```bash
ansible-playbook \
  -i inventories/production/hosts.ini \
  playbooks/bootstrap.yml
```

### 2. Deploy the application

```bash
ansible-playbook \
  -i inventories/production/hosts.ini \
  playbooks/deploy.yml \
  --ask-vault-pass
```

### 3. Validate connectivity

```bash
ansible webservers \
  -i inventories/production/hosts.ini \
  -m ping
```

### 4. Access the application

Open the configured application port in your browser:

```text
http://YOUR_VPS_IP:8080/
```

Use the demo credentials configured in your encrypted Vault variables.

## Key Ansible Concepts

- **Inventory:** Defines the managed hosts and connection settings.
- **Playbooks:** Define the automation workflow.
- **Roles:** Separate server setup, Docker, Nginx, and application deployment.
- **Templates:** Generate configuration files from variables.
- **Handlers:** Restart affected services when configuration changes.
- **Idempotency:** Avoid unnecessary changes on repeated runs.
- **Ansible Vault:** Encrypt sensitive variables.

## Security Notes

- Keep credentials and private keys out of Git.
- Use Ansible Vault for sensitive variables.
- Restrict access to generated configuration files containing credentials.
- Keep PostgreSQL off the public network; expose only the application ports required by your deployment.
- Use SSH key authentication and restrict server access.
- Review firewall rules before exposing the application to the internet.

## Future Improvements

- Add automated deployment validation and smoke tests.
- Improve configuration validation and failure handling.
- Introduce a dedicated secrets management solution.
- Add CI/CD integration.
- Implement automated backups and recovery testing.

## License

Choose a license before permitting reuse or redistribution of this project.
