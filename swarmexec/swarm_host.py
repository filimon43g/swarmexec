import validators

class SwarmHost:

    def __init__(self, hostname:str):
        self.user, self.hostname = get_user_hostname(hostname)

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


def validate_ssh_connection_string(orig_hostname:str):
    user, hostname = get_user_hostname(orig_hostname)
    is_valid_host =  validators.domain(hostname) or validators.ipv4(hostname) or validators.ipv6(hostname)
    if not is_valid_host:
        raise ValueError
    return orig_hostname
