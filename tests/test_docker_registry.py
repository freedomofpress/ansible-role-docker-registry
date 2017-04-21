import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_docker_registry_data_direcotry(File):
    f = File('/var/www/docker-registry')
    assert f.exists
    assert f.is_directory
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == "0755"


# Not configured by the role, but required, and listed in the testing
# dependencies.
def test_docker_is_installed(Package):
    p = Package("docker")
    assert p.is_installed
