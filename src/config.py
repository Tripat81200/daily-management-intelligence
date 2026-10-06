import os
import yaml
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"


def load_config(config_file: Path = CONFIG_PATH) -> Dict[str, Any]:
    """Load configuration from YAML and overlay environment variables."""
    cfg: Dict[str, Any] = {}
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

    # Overlay environment variables
    env_mappings = {
        "GEMINI_API_KEY": ("ai", "gemini_api_key"),
        "GOOGLE_API_KEY": ("ai", "gemini_api_key"),
        "OPENAI_API_KEY": ("ai", "openai_api_key"),
        "EMAIL_TO": ("email", "to"),
        "EMAIL_FROM": ("email", "from_address"),
        "EMAIL_SERVICE": ("email", "service"),
        "RESEND_API_KEY": ("email", "resend_api_key"),
        "SMTP_HOST": ("email", "smtp_host"),
        "SMTP_PORT": ("email", "smtp_port"),
        "SMTP_USER": ("email", "smtp_user"),
        "SMTP_PASS": ("email", "smtp_pass"),
        "DRY_RUN": ("runtime", "dry_run"),
        "LOG_LEVEL": ("runtime", "log_level"),
    }

    if "email" not in cfg:
        cfg["email"] = {}
    if "runtime" not in cfg:
        cfg["runtime"] = {}
    if "ai" not in cfg:
        cfg["ai"] = {}

    for env_key, (section, subkey) in env_mappings.items():
        val = os.getenv(env_key)
        if val is not None:
            if subkey == "smtp_port":
                try:
                    val = int(val)
                except ValueError:
                    val = 587
            elif subkey == "dry_run":
                val = str(val).lower() in ("true", "1", "yes")
            # If gemini key was already found from GEMINI_API_KEY, don't overwrite with None from GOOGLE_API_KEY
            if subkey == "gemini_api_key" and cfg.get("ai", {}).get("gemini_api_key"):
                continue
            cfg[section][subkey] = val

    # Defaults
    if "service" not in cfg["email"]:
        cfg["email"]["service"] = "resend" if cfg["email"].get("resend_api_key") else "smtp"
    if "from_address" not in cfg["email"]:
        cfg["email"]["from_address"] = "Management Intelligence <briefing@resend.dev>"
    if "log_level" not in cfg["runtime"]:
        cfg["runtime"]["log_level"] = "INFO"
    if "dry_run" not in cfg["runtime"]:
        cfg["runtime"]["dry_run"] = False

    return cfg
