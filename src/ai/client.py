import os
import json
import re
import time
import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


def clean_json_text(text: str) -> str:
    """Strip markdown codeblocks and extra whitespace from LLM output."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()


class AIClient:
    """Unified client supporting Google Gemini and OpenAI-compatible providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ai_cfg = config.get("ai", {})
        self.provider = self.ai_cfg.get("provider", "gemini").lower()
        self.model = self.ai_cfg.get("model", "gemini-2.5-flash")
        self.gemini_api_key = self.ai_cfg.get("gemini_api_key") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = self.ai_cfg.get("openai_api_key") or os.getenv("OPENAI_API_KEY")

    def generate_intelligence(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generate structured intelligence briefing JSON with automatic retry."""
        if self.provider == "gemini" or (not self.openai_api_key and self.gemini_api_key):
            return self._call_gemini(system_prompt, user_prompt)
        elif self.openai_api_key:
            return self._call_openai(system_prompt, user_prompt)
        else:
            raise ValueError(
                "No valid AI API key found! Please set GEMINI_API_KEY (recommended free tier) "
                "or OPENAI_API_KEY in your environment or GitHub Secrets."
            )

    def _call_gemini(self, system_prompt: str, user_prompt: str, retries: int = 3) -> Dict[str, Any]:
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        # Try google-genai SDK first if available
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.gemini_api_key)
            # Try configured model, fallback to gemini-2.5-flash if needed
            candidate_models = [self.model, "gemini-2.5-flash", "gemini-1.5-flash"]
            
            last_err = None
            for m in candidate_models:
                try:
                    logger.info(f"Calling Gemini SDK with model {m}...")
                    response = client.models.generate_content(
                        model=m,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.2,
                            response_mime_type="application/json"
                        )
                    )
                    text = response.text
                    if text:
                        cleaned = clean_json_text(text)
                        return json.loads(cleaned)
                except Exception as e:
                    logger.warning(f"Gemini SDK call failed for {m}: {e}")
                    last_err = e
        except Exception as e:
            logger.info(f"Using direct REST fallback for Gemini: {e}")

        # Direct REST API fallback for rock-solid stability
        url_models = [self.model, "gemini-2.5-flash", "gemini-1.5-flash"]
        for attempt in range(retries):
            for m in url_models:
                api_url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
                    f"?key={self.gemini_api_key}"
                )
                payload = {
                    "system_instruction": {
                        "parts": [{"text": system_prompt}]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": user_prompt}]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.2,
                        "responseMimeType": "application/json"
                    }
                }
                headers = {"Content-Type": "application/json"}
                try:
                    resp = requests.post(api_url, headers=headers, json=payload, timeout=90)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            cleaned = clean_json_text(raw_text)
                            return json.loads(cleaned)
                    elif resp.status_code in (429, 503):
                        logger.warning(f"Rate limited or server error ({resp.status_code}) on {m}. Waiting before retry...")
                        time.sleep(2 ** (attempt + 1))
                    else:
                        logger.warning(f"Gemini REST error {resp.status_code} on {m}: {resp.text}")
                except Exception as ex:
                    logger.warning(f"Request exception on {m}: {ex}")

        raise RuntimeError("Failed to obtain response from Gemini API after multiple retries.")

    def _call_openai(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config.get("ai", {}).get("openai_model", "gpt-4o-mini"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        resp = requests.post(api_url, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
        res_data = resp.json()
        raw_text = res_data["choices"][0]["message"]["content"]
        return json.loads(clean_json_text(raw_text))
