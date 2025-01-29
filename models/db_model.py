from datetime import datetime

class DbModel:
    id: str
    date_time_created: datetime
    date_time_modified: datetime
    date_time_deleted: datetime
    deleted: bool

    def __init__(self):
        self.deleted = False
        self.date_time_deleted = None

    def set_audit_fields(self):
        current_time = datetime.utcnow()
        if not hasattr(self, 'date_time_created') or not self.date_time_created:
            self.date_time_created = current_time
        self.date_time_modified = current_time

    def get_audit_dict(self) -> dict:
        return {
            "date_time_created": self.date_time_created,
            "date_time_modified": self.date_time_modified
        }

    def set_audit_fields_from_dict(self, data: dict):
        self.date_time_created = data.get("date_time_created")
        self.date_time_modified = data.get("date_time_modified")
        self.date_time_deleted = data.get("date_time_deleted", None)
        self.deleted = data.get("deleted", False)

    def mark_as_deleted(self):
        self.deleted = True
        self.date_time_deleted = datetime.utcnow()