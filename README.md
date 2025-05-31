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
   git clone https://github.com/yourusername/crypto-advisor-chatbot.git
   cd crypto-advisor-chatbot


smart_crypto.py using the real api response is as follws:
![Screenshot from 2025-05-31 10-47-20](https://github.com/user-attachments/assets/9b813bdf-a7ba-4b2b-8b97-c282bfec4ebc)
