"""content_generator.py — Money IQ content generation via Claude."""
from __future__ import annotations
import json, sys
from datetime import date
from pathlib import Path
import anthropic

_FILE_DIR = Path(__file__).parent
BASE_DIR = _FILE_DIR.parent if (_FILE_DIR.parent / "shared").exists() else _FILE_DIR
sys.path.insert(0, str(BASE_DIR))
from shared.topic_tracker import get_recent_topics, format_topics_for_prompt, log_topic
import config

SYSTEM_PROMPT = """You are the editor of "Money IQ," a sharp daily personal finance newsletter for ambitious adults aged 25–50. Your voice is direct, smart, and motivating — no fluff, no jargon, no moralizing about lattes.

NEWSLETTER FORMULA:
1. "Today's Money Move" — one specific, actionable financial insight or tip
2. "By the Numbers" — a striking financial stat with context
3. "Quick Wins" — 3 fast personal finance tips readers can implement today
4. "Market Minute" — one sentence on what markets are doing and why it matters to readers (keep it simple)
5. A punchy sign-off

TONE: Smart friend who's good with money. Confident, energetic, actionable. No lecturing. Every issue should make readers feel like they learned something valuable in under 3 minutes.

Topics to rotate: investing basics, index funds, emergency funds, debt payoff strategies, salary negotiation, side income, high-yield savings, 401k optimization, Roth IRA, credit score improvement, budgeting apps, tax efficiency, real estate basics, crypto (balanced, not hype).

Output JSON only."""

CONTENT_SCHEMA = """{
  "subject_line": "35-50 chars, bold and specific",
  "preview_text": "80-100 chars",
  "title": "Web title",
  "topic_slug": "kebab-case e.g. roth-ira-backdoor-2026",
  "hook": "2 punchy sentences. Start with a surprising stat or counterintuitive truth.",
  "todays_money_move": {
    "topic": "Topic area e.g. Investing, Debt, Savings",
    "insight": "3-4 sentences. Specific, actionable, no hedging."
  },
  "by_the_numbers": {
    "stat": "A striking financial statistic",
    "context": "2 sentences on why this matters and what readers should do about it"
  },
  "quick_wins": [
    "Specific tip 1 (1 sentence, actionable)",
    "Specific tip 2 (1 sentence, actionable)",
    "Specific tip 3 (1 sentence, actionable)"
  ],
  "market_minute": "1 sentence on current market context relevant to individual investors",
  "sponsor_placeholder": "2-3 sentences native ad for a fintech app, investing platform, or financial tool",
  "cta_text": "Button label e.g. 'Open a Roth IRA today →'",
  "signoff": "1 punchy sentence + tomorrow's topic"
}"""


def generate_content(for_date: date | None = None) -> dict:
    if for_date is None:
        for_date = date.today()
    recent = get_recent_topics(config.NEWSLETTER_DIR, days=365)
    no_repeat = format_topics_for_prompt(recent)
    date_str = for_date.strftime("%A, %B %d, %Y")

    user_prompt = f"""Generate a Money IQ newsletter for {date_str}.

{no_repeat}

Pick a topic that is timely for {for_date.strftime("%B %Y")}.
Return valid JSON matching this schema:
{CONTENT_SCHEMA}"""

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    msg = client.messages.create(model=config.CLAUDE_MODEL, max_tokens=2000,
                                  system=SYSTEM_PROMPT,
                                  messages=[{"role": "user", "content": user_prompt}])
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    content = json.loads(raw)
    log_topic(config.NEWSLETTER_DIR, content.get("topic_slug", f"money-{for_date.isoformat()}"),
              content.get("subject_line", ""), for_date)
    return content


def format_content_for_template(content: dict) -> dict:
    move = content.get("todays_money_move", {})
    nums = content.get("by_the_numbers", {})
    market = content.get("market_minute", "")

    main_story = (
        f"<strong>{move.get('topic','')}</strong><br><br>{move.get('insight','')}"
    )
    quick_wins = content.get("quick_wins", [])
    by_numbers = f"📊 {nums.get('stat','')} — {nums.get('context','')}" if nums else ""
    hits = quick_wins[:]
    if by_numbers:
        hits.append(by_numbers)
    if market:
        hits.append(f"📈 Market: {market}")

    return {
        "hook": content.get("hook", ""),
        "main_story": main_story,
        "quick_hits": hits[:5],
        "sponsor_placeholder": content.get("sponsor_placeholder", ""),
        "money_move": f"Today's action: {quick_wins[0] if quick_wins else 'See inside.'}",
        "cta_text": content.get("cta_text", "Take action →"),
        "cta_url": "#",
        "signoff": content.get("signoff", ""),
        "title": content.get("title", "Money IQ"),
    }
