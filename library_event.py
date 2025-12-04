from datetime import datetime

class LibraryEvent:
    def __init__(self, event_type: str, details: str, timestamp: datetime):
        self.event_type = event_type
        self.details = details
        self.timestamp = timestamp

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.event_type}: {self.details}"