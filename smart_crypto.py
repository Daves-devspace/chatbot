# crypto_advisor.py

"""
CryptoBuddy – Rule-Based + Real-Time Cryptocurrency Advisor Chatbot

Stretch Goals implemented:
  A) Real-Time price & market_cap from CoinGecko API (no API key needed)
  B) Simple NLP (tokenize + stem) via NLTK to catch synonyms/variants
  
  
"""
import nltk

# ---------------------------------------------------------
# Check for ‘punkt’ and download it if it’s not already there
# ---------------------------------------------------------
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK ‘punkt’ not found. Downloading…")
    nltk.download('punkt')

# ---------------------------------------------------------
# (the rest of your imports and code follow)
# ---------------------------------------------------------

import sys
import time
import requests
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

# ------------------------------------------------------------------------------
# 0. Instructions / Dependencies:
#
# 1) Make sure you have Python 3.x installed.
# 2) Install required packages:
#      pip install requests nltk
#
# 3) Before running for the first time, you’ll need NLTK’s 'punkt' model:
#      >>> import nltk
#      >>> nltk.download('punkt')
#
# 4) Run the chatbot:
#      python crypto_advisor.py
#
# ------------------------------------------------------------------------------
# Note on CoinGecko usage:
#  - We map our coin names (e.g., "Bitcoin") to CoinGecko IDs ("bitcoin").
#  - We fetch real-time 'price_change_percentage_24h' and 'market_cap' in USD.
#  - Based on price change (>0 → “rising”, <0 → “falling”, abs≈0 → “stable”),
#    and based on market cap thresholds to categorize high/medium/low.
# ------------------------------------------------------------------------------
#                                  SETUP
# ------------------------------------------------------------------------------

# 1. Personali ty / Bot metadata
BOT_NAME = "CryptoBuddy"
BOT_TONE = "Friendly"

# 2. NLTK Stemmer setup
stemmer = PorterStemmer()

def normalize_query(q: str):
    """
    Tokenize + stem the user query to catch word variants:
      - “sustainable”, “sustainability”, “eco-friendly” → stems to “sustain”, “ecofriendl”
      - “trending”, “trend”, “upward” → stems accordingly
    """
    tokens = word_tokenize(q.lower())
    stems = [stemmer.stem(tok) for tok in tokens]
    return stems

# 3. CoinGecko ID mapping for each coin we track
#   (CoinGecko uses lowercase IDs, e.g. "bitcoin", "ethereum", "cardano")
COIN_ID_MAP = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Cardano": "cardano",
    "Polkadot": "polkadot"
}

# 4. Hard-coded sustainability data (energy_use + sustainability_score out of 10)
#    Since CoinGecko does not provide “energy_use” or “sustainability_score” directly,
#    we keep a separate small dict for those attributes.
SUSTAINABILITY_DB = {
    "Bitcoin":    {"energy_use": "high",   "sustainability_score": 3.0 / 10},
    "Ethereum":   {"energy_use": "medium", "sustainability_score": 6.0 / 10},
    "Cardano":    {"energy_use": "low",    "sustainability_score": 8.0 / 10},
    "Polkadot":   {"energy_use": "low",    "sustainability_score": 7.0 / 10}
}

# ------------------------------------------------------------------------------
#                                 HELPER FUNCTIONS
# ------------------------------------------------------------------------------

