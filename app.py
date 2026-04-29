import json
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import anthropic
from menu import get_menu_text, RESTAURANT_NAME

app = Flask(__name__)

# ============================================================
#  PASTE YOUR ANTHROPIC API KEY BELOW
# ============================================================
API_KEY = "PASTE_YOUR_API_KEY_HERE"
# ============================================================

client = anthropic.Anthropic(api_key=API_KEY)

BASE_SYSTEM_PROMPT = f"""You are Bella, a friendly and enthusiastic AI ordering assistant for {RESTAURANT_NAME}.
Help customers browse the menu, answer questions about dishes, take their order, and confirm it.

Here is the full menu:
{get_menu_text()}

Guidelines:
- Be warm, friendly, and professional — light humor is welcome
- Use the customer's name occasionally to make the experience personal
- Format prices clearly with a dollar sign (e.g. $12.99)
- Never make up items or prices not on the menu
- Naturally suggest complementary items (e.g. a drink with a pizza, dessert after a main)
- When items are ordered, confirm each addition enthusiastically
- When the customer is done, provide a clear itemized order summary with the total
- To confirm an order, include the phrase "Your order is confirmed!" and wish them well

═══════════════════════════════════════════════
HIDDEN ORDER TRACKING — NEVER SHOW TO THE CUSTOMER
═══════════════════════════════════════════════
Whenever the customer's order changes (items added, removed, or modified), you MUST
append ONE line at the very end of your response in this exact format:

[ORDER]:{{"items":[{{"name":"Item Name","price":13.99,"qty":1}}],"total":13.99}}

Rules:
- Include ALL currently ordered items, not just new ones
- qty = quantity of that specific item
- total = sum of all (price × qty), rounded to 2 decimal places
- Only append this line when the order actually changed
- NEVER mention or show this line to the customer
- If order is cleared or cancelled: [ORDER]:{{"items":[],"total":0}}
"""

conversation_history = []


def build_system_prompt(customer_name="", table_number="", preferences=None, order_type="dine-in", delivery_address=""):
    """Build a dynamic system prompt with personalization and dietary preferences."""
    prompt = BASE_SYSTEM_PROMPT
    extras = []

    if customer_name:
        extras.append(f"The customer's name is {customer_name}. Greet them by name and use it occasionally — but naturally, not every message.")

    # Order type context
    if order_type == "dine-in" and table_number:
        extras.append(f"This is a DINE-IN order. The customer is sitting at Table {table_number}. When confirming, say 'Your order is confirmed!' and that their food will be brought to their table.")
    elif order_type == "pickup":
        extras.append(f"This is a PICKUP order. When confirming, say 'Your order is confirmed!' and let them know their order will be ready for collection at the counter shortly. Give an estimated wait time of 15-20 minutes.")
    elif order_type == "delivery":
        extras.append(f"This is a DELIVERY order to: {delivery_address}. When confirming, say 'Your order is confirmed!' and let them know their food will be delivered to their address in approximately 30-45 minutes.")

    if preferences:
        pref_list = ", ".join(preferences)
        extras.append(
            f"DIETARY REQUIREMENTS — strictly follow these: {pref_list}. "
            f"Only recommend items that meet ALL of these requirements. "
            f"If the customer tries to order something that conflicts with their preferences, "
            f"politely flag it and suggest a suitable alternative."
        )

    if extras:
        prompt += "\n\nPERSONALIZATION & REQUIREMENTS:\n" + "\n".join(f"- {e}" for e in extras)

    return prompt


@app.route("/")
def index():
    return render_template("index.html", restaurant_name=RESTAURANT_NAME)


@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    data = request.get_json()
    user_message     = data.get("message", "").strip()
    preferences      = data.get("preferences", [])
    customer_name    = data.get("customer_name", "")
    table_number     = data.get("table_number", "")
    order_type       = data.get("order_type", "dine-in")
    delivery_address = data.get("delivery_address", "")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    conversation_history.append({"role": "user", "content": user_message})

    system = build_system_prompt(customer_name, table_number, preferences, order_type, delivery_address)

    def generate():
        full_response = ""
        try:
            with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=system,
                messages=conversation_history,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    yield f"data: {json.dumps({'text': text})}\n\n"

            conversation_history.append({"role": "assistant", "content": full_response})
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("=" * 50)
    print(f"  Food AI — {RESTAURANT_NAME} Chatbot")
    print("  Open your browser and go to:")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=False)
