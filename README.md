# Бот-помощник для детей и родителей, которые хотят защитить свои цифровые данные и ознакомиться с профилактикой предотвращения кибербуллинга.
# Cyber Safety Assistant Bot

A Telegram chatbot designed to assist children and parents in understanding and preventing cyberbullying, as well as protecting their digital privacy. The bot offers educational information and supportive responses based on user queries, utilizing fuzzy text matching and a local dataset.

---

## Overview

This chatbot project:
- Answers questions about digital hygiene and cyberbullying.
- Provides information on how to remove offensive content.
- Suggests support contacts for reporting incidents.
- Uses a simple text-based Q&A system with fuzzy search.
- Saves chat history for future reference.

---

##  Technologies Used

- Python
- Telegram Bot API
- FuzzyWuzzy (for text matching)
- NLTK (tokenization and text preprocessing)
- Requests (HTTP API interaction)
- Dataset stored in plain `.txt` format

---

## Project Structure

- `main.py` — Main bot logic with message handling and response generation.
- `tbot_dataset.txt` — Question-answer dataset used for response matching.
- `requirements.txt` — List of required Python packages.
- `.idea/` — Project settings (for IDEs like PyCharm).
- `README.md` — Documentation for the project.

---

## Bot Features

- Greets users and explains its purpose upon `/start`
- Matches user questions to known answers using FuzzyWuzzy
- If no exact match is found, performs token-based comparison
- Logs every chat interaction to a file named after the user
- Responds only to text messages

---

## How to Run

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure to update the bot token in `main.py`:
   ```python
   token = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

5. Run the bot:
   ```bash
   python main.py
   ```

---

## Notes

- The bot uses `fuzzywuzzy.fuzz.partial_ratio` with a threshold (`rate`) to determine response relevance.
- Responses are fetched from the `tbot_dataset.txt` file. Format expected:
  ```
  вопрос: How can I report cyberbullying? ответ: You can report it to [organization/contact].
  ```


