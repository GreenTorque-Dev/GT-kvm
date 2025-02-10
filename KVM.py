import kvm
from unix.linux import Linux
from unix import Local
import json


class KVMManager:
    def __init__(self, uri="qemu:///system"):
        self.uri = uri
        self.hypervisor = None
        self.domains = {}  # Store domain objects
        self.connect()

    def connect(self):
        """Establish a connection to the KVM hypervisor."""
        self.hypervisor = kvm.Hypervisor(Linux(Local()), uri=self.uri)
        self._load_domains()

    def _load_domains(self):
        """Load existing domains into the dictionary."""
        domain_list = self.hypervisor.list_domains(all=True)
        self.domains = {name: Domain(self.hypervisor, name) for name in domain_list}

    def get_nodeinfo(self):
        """Retrieve system node information."""
        return self.hypervisor.nodeinfo()

    def get_domain(self, name):
        """Retrieve a specific domain object by name."""
        return self.domains.get(name)

    def list_domains(self):
        """List all available domains."""
        return list(self.domains.keys())

    def create_domain(self, config):
        """Create a new domain using the given configuration."""
        domain_name = config.get("name")
        if not domain_name:
            raise ValueError("Domain configuration must include a name.")
        self.hypervisor.domain_create(config)
        self.domains[domain_name] = Domain(self.hypervisor, domain_name)

    def delete_domain(self, name):
        """Delete a domain by name."""
        if name in self.domains:
            self.hypervisor.domain.delete(name)
            del self.domains[name]

    def list_networks(self):
        """List available networks."""
        return self.hypervisor.list_networks()


class Domain:
    def __init__(self, hypervisor, name):
        self.hypervisor = hypervisor
        self.name = name

    def start(self):
        """Start the domain."""
        return self.hypervisor.domain.start(self.name)

    def stop(self):
        """Stop the domain."""
        return self.hypervisor.domain.shutdown(self.name)

    def force_stop(self):
        """Force stop the domain."""
        return self.hypervisor.domain.destroy(self.name)

    def get_state(self):
        """Retrieve the current state of the domain."""
        return self.hypervisor.domain.state(self.name)

    def get_id(self):
        """Retrieve the domain ID."""
        return self.hypervisor.domain.id(self.name)

    def get_config(self):
        """Retrieve the domain configuration in JSON format."""
        return json.dumps(self.hypervisor.domain.conf(self.name), indent=2)


# Example Usage:
if __name__ == "__main__":
    manager = KVMManager()
    print("Node Info:", manager.get_nodeinfo())

    domains = manager.list_domains()
    print("Available Domains:", domains)

    domain_name = "guest1"
    if domain_name in domains:
        domain = manager.get_domain(domain_name)
        print(f"State of {domain_name}:", domain.get_state())
        print(f"Config of {domain_name}:\n", domain.get_config())