def fetch_from_coingecko(coin_id: str):
    """
    Fetch full coin data from CoinGecko (free, no API key needed).
    Returns the parsed JSON (dict). If something fails, returns None.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    try:
        response = requests.get(url, params={"localization": "false",
                                             "tickers": "false",
                                             "market_data": "true",
                                             "community_data": "false",
                                             "developer_data": "false",
                                             "sparkline": "false"})
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching {coin_id} from CoinGecko: {e}")
        return None

def categorize_market_cap(market_cap_usd: float):
    """
    Convert a raw market cap (in USD) to "high", "medium", or "low" categories.
    Thresholds (example):
      - High   : > 50 billion USD
      - Medium : 10 billion – 50 billion
      - Low    : < 10 billion
    """
    if market_cap_usd >= 50_000_000_000:
        return "high"
    elif market_cap_usd >= 10_000_000_000:
        return "medium"
    else:
        return "low"

def categorize_price_trend(pct_change_24h: float):
    """
    Given a percentage change in the last 24h, return "rising", "falling", or "stable".
      - If pct_change_24h > 1.0% → "rising"
      - If pct_change_24h < -1.0% → "falling"
      - Otherwise → "stable"
    (Thresholds can be adjusted as needed.)
    """
    if pct_change_24h > 1.0:
        return "rising"
    elif pct_change_24h < -1.0:
        return "falling"
    else:
        return "stable"

def get_coin_data(coin_name: str):
    """
    Combines real-time data from CoinGecko with our static sustainability DB.
    Returns a dict with:
      {
        "price_trend":     "rising"/"stable"/"falling",
        "market_cap":      "high"/"medium"/"low",
        "energy_use":      <from SUSTAINABILITY_DB>,
        "sustainability_score": <from SUSTAINABILITY_DB> (float out of 1),
        "price_change_24h": <raw pct_change float>,
        "market_cap_usd":   <raw USD float>
      }
    If any fetch fails, returns None.
    """
    coin_id = COIN_ID_MAP.get(coin_name)
    if not coin_id:
        return None

    data = fetch_from_coingecko(coin_id)
    if data is None or "market_data" not in data:
        return None

    md = data["market_data"]
    # Extract 24h price change percentage (float) and raw market cap USD
    pct_change_24h = md.get("price_change_percentage_24h", 0.0)
    market_cap_usd = md.get("market_cap", {}).get("usd", 0.0)

    # Categorize them
    price_trend = categorize_price_trend(pct_change_24h)
    market_cap_cat = categorize_market_cap(market_cap_usd)

    # Merge with static sustainability info
    sust_info = SUSTAINABILITY_DB.get(coin_name, {})
    energy_use = sust_info.get("energy_use", "unknown")
    sustainability_score = sust_info.get("sustainability_score", 0.0)

    return {
        "price_trend": price_trend,
        "market_cap": market_cap_cat,
        "energy_use": energy_use,
        "sustainability_score": sustainability_score,
        "price_change_24h": pct_change_24h,
        "market_cap_usd": market_cap_usd
    }

# ------------------------------------------------------------------------------
#                           RECOMMENDATION FUNCTIONS
# ------------------------------------------------------------------------------

def recommend_most_sustainable():
    """
    Among tracked coins, pick the one with highest sustainability_score (out of 1).
    Returns: (coin_name, score_out_of_10)
    """
    best_coin = max(SUSTAINABILITY_DB.keys(),
                    key=lambda c: SUSTAINABILITY_DB[c]["sustainability_score"])
    score_frac = SUSTAINABILITY_DB[best_coin]["sustainability_score"]
    score_10 = round(score_frac * 10)
    return best_coin, score_10

def recommend_high_profit():
    """
    Among tracked coins, fetch real-time data and pick those with:
      price_trend == "rising" AND market_cap == "high".
    If multiple, return the one with the highest sustainability_score.
    Returns coin_name or None if none match.
    """
    candidates = []
    for coin in COIN_ID_MAP.keys():
        info = get_coin_data(coin)
        if info is None:
            continue
        if info["price_trend"] == "rising" and info["market_cap"] == "high":
            candidates.append(coin)

    if not candidates:
        return None

    # Among candidates, pick the highest sustainability_score
    best = max(candidates,
               key=lambda c: SUSTAINABILITY_DB.get(c, {}).get("sustainability_score", 0.0))
    return best

# ------------------------------------------------------------------------------
#                           CHATBOT RESPONSE LOGIC
# ------------------------------------------------------------------------------

def chatbot_response(user_query: str) -> str:
    """
    Use simple stems (NLP) to match keywords to tasks:
      - “sustain” / “eco” → recommend most sustainable coin
      - “trend” / “profit” / “long-term” → recommend high-profit coin
      - “compare” or “vs” → compare two coins’ real-time stats
      - “list” / “show” → list all tracked coins
      - “help” / “commands” → show help menu
    """
    stems = normalize_query(user_query)

    # 1. SUSTAINABILITY
    if "sustain" in stems or "eco" in stems or "green" in stems:
        coin, score10 = recommend_most_sustainable()
        return (f"🤖 {BOT_NAME}: I recommend **{coin}** (sustainability score: {score10}/10). "
                f"It’s eco-friendly and has long-term potential! 🍃")

    # 2. PROFITABILITY / TREND
    if "trend" in stems or "profit" in stems or "longterm" in stems or "long" in stems:
        best_coin = recommend_high_profit()
        if best_coin:
            data = get_coin_data(best_coin)
            # Round price_change_24h & format market cap
            pct = round(data["price_change_24h"], 2)
            mc_usd = data["market_cap_usd"]
            mc_cat = data["market_cap"]
            sust10 = round(data["sustainability_score"] * 10)
            return (f"🤖 {BOT_NAME}: **{best_coin}** is trending **{data['price_trend']}** "
                    f"(24h change: {pct}%) with a **{mc_cat}** market cap "
                    f"(≈ ${mc_usd:,.0f}). Its sustainability_score is {sust10}/10—win-win! 🚀")
        else:
            return (f"🤖 {BOT_NAME}: I don’t see any coin that’s both ‘rising’ and ‘high’ market cap right now. "
                    f"Maybe consider checking again later?")

    # 3. COMPARE two coins
    #    Look for “vs” or “compare” in stems
    if "vs" in stems or "compar" in stems:
        # Basic logic: find any two valid coin names in the user_query (case-insensitive)
        found = [coin for coin in COIN_ID_MAP.keys()
                 if coin.lower() in user_query.lower()]
        if len(found) >= 2:
            c1, c2 = found[0], found[1]
            d1 = get_coin_data(c1)
            d2 = get_coin_data(c2)
            if d1 is None or d2 is None:
                return f"🤖 {BOT_NAME}: Sorry, I couldn’t fetch real-time data for one of those coins."

            # Format each coin’s stats
            pct1 = round(d1["price_change_24h"], 2)
            pct2 = round(d2["price_change_24h"], 2)
            mc1 = d1["market_cap"]
            mc2 = d2["market_cap"]
            sust1 = round(d1["sustainability_score"] * 10)
            sust2 = round(d2["sustainability_score"] * 10)

            resp = (f"🤖 {BOT_NAME}: Here’s a quick comparison:\n"
                    f"- {c1}: price_trend={d1['price_trend']} (24h change: {pct1}%), "
                    f"market_cap={mc1}, sustainability={sust1}/10.\n"
                    f"- {c2}: price_trend={d2['price_trend']} (24h change: {pct2}%), "
                    f"market_cap={mc2}, sustainability={sust2}/10.\n")
            # Simple “tie-breaker” on sustainability if both rising
            if d1["price_trend"] == "rising" and d2["price_trend"] == "rising":
                better = c1 if d1["sustainability_score"] > d2["sustainability_score"] else c2
                resp += f"👉🏻 Both are rising, but {better} has a higher sustainability score!"
            return resp
        else:
            return f"🤖 {BOT_NAME}: I need two valid coin names to compare (e.g., ‘Compare Bitcoin vs Cardano’)."

    # 4. LIST ALL COINS
    if "list" in stems or "show" in stems:
        names = ", ".join(COIN_ID_MAP.keys())
        return f"🤖 {BOT_NAME}: Currently I track: {names}."

    # 5. HELP / COMMANDS
    if "help" in stems or "command" in stems:
        return (
            f"🤖 {BOT_NAME} Help:\n"
            f"- Ask 'Which crypto is trending up?' or 'What’s the most sustainable coin?'\n"
            f"- Ask 'Compare Bitcoin vs Cardano'\n"
            f"- Ask 'List all coins' to see all options\n"
            f"- Type 'exit' or 'quit' to leave\n"
        )

    # 6. FALLBACK
    return (f"🤖 {BOT_NAME}: I’m not quite sure what you mean. Try:\n"
            f"- 'Which crypto is trending up?'\n"
            f"- 'Most sustainable coin?'\n"
            f"- 'Compare Ethereum vs Cardano'\n"
            f"- 'List all coins'\n"
            f"- 'Help'\n")

# ------------------------------------------------------------------------------
#                              MAIN CHATBOT LOOP
# ------------------------------------------------------------------------------

def greet_user():
    print(f"{BOT_NAME}: Hey there! I’m {BOT_NAME}, your AI-powered crypto sidekick! 🌟")
    print(f"{BOT_NAME}: Ask me things like 'Which crypto is trending up?' or 'Most sustainable coin?'.\n")

def run_chatbot():
    greet_user()
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"{BOT_NAME}: Bye! Happy—and informed—investing! 👋")
                sys.exit(0)
            response = chatbot_response(user_input)
            print(response + "\n")
            # Be polite with CoinGecko’s rate limits
            time.sleep(0.5)
        except KeyboardInterrupt:
            print(f"\n{BOT_NAME}: Bye! Happy investing! 👋")
            sys.exit(0)

if __name__ == "__main__":
    run_chatbot()
