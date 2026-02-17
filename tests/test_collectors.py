from app.ad import ADResolver
from app.collectors import collect_inventory


def test_collect_inventory_ssh_returns_linux():
    snap = collect_inventory("ssh", "srv-linux-01", "10.0.0.10")
    assert snap.os_name == "Linux"
    assert any(s["name"] == "nginx" for s in snap.services)


def test_collect_inventory_winrm_returns_windows():
    snap = collect_inventory("winrm", "srv-win-01", "10.0.0.20")
    assert snap.os_name.startswith("Windows")


def test_ad_resolver_owner():
    resolver = ADResolver()
    assert resolver.resolve_owner("srv-win-01") == "windows-team@example.com"
    assert resolver.resolve_owner("srv-linux-01") == "linux-team@example.com"
