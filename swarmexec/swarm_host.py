import validators

class SwarmHost:

    def __init__(self, hostname:str):
        self.user, self.hostname = get_user_hostname(hostname)
        self.domain = get_domain_from_host(self.hostname)

    def ssh_connection_string(self, hostname=None):
        if not hostname:
            hostname = self.hostname
        if self.user:
            return "ssh://" + "@".join([self.user, hostname])
        else:
            return "ssh://" + hostname


def get_user_hostname(hostname:str):
    hostname.replace("ssh://", "")
    user = None
    if "@" in hostname:
        user = hostname.split("@")[0]
        hostname = hostname.split("@")[1]
    return user, hostname


def get_domain_from_host(hostname:str):
    if validators.domain(hostname):
        if len(hostname.split(".")) == 3:
            return ".".join(hostname.split(".")[1:])


def validate_ssh_connection_string(orig_hostname:str):
    user, hostname = get_user_hostname(orig_hostname)
    is_valid_host =  validators.domain(hostname) or validators.ipv4(hostname) or validators.ipv6(hostname)
    if not is_valid_host:
        raise ValueError
    return orig_hostname
