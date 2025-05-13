from entities.user import ts_to_date

class Connection:
    def __init__(self, ip, last_seen, user_agent):
        self.ip = ip
        self.last_seen = ts_to_date(last_seen) if last_seen is not None else None
        self.user_agent = user_agent

    def __str__(self):
        return f"IP: {self.ip}, Last seen: {self.last_seen}, User agent: {self.user_agent}"
    
class Device:
    def __init__(self, device_id, display_name, last_seen_ip, last_seen_user_agent, last_seen, user_id):
        self.device_id = device_id
        self.display_name = display_name
        self.last_seen_ip = last_seen_ip
        self.last_seen_user_agent = last_seen_user_agent
        self.last_seen = ts_to_date(last_seen) if last_seen is not None else None
        self.user_id = user_id

    def __str__(self):
        return f"Device ID: {self.device_id}, Display name: {self.display_name}, Last seen IP: {self.last_seen_ip}, Last seen user agent: {self.last_seen_user_agent}, Last seen: {self.last_seen}"