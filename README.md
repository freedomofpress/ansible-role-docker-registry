docker-registry Ansible role
============================

Installs and configures the official [Docker registry] container.


Requirements
------------

You will need to configure a reverse proxy for HTTPS with basic auth.

Role Variables
--------------

```yaml
# Directory for storing pushed images on registry host.
docker_registry_data_directory: /var/www/docker-registry

# Port to expose to host machine, for use in reverse proxy.
docker_registry_expose_port: 5000
```

Dependencies
------------

  * Docker container support (e.g. marklee77.docker)
  * HTTPS reverse proxy (e.g. jdauphant.nginx)

Example Playbook
----------------

```yaml
# Configure only local Docker container.
# Does not handle HTTPS reverse proxy.
- name: Configure Docker registry.
  hosts: docker-registry
  roles:
    - role: freedomofpress.docker-registry


# Configure HTTPS reverse proxy via Nginx.
- name: Configure Docker registry.
  hosts: docker-registry
  vars:
    docker_registry_expose_port: 9000
  roles:
    - role: freedomofpress.docker-registry
    - role: jdauphant.nginx
      nginx_sites:
        docker_registry:
          - listen 443
          - server_name {{ letsencrypt_fqdn }}
          - ssl on
          - ssl_certificate {{ letsencrypt_cert_chain_fullpath }}
          - ssl_certificate_key {{ letsencrypt_cert_privkey_fullpath }}
          - root {{ docker_registry_data_directory }}
          - client_max_body_size 0
          - chunked_transfer_encoding on
          - |-
              location /v2/ {
                proxy_pass http://127.0.0.1:5000;
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_read_timeout 900;
              }
```

Running the tests
-----------------

This role uses [Molecule] and [Testinfra] for testing. To test:

```
pip install -r requirements.txt
```

License
-------

MIT

Author Information
------------------

[Freedom of the Press Foundation]

[Docker registry]: https://hub.docker.com/_/registry/
[thefinn93.letsencrypt]: https://github.com/thefinn93/ansible-letsencrypt
[jdauphant.nginx]: https://github.com/jdauphant/ansible-role-nginx
[Freedom of the Press Foundation]: https://freedom.press/
[Molecule]: http://molecule.readthedocs.org/en/master/
