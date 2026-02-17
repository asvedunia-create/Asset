class ADResolver:
    """MVP resolver. Replace with LDAP/AD query in production."""

    def resolve_owner(self, hostname: str) -> str:
        if hostname.lower().startswith("srv-win"):
            return "windows-team@example.com"
        return "linux-team@example.com"
