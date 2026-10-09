from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow", env_file=".env")

    PROJECT_NAME: str = "PatchBay Runtime"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    DEFAULT_LLM_PROVIDER: str = "offline"
    WORKSPACE_ROOT: str = "/tmp/patchbay_workspace"

settings = Settings()
