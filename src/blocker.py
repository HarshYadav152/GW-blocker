import os
import platform
import datetime
from typing import List

class WebsiteBlocker:
    def __init__(self):
        """Initialize the website blocker with platform-specific hosts file path."""
        self.redirect = "127.0.0.1"
        self.hosts_path = self._get_hosts_path()
        
    def _get_hosts_path(self) -> str:
        """Get the hosts file path based on the operating system."""
        system = platform.system().lower()
        if system == "windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        elif system in ("linux", "darwin"):  # Linux or macOS
            return "/etc/hosts"
        else:
            raise OSError(f"Unsupported operating system: {system}")
    
    def is_admin(self) -> bool:
        """Check if the script is running with admin privileges."""
        try:
            if platform.system().lower() == "windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0  # Unix-based systems
        except Exception:
            return False
            
    def block_website(self, website: str) -> bool:
        """Block a specific website."""
        if not self.is_admin():
            return False
            
        try:
            with open(self.hosts_path, "r+") as hosts_file:
                content = hosts_file.read()
                if website not in content:
                    hosts_file.write(f"\n{self.redirect} {website}")
                return True
        except Exception:
            return False
            
    def block_websites(self, websites: List[str]) -> bool:
        """Block multiple websites."""
        if not self.is_admin():
            return False
            
        try:
            with open(self.hosts_path, "r+") as hosts_file:
                content = hosts_file.read()
                for website in websites:
                    if website not in content:
                        hosts_file.write(f"\n{self.redirect} {website}")
                return True
        except Exception:
            return False
    
    def unblock_website(self, website: str) -> bool:
        """Unblock a specific website."""
        if not self.is_admin():
            return False
            
        try:
            with open(self.hosts_path, "r+") as hosts_file:
                lines = hosts_file.readlines()
                hosts_file.seek(0)
                for line in lines:
                    if not line.strip().endswith(website):
                        hosts_file.write(line)
                hosts_file.truncate()
                return True
        except Exception:
            return False
            
    def unblock_all(self) -> bool:
        """Unblock all websites (remove all custom entries)."""
        if not self.is_admin():
            return False
            
        try:
            with open(self.hosts_path, "r+") as hosts_file:
                lines = hosts_file.readlines()
                hosts_file.seek(0)
                for line in lines:
                    if self.redirect not in line:
                        hosts_file.write(line)
                hosts_file.truncate()
                return True
        except Exception:
            return False
            
    def get_blocked_websites(self) -> List[str]:
        """Get a list of currently blocked websites."""
        blocked_sites = []
        try:
            with open(self.hosts_path, "r") as hosts_file:
                for line in hosts_file:
                    if line.strip().startswith(self.redirect):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            blocked_sites.append(parts[1])
        except Exception:
            pass
        return blocked_sites