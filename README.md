# chatbot

# CryptoBuddy – Rule-Based + Real-Time Cryptocurrency Advisor Chatbot

**CryptoBuddy** is a friendly, rule-based Python chatbot that:
- Fetches live cryptocurrency data (price change and market cap) from the CoinGecko API.
- Uses simple if-else logic and predefined sustainability scores to recommend coins based on profitability **and** sustainability.
- Employs basic NLP (via NLTK tokenization + stemming) to understand variations of user queries (e.g., “sustainable,” “eco-friendly,” “trending,” etc.).

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites & Dependencies](#prerequisites--dependencies)  
3. [Installation](#installation)  
4. [Running CryptoBuddy](#running-cryptobuddy)  
5. [Supported Queries & Examples](#supported-queries--examples)  
6. [How It Works](#how-it-works)  
7. [Extending / Customization](#extending--customization)  
8. [Troubleshooting](#troubleshooting)  
9. [Project Structure](#project-structure)  
10. [License](#license)  

---

## Features

- **Real-Time Data (CoinGecko)**  
  - Automatically fetches live 24-hour price change percentages and raw market cap (USD) for each tracked coin.  
  - Categorizes price trend as “rising,” “stable,” or “falling” (based on ±1% threshold).  
  - Categorizes market cap as “high” (≥ \$50B), “medium” (\$10B–\$50B), or “low” (< \$10B).

- **Sustainability Scores (Static)**  
  - Each coin has a preset “energy_use” label (high/medium/low) and a `sustainability_score` (0.0–1.0).  
  - Functions can recommend the coin with the highest sustainability.

- **Rule-Based Recommendations**  
  - **Most Sustainable**: Recommends the coin with the highest `sustainability_score`.  
  - **High-Profit**: Filters for coins where `price_trend == "rising"` AND `market_cap == "high"`. If multiple match, breaks ties by higher sustainability score.  
  - **Compare Two Coins**: Displays side-by-side live stats (price trend, market cap category, 24-hour change %, sustainability) for any two user-specified coins.

- **Basic NLP (NLTK)**  
  - Tokenizes and stems user inputs to catch synonyms and variants:
    - “sustainability,” “sustainable,” “ecofriendly” → stem “sustain” or “ecofriendl”
    - “trending,” “trend,” “upward” → stem “trend”
    - “compare,” “vs,” “vs.”, etc.  
  - Makes it more robust against varied phrasing.

- **Help & Fallback**  
  - Typing `help` or `commands` prints usage hints.  
  - Unknown queries trigger a friendly fallback that suggests valid question formats.

- **Graceful Exit**  
  - Typing `exit`, `quit`, or `bye` ends the chat with a goodbye message.

---

## Prerequisites & Dependencies

- **Python 3.7+** (recommended: 3.8, 3.9, 3.10, or newer)
- **Virtual Environment** (strongly recommended to isolate dependencies)

### Python Packages

- `requests` – For making HTTP requests to CoinGecko  
- `nltk` – For tokenization and stemming  

These can be installed via `pip`.  

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Daves-devspace/chatbot.git
   cd chatbot

2. Create & Activate a Virtual Environment

Linux/macOS

bash

python3 -m venv venv
source venv/bin/activate
Windows (PowerShell)

powershell

python -m venv venv
venv\Scripts\Activate.ps1

3. Install Dependencies


pip install -r requirements.txt
If you don’t have a requirements.txt, you can run:

bash

pip install requests nltk
4. Download NLTK Tokenizer Data
In a Python REPL (while the venv is active), run:

python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('punkt_tab')
>>> exit()
This ensures word_tokenize will work without errors.

Running CryptoBuddy
Once dependencies are installed and NLTK data is downloaded, simply run:

bash
python smart_crypto.py
You should see:

CryptoBuddy: Hey there! I’m CryptoBuddy, your AI-powered crypto sidekick! 🌟
CryptoBuddy: Ask me things like 'Which crypto is trending up?' or 'Most sustainable coin?'.
Now type your questions at the You: prompt. To exit, type exit, quit, or bye.

Supported Queries & Examples
1. Which crypto is trending up?

User: Which crypto is trending up?

Bot (sample):

🤖 CryptoBuddy: Cardano is trending rising (24h change: 2.45%) 
with a high market cap (≈ $12,345,678,900). Its sustainability_score is 8/10—win-win! 🚀
What’s the most sustainable coin?

2. User: What’s the most sustainable coin?

Bot (sample):

🤖 CryptoBuddy: I recommend Cardano (sustainability score: 8/10). 
It’s eco-friendly and has long-term potential! 🍃
Compare two coins

3. User: Compare Bitcoin vs Ethereum

Bot (sample):

🤖 CryptoBuddy: Here’s a quick comparison:
- Bitcoin: price_trend=rising (24h change: 1.12%), market_cap=high, sustainability=3/10.
- Ethereum: price_trend=stable (24h change: 0.05%), market_cap=high, sustainability=6/10.
👉🏻 Both are high-market-cap, and Bitcoin is rising, but Ethereum has a higher sustainability score!
List all tracked coins

4. User: List all coins

Bot:

🤖 CryptoBuddy: Currently I track: Bitcoin, Ethereum, Cardano, Polkadot.
5. Help Menu

User: help or commands

Bot:

🤖 CryptoBuddy Help:
- Ask 'Which crypto is trending up?' or 'What’s the most sustainable coin?'
- Ask 'Compare Bitcoin vs Cardano'
- Ask 'List all coins' to see all options
- Type 'exit' or 'quit' to leave
- 
6. Fallback (unrecognized)

User: Hey, best

Bot (sample):

🤖 CryptoBuddy: I’m not quite sure what you mean. Try:
- 'Which crypto is trending up?'
- 'Most sustainable coin?'
- 'Compare Ethereum vs Cardano'
- 'List all coins'
- 'Help'
  
How It Works
1. Predefined Sustainability Database (SUSTAINABILITY_DB)

Holds “energy_use” and sustainability_score for each tracked coin (static, since CoinGecko does not provide energy/eco metrics).

Example entry:

python
SUSTAINABILITY_DB = {
    "Cardano": {"energy_use": "low", "sustainability_score": 8.0/10},
    # …etc…
}

2. CoinGecko ID Mapping (COIN_ID_MAP)

Maps friendly names (e.g., "Bitcoin") to CoinGecko API IDs (e.g., "bitcoin").

Used to fetch real-time market data.

3. get_coin_data(coin_name)

Fetches JSON from https://api.coingecko.com/api/v3/coins/{coin_id}.

Extracts:

price_change_percentage_24h → categorizes as “rising”/“falling”/“stable”

market_cap["usd"] → categorizes as “high”/“medium”/“low”

Merges these with static SUSTAINABILITY_DB values (energy use, sustainability score).

Returns a unified dict:


{
  "price_trend": "rising",
  "market_cap": "high",
  "energy_use": "low",
  "sustainability_score": 0.8,
  "price_change_24h": 2.35,
  "market_cap_usd": 12_345_678_900
}

4. NLP Preprocessing (normalize_query)

Uses nltk.tokenize.word_tokenize + PorterStemmer to convert user input into a list of stems.

Allows matching “sustain,” “sustainability,” “sustainable,” “eco,” “eco-friendly,” etc., all to the same root.

5. Recommendation Logic

Most Sustainable: Pick coin with highest sustainability_score.

High Profit: Filter down to coins where price_trend == "rising" AND market_cap == "high". If more than one, pick the highest sustainability_score.

Compare: If user mentions two valid coin names, fetch each coin’s real-time stats and print a side-by-side summary.

6. Main Loop (run_chatbot)

Prints a greeting.

Repeatedly:

Prompts You:

Converts input to stems

Matches stems against rule categories (sustainability, trend, compare, list, help)

Prints a formatted response (tagged with 🤖 CryptoBuddy:)

On exit / quit / bye, prints a goodbye and ends.

Extending / Customization

Add More Coins

Extend COIN_ID_MAP and SUSTAINABILITY_DB with additional coin names and their corresponding CoinGecko IDs and static eco-metrics.

Example:


COIN_ID_MAP["Solana"] = "solana"
SUSTAINABILITY_DB["Solana"] = {"energy_use": "low", "sustainability_score": 7.5/10}
Refine Categorization Thresholds

Edit categorize_price_trend(pct_change_24h) to use different percentage thresholds.

Adjust categorize_market_cap(market_cap_usd)—e.g., raise/lower the $10 B / $50 B boundaries based on current market conditions.

More NLP Variants

Incorporate wordnet synsets or a small custom list of synonyms (e.g., “go green,” “eco-conscious,” “greenest coin,” “pump,” “moon,” etc.).

Use fuzzy string matching (e.g., via difflib.get_close_matches) to catch typos like “bitcon” → “bitcoin.”

Caching / Rate Limiting

CoinGecko enforces a free tier rate limit (~50 calls/minute).

You can cache the last‐fetched get_coin_data(...) results for 30–60 seconds to avoid repeated API calls when users ask multiple questions in quick succession.

Plotting Price Trends

If you wish to display a small 7-day price chart, you could:

Fetch market_data["sparkline_7d"]["price"] from CoinGecko.

Use python_user_visible + matplotlib to generate and display a PNG chart.

Troubleshooting
LookupError: punkt_tab not found

Ensure you ran:

import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
Both packages must be installed in the same Python environment where you run smart_crypto.py.

Network Issues / CoinGecko

If you see HTTP errors (e.g., 429 Too Many Requests), wait 30–60 seconds and try again.

Consider adding a short time.sleep(0.5) after each user query to respect rate limits.

“NoneType” or “KeyError” When Fetching Data

If CoinGecko’s API shape changes, you may need to inspect the returned JSON.

Example: data["market_data"]["price_change_percentage_24h"] must exist; if it’s missing, handle with a default (e.g., 0.0).

Bot Doesn’t Recognize a Coin Name

Make sure the coin name (e.g., “Bitcoin”) matches exactly one of the keys in COIN_ID_MAP.

Currently, it’s case-sensitive when matching; you can convert both sides to .lower() in the comparison to be more forgiving.

Project Structure

crypto-advisor-chatbot/
├── smart_crypto.py        # Main chatbot script (with CoinGecko + NLTK)
├── requirements.txt       # e.g.: requests>=2.32.3, nltk>=3.9.1
├── README.md              # (this file)
└── screenshots/           # (optional) Example conversation screenshots
    ├── trending_example.png
    └── compare_example.png
smart_crypto.py

Contains the full Python code:

NLTK data checks/download

NLP normalization

CoinGecko API fetching & categorization

Recommendation & comparison logic

Main chatbot loop

requirements.txt


requests>=2.32.3
nltk>=3.9.1

screenshots/ (optional)

Store PNGs or JPGs showing sample interactions, e.g.:

trending_example.png (user asks “Which crypto is trending up?”)

sustainability_example.png (user asks “Most sustainable coin?”)

compare_example.png (user asks “Compare Bitcoin vs Cardano”)

License
This project is released under the MIT License. See LICENSE for details.



smart_crypto.py using the real api response is as follows:
![Screenshot from 2025-05-31 10-47-20](https://github.com/user-attachments/assets/9b813bdf-a7ba-4b2b-8b97-c282bfec4ebc)
