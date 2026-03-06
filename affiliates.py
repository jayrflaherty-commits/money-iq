"""affiliates.py — Affiliate links for Money IQ newsletter."""
from __future__ import annotations
from datetime import date
from typing import Optional

AMAZON_ASSOCIATE_TAG = "retirehub09-20"

AFFILIATE_LINKS = {
    "investing_app": {
        "name": "Acorns — invest your spare change",
        "description": "Round up your everyday purchases and invest the difference automatically — start with $5",
        "cta": "Start investing →",
        "url": "https://YOUR_ACORNS_AFFILIATE_LINK_HERE",
        # Acorns via Impact | Commission: $5–15/signup
    },
    "credit_cards": {
        "name": "NerdWallet — find the best card",
        "description": "Compare 100+ credit cards in 60 seconds — find the highest rewards for your spending",
        "cta": "Compare cards →",
        "url": "https://YOUR_NERDWALLET_AFFILIATE_LINK_HERE",
        # NerdWallet via CJ | Commission: $50–200 per approved card
    },
    "banking": {
        "name": "Chime — no-fee online banking",
        "description": "No monthly fees, no minimums, no overdraft fees — plus get paid up to 2 days early",
        "cta": "Open free account →",
        "url": "https://YOUR_CHIME_AFFILIATE_LINK_HERE",
        # Chime via Impact or direct | Commission: $30–50/account
    },
    "loans": {
        "name": "Credible — compare personal loan rates",
        "description": "Check rates from 17 lenders in 2 minutes — no hard credit pull to compare",
        "cta": "Check my rate →",
        "url": "https://YOUR_CREDIBLE_AFFILIATE_LINK_HERE",
        # Credible via CJ or Impact | Commission: $30–100/lead
    },
    "books": {
        "name": "Top money books on Amazon",
        "description": "The books our editors actually recommend for building wealth",
        "cta": "Browse the list →",
        "url": f"https://www.amazon.com/s?k=personal+finance+books+bestsellers&tag={AMAZON_ASSOCIATE_TAG}",
    },
}

CATEGORY_ORDER = list(AFFILIATE_LINKS.keys())

def get_daily_affiliate(for_date: date | None = None) -> dict:
    if for_date is None:
        for_date = date.today()
    key = CATEGORY_ORDER[for_date.toordinal() % len(CATEGORY_ORDER)]
    affiliate = AFFILIATE_LINKS[key].copy()
    affiliate["category"] = key
    return affiliate

def get_amazon_link(asin: str) -> str:
    return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"
