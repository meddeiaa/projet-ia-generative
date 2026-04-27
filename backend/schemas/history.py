from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class HistoryItem(BaseModel):
    """
    Une entrée d'historique
    """
    id: int
    generation_type: str
    prompt: str
    style: Optional[str] = None
    result: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    """
    Liste d'historique avec pagination
    """
    items: List[HistoryItem]
    total: int