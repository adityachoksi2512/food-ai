# Food AI 🤌

An AI-powered restaurant ordering chatbot built with Python, Flask, and Claude API.

## Demo
▶️ [Watch the Food AI Demo](https://drive.google.com/file/d/1ztoSyY8g0BwWSHaDI0R6pNJqER5d3do7/view?usp=drive_link)

## Features
- Real-time streaming responses
- Live order cart with automatic updates
- Voice input via Web Speech API
- Dietary filters (Vegetarian, Vegan, Gluten-Free)
- Order type selection (Dine In, Pickup, Delivery)
- Order status tracker
- Loyalty points system
- Printable receipt

## Tech Stack
- Python + Flask (backend)
- Claude API with Server-Sent Events (streaming)
- Web Speech API (voice input)
- Vanilla HTML/CSS/JS (frontend)

## Setup
1. Clone the repo
2. Run `pip install flask anthropic`
3. Add your Anthropic API key to `app.py`
4. Run `python app.py`
5. Open http://localhost:5000
