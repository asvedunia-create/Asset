from dataclasses import dataclass


@dataclass
class InventorySnapshot:
    os_name: str
    services: list[dict[str, str]]


class SSHCollector:
    def collect(self, hostname: str, address: str) -> InventorySnapshot:
        # MVP stub. Replace with real SSH commands and parsers.
        return InventorySnapshot(
            os_name="Linux",
            services=[
                {"name": "nginx", "version": "1.24.0"},
                {"name": "sshd", "version": "9.6p1"},
            ],
        )


class WinRMCollector:
    def collect(self, hostname: str, address: str) -> InventorySnapshot:
        # MVP stub. Replace with real WinRM PowerShell queries.
        return InventorySnapshot(
            os_name="Windows Server 2022",
            services=[
                {"name": "IIS", "version": "10.0"},
                {"name": "WinRM", "version": "3.0"},
            ],
        )


def collect_inventory(protocol: str, hostname: str, address: str) -> InventorySnapshot:
    if protocol == "ssh":
        return SSHCollector().collect(hostname=hostname, address=address)
    if protocol == "winrm":
        return WinRMCollector().collect(hostname=hostname, address=address)
    raise ValueError(f"Unsupported protocol: {protocol}")
