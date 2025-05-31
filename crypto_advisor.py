import sys

# 1. Predefined crypto database
crypto_db = {
    "Bitcoin": {
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3.0 / 10
    },
    "Ethereum": {
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6.0 / 10
    },
    "Cardano": {
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8.0 / 10
    },
    "Polkadot": {
        "price_trend": "falling",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 7.0 / 10
    },
}

# 2. Chatbot personality metadata
BOT_NAME = "CryptoBuddy"
BOT_TONE = "Friendly"  # e.g., “Hey there! Let’s find you a green and growing crypto!”

def greet_user():
    """Prints a greeting when the script starts."""
    print(f"{BOT_NAME}: Hey there! I’m {BOT_NAME}. Your AI-powered crypto sidekick! 🌟")
    print(f"{BOT_NAME}: Ask me things like 'Which crypto is trending up?' or 'Most sustainable coin?'.\n")

def recommend_most_sustainable():
    """Return the coin with the highest sustainability_score."""
    recommend = max(crypto_db,
                    key=lambda coin: crypto_db[coin]["sustainability_score"])
    score = crypto_db[recommend]["sustainability_score"]
    # Convert score to a 0–10 scale if stored as fraction (already 0–1 or 0–10)
    display_score = round(score * 10) if score <= 1 else round(score)
    return recommend, display_score

def recommend_high_profit():
    """
    Return a coin that has price_trend='rising' AND market_cap='high'.
    If multiple, pick the one with the higher sustainability_score.
    """
    candidates = [
        coin for coin, data in crypto_db.items()
        if data["price_trend"] == "rising" and data["market_cap"] == "high"
    ]
    if not candidates:
        return None

    # If multiple, pick the one with max sustainability_score:
    recommend = max(candidates,
                    key=lambda coin: crypto_db[coin]["sustainability_score"])
    return recommend

def chatbot_response(user_query: str) -> str:
    """Generate a response based on the user_query string."""
    query = user_query.lower()

    # 1. Check if user wants the most sustainable coin
    if "sustain" in query or "eco" in query or "green" in query:
        coin, score = recommend_most_sustainable()
        return (f"🤖 {BOT_NAME}: I recommend **{coin}** (sustainability score: {score}/10). "
                f"It’s eco-friendly and has long-term potential!")

    # 2. Check if user asks “trending” or “profit” or “long-term growth”
    elif "trend" in query or "profit" in query or "long-term" in query:
        coin = recommend_high_profit()
        if coin:
            data = crypto_db[coin]
            return (f"🤖 {BOT_NAME}: **{coin}** is trending up (price_trend = '{data['price_trend']}') "
                    f"with a high market cap. Plus, its sustainability_score is "
                    f"{round(data['sustainability_score'] * 10)}/10—win-win! 🚀")
        else:
            return (f"🤖 {BOT_NAME}: I don’t see any coin that’s both 'rising' and 'high' market cap right now. "
                    f"Maybe consider one that’s rising or check back later!")

    # 3. Check if user asks “compare” or “what about X vs Y”
    elif " vs " in query or "compare" in query:
        # e.g. "compare bitcoin and cardano"
        # Simplest implementation: parse two coin names between spaces
        tokens = query.replace(",", "").split()
        # find coin names in our database
        found = [coin for coin in crypto_db.keys() if coin.lower() in tokens]
        if len(found) >= 2:
            c1, c2 = found[0], found[1]
            d1, d2 = crypto_db[c1], crypto_db[c2]
            resp = (f"🤖 {BOT_NAME}: Here’s a quick comparison:\n"
                    f"- {c1}: price_trend={d1['price_trend']}, "
                    f"market_cap={d1['market_cap']}, sustainability={round(d1['sustainability_score']*10)}/10.\n"
                    f"- {c2}: price_trend={d2['price_trend']}, "
                    f"market_cap={d2['market_cap']}, sustainability={round(d2['sustainability_score']*10)}/10.\n")
            # Simple recommendation: pick whichever has higher sustainability if both rising, otherwise mention both
            if d1["price_trend"] == "rising" and d2["price_trend"] == "rising":
                better = c1 if d1["sustainability_score"] > d2["sustainability_score"] else c2
                resp += f"👉🏻 Both are rising, but {better} has a higher sustainability score!"
            return resp
        else:
            return f"🤖 {BOT_NAME}: I need two valid coin names to compare (e.g., 'compare Bitcoin and Cardano')."

    # 4. If user asks “help” or “commands”
    elif "help" in query or "commands" in query:
        return (
            f"🤖 {BOT_NAME} Help:\n"
            f"- Ask 'Which crypto is trending up?' or 'What’s the most sustainable coin?'\n"
            f"- Ask 'Compare Bitcoin vs Cardano'\n"
            f"- Ask 'List all coins' to see all options\n"
        )

    # 5. List all available coins
    elif "list all" in query or "show all coins" in query:
        names = ", ".join(crypto_db.keys())
        return f"🤖 {BOT_NAME}: Currently I track: {names}."

    # 6. Fallback for unknown queries
    else:
        return (f"🤖 {BOT_NAME}: Hmm, I’m not sure I understand. Try questions like:\n"
                f"- 'Which crypto is trending up?'\n"
                f"- 'Most sustainable coin?'\n"
                f"- 'Compare Ethereum vs Cardano'\n")
        

def run_chatbot():
    """Main loop: greet the user, then continuously accept input until 'exit'."""
    greet_user()
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"{BOT_NAME}: Bye! Happy investing! 👋")
                sys.exit(0)
            response = chatbot_response(user_input)
            print(response + "\n")
        except KeyboardInterrupt:
            print(f"\n{BOT_NAME}: Bye! Happy investing! 👋")
            sys.exit(0)

if __name__ == "__main__":
    run_chatbot()