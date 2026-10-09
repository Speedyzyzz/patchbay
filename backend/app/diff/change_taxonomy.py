from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ChangeCategory(str, Enum):
    ENDPOINT_RENAME = "endpoint_rename"
    PARAM_ADDED = "param_added"
    PARAM_REMOVED = "param_removed"
    PAGINATION_CHANGED = "pagination_changed"
    AUTH_CHANGED = "auth_changed"

class APIContractChange(BaseModel):
    change_id: str
    category: ChangeCategory
    target_symbol: str
    replacement_symbol: Optional[str] = None
    old_signature: Dict[str, Any] = Field(default_factory=dict)
    new_signature: Dict[str, Any] = Field(default_factory=dict)
    migration_hint: str
