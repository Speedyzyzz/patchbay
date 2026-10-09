from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class LLMResponse(BaseModel):
    content: Optional[str] = None
    model: str
    tokens_used: int = 0

class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.0,
        **kwargs: Any
    ) -> LLMResponse:
        pass
