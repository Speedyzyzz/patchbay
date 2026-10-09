from typing import Dict, List
from pydantic import BaseModel, Field

class CallSite(BaseModel):
    file_path: str
    line_number: int
    symbol_name: str
    callee_expression: str
    arguments: List[str] = Field(default_factory=list)

class APIUsageGraph(BaseModel):
    call_sites: List[CallSite] = Field(default_factory=list)
    symbol_to_files: Dict[str, List[str]] = Field(default_factory=dict)

    def add_call_site(self, call: CallSite) -> None:
        self.call_sites.append(call)
        if call.symbol_name not in self.symbol_to_files:
            self.symbol_to_files[call.symbol_name] = []
        if call.file_path not in self.symbol_to_files[call.symbol_name]:
            self.symbol_to_files[call.symbol_name].append(call.file_path)
