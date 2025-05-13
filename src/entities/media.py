import datetime

class MediaDTO():
    def __init__(self, created_ts: int = None, last_access_ts: int = None, media_id: str = None, media_length: int = None, 
                 media_type: str = None, quarantined_by: str = None, safe_from_quarantine: bool = None, upload_name: str = None):
        self.created_ts = ts_to_date(created_ts) if created_ts is not None else None
        self.last_access_ts = ts_to_date(last_access_ts) if last_access_ts is not None else None
        self.media_id = media_id
        self.media_length = media_length
        self.media_type = media_type
        self.quarantined_by = quarantined_by
        self.safe_from_quarantine = safe_from_quarantine
        self.upload_name = upload_name

    def __str__(self):
        return f"Media: created_at {self.created_ts}, last_access_ts {self.last_access_ts}, media_id {self.media_id}, media_length {self.media_length}, media_type {self.media_type}, quarantined_by {self.quarantined_by}, safe_from_quarantine {self.safe_from_quarantine}, upload_name {self.upload_name}"

def ts_to_date(ts):
        date = datetime.datetime.fromtimestamp(ts / 1000)
        return date.strftime('%Y-%m-%d, %H:%M:%S')