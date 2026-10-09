from typing import Any, Dict, List
from app.llm.provider import LLMProvider, LLMResponse

class OfflinePatchSynthesizerLLM(LLMProvider):
    def __init__(self, model_name: str = "patchbay-offline-v1"):
        self.model_name = model_name

    async def generate(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.0,
        **kwargs: Any
    ) -> LLMResponse:
        return LLMResponse(
            content="Synthesized AST rewrite rule candidate",
            model=self.model_name,
            tokens_used=40
        )
