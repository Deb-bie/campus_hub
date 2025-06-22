from pydantic import BaseModel # type: ignore
from typing import Optional, Dict

class LogItem(BaseModel):
    timestamp: str
    service_name: str
    log_level: str
    message: str
    metadata: Optional[Dict] = {}

    request_id: Optional[str] = None
    trace_id: Optional[str] = None       
    environment: Optional[str] = "dev"

