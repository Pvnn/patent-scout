from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalConfig(BaseSettings):
    """
    Global configuration settings for the PatentScout application.
    Can be overridden via environment variables (e.g., PATENTSCOUT_MAX_RETRIES=5).
    """

    MAX_RETRIES: int = 3
    RETRY_BACKOFF_FACTOR: float = 2.0  # Base seconds to wait before retry (exponential)
    TIMEOUT_SECONDS: int = 120  # Hard timeout for any subprocess tool
    OPENAI_MODEL: str = "gpt-4o-mini"  # Low-cost model for production
    OPENAI_TEMPERATURE: float = 0.0  # Zero temperature for deterministic outputs

    model_config = SettingsConfigDict(env_prefix="PATENTSCOUT_")


# Global configuration instance
config = GlobalConfig()
