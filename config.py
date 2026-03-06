"""config.py — Money IQ newsletter configuration."""
import os
from dotenv import load_dotenv
load_dotenv(override=True)

NEWSLETTER_NAME        = "Money IQ"
NEWSLETTER_DIR         = "money-iq"
TAGLINE                = "Sharp personal finance for ambitious adults"
SEND_HOUR              = 8
SEND_MINUTE            = 0
TIMEZONE               = "America/New_York"
ANTHROPIC_API_KEY      = os.getenv("ANTHROPIC_API_KEY", "")
BEEHIIV_API_KEY        = os.getenv("MONEY_IQ_BEEHIIV_API_KEY", os.getenv("BEEHIIV_API_KEY", ""))
BEEHIIV_PUBLICATION_ID = os.getenv("MONEY_IQ_BEEHIIV_PUBLICATION_ID", "")
CLAUDE_MODEL           = "claude-sonnet-4-5"

def validate():
    missing = [k for k, v in {
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "MONEY_IQ_BEEHIIV_API_KEY": BEEHIIV_API_KEY,
        "MONEY_IQ_BEEHIIV_PUBLICATION_ID": BEEHIIV_PUBLICATION_ID,
    }.items() if not v]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")
