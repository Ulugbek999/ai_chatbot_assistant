from flask import Flask, request, jsonify, render_template
import openai
import re
from models import create_tables, insert_mock_data
from database import connect_db
from models import create_tables_tech, insert_mock_data_tech, insert_tech_user
import os
from dotenv import load_dotenv
from flask import Flask, session

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
app.secret_key = 'the_secret_key_for_now.'  # <-- REQUIRED for sessions


#to set up tables and mock data in the database
#inserting mock data
with app.app_context():
    create_tables()
    insert_mock_data()
    create_tables_tech()
    insert_mock_data_tech()

    

load_dotenv()  # take environment variables from .env.

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("API key not found.")
else:
    openai.api_key = api_key
    print("OpenAI API key is set successfully.")

openai.api_key = api_key

#session_memory = {}  # Session memory for storing names and relationships -> no longer used as it saves all the user info from different users
context_window = []  # Context window to hold last 5-10 exchanges
user_info = [] # To store user info such as their names, emails, phone numbers

#home route
@app.route('/')
def home():
    return render_template('index.html')

#------------------------Database routes---------------------------------#
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully."}), 201

@app.route('/check_inventory', methods=['POST'])
def check_inventory():
    data = request.json
    product = data.get('product')
    size = data.get('size')

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM inventory WHERE product = ? AND size = ?", (product, size))
    result = cur.fetchone()
    conn.close()

    if result:
        return jsonify({"product": product, "size": size, "quantity": result['quantity']})
    else:
        return jsonify({"message": "Item not found"}), 404

#track shipment
@app.route('/track_shipment', methods=['POST'])
def track_shipment():
    data = request.json
    tracking_number = data.get('tracking_number')

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT status, estimated_delivery_date FROM shipping WHERE tracking_number = ?", (tracking_number,))
    result = cur.fetchone()
    conn.close()

    if result:
        return jsonify({
            "tracking_number": tracking_number,
            "status": result['status'],
            "estimated_delivery_date": result['estimated_delivery_date']
        })
    else:
        return jsonify({"message": "Tracking number not found"}), 404
#---------------------------------------------------------------------------

def parse_commands(input_text):
    #detecting if a user wants to track an order
    track_keywords = ["track", "tracking number"]
    check_inv_keywords = ["do you have", "check inventory", "available"]

    lower_input = input_text.lower()
    if any(keyword in lower_input for keyword in track_keywords):
        return "track"
    elif any(keyword in lower_input for keyword in check_inv_keywords):
        return "check_inventory"
    else:
        return "general"

#function to determine what type of chatbot is being currently used and supplying the appropriate data to the chatbot
def contentSupply(chatBotType):
    # Get the directory where this file (app.py) is located
    base_dir = os.path.dirname(os.path.realpath(__file__))

    if chatBotType == "clothing":
        file_path = os.path.join(base_dir, 'clothingStoreAssistantData.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contentType = file.read()
        except FileNotFoundError:
            print("clothingStoreAssistantData.txt not found in:", file_path)
            contentType = "Clothing Assistant data not found."
    elif chatBotType == "tech":
        file_path = os.path.join(base_dir, 'techAssistantData.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contentType = file.read()
        except FileNotFoundError:
            print("techAssistantData.txt not found in:", file_path)
            contentType = "Tech Assistant data not found."
    elif chatBotType == "travel":
        file_path = os.path.join(base_dir, 'travelAgencyAssistantData.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contentType = file.read()
        except FileNotFoundError:
            print("travelAgencyAssistantData.txt not found in:", file_path)
            contentType = "Travel Assistant data not found."
    else:
        contentType = "Tell the user that something went wrong and you didn't get your data."

    return contentType

#function to extract name's and other user information
def extract_user_info(input_text):
    # Patterns for extracting the name
    patterns1 = [
        r"call my (\w+) ([A-Za-z]+(?: [A-Za-z]+)*)",     # e.g. "call my friend John Doe"
        r"my name is ([A-Za-z]+(?: [A-Za-z]+)*)",       # e.g. "my name is John Doe"
        r"my name's ([A-Za-z]+(?: [A-Za-z]+)*)",        # e.g. "my name's John Doe"
        r"(?:i am|i'm) ([A-Za-z]+(?: [A-Za-z]+)*)"      # e.g. "I'm John Doe" or "I am John Doe"
    ]

    # Patterns to extract the email (only robust pattern to avoid capturing partial text)
    patterns2 = [
        r"[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    ]

    # Patterns for phone numbers
    patterns3 = [
        r"my phone number is ([\d\s\-\(\)]+)",
        r"([\d\s\-\(\)]+) is my phone number",
        r"([\d\s\-\(\)]+) is my number",
        r"\+?\d[\d\s\-\(\)]+"
    ]

    # First, check for name patterns using case-insensitive search
    for pattern in patterns1:
        match = re.search(pattern, input_text, flags=re.IGNORECASE)
        if match:
            # If pattern has multiple groups (e.g. "call my friend John Doe"), take the last group as the name.
            # Otherwise, take the first group.
            if len(match.groups()) >= 1:
                name = match.group(len(match.groups()))
            else:
                name = match.group(1)
            return ("user", name.strip().title())

    # Check for email pattern
    for pattern in patterns2:
        match = re.search(pattern, input_text, flags=re.IGNORECASE)
        if match:
            email = match.group(0)
            return ("email", email.strip())

    # Check for phone number patterns
    for pattern in patterns3:
        match = re.search(pattern, input_text, flags=re.IGNORECASE)
        if match:
            # Use group(1) if available, otherwise fallback to full match
            phoneNumber = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
            return ("phone", phoneNumber.strip())

    return None  # Return None if no patterns match


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_input = data.get('user_input', '')
    chatbot_type = data.get('chatbot_type', 'general')

    # 1) Retrieve the chatbot's system instructions from your data files
    contentType = contentSupply(chatbot_type)

    # 2) Ensure each user has their own context window in session
    if 'context_window' not in session:
        session['context_window'] = []
    
    # 3) Store the user's message in their context window
    session['context_window'].append({"role": "user", "content": user_input})
    # Limit to last 5 messages
    session['context_window'] = session['context_window'][-5:]
    session.modified = True

    import re

    # 4) If the user’s message contains a 6+ digit tracking number, store it in session
    tracking_pattern = re.search(r'\b(\d{6,})\b', user_input)
    if tracking_pattern:
        session["tracking"] = tracking_pattern.group(1)
        print(f"DEBUG: Found tracking number = {session['tracking']}")

    # 5) Detect user intent (track shipment vs. check inventory vs. general)
    def parse_command(text):
        track_keywords = ["track", "tracking number", "check shipment"]
        check_inv_keywords = ["do you have", "check inventory", "available", "size"]

        lower_text = text.lower()
        if any(k in lower_text for k in track_keywords):
            return "track"
        elif any(k in lower_text for k in check_inv_keywords):
            return "check_inventory"
        else:
            return "general"

    user_intent = parse_command(user_input)

    # 6) Extract name/email/phone; store them in session
    parsed_info = extract_user_info(user_input)
    if parsed_info is not None:
        key, value = parsed_info
        session[key] = value
        session.modified = True

    # 7) Potential additional system context
    system_additional_context = ""

    # 8) If tech bot, store user info in DB
    if chatbot_type == 'tech':
        user_name = session.get('user')   # from session
        user_email = session.get('email')
        user_phone = session.get('phone')

        if user_name or user_email or user_phone:
            if not user_name:
                user_name = "Unknown"
            if not user_email:
                user_email = "Unknown"
            if not user_phone:
                user_phone = "Unknown"

            # Only insert if at least one is not "Unknown"
            if (user_name, user_email, user_phone) != ("Unknown", "Unknown", "Unknown"):
                user_id = insert_tech_user(user_name, user_phone, user_email)
                print(f"DEBUG: Inserted user with ID {user_id}, "
                      f"Name: {user_name}, Phone: {user_phone}, Email: {user_email}")
                system_additional_context += (
                    f"I have saved your details to our tech support system. "
                    f"Your user ID is {user_id}. "
                )

    # 9) If user wants to track an order
    if user_intent == "track":
        tracking_num = session.get("tracking", None)
        if tracking_num:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT status, estimated_delivery_date
                FROM shipping
                WHERE tracking_number = ?
            """, (tracking_num,))
            result = cur.fetchone()
            conn.close()

            if result:
                shipping_status = result["status"]
                delivery_date = result["estimated_delivery_date"]
                system_additional_context = (
                    f"I’ve found your shipment with tracking number {tracking_num}. "
                    f"It’s currently {shipping_status} and is expected to be delivered by {delivery_date}. "
                    f"Is there anything else I can help you with?"
                )
            else:
                system_additional_context = (
                    f"I couldn’t find any shipment with tracking number {tracking_num}. "
                    "Please double-check the number or contact support for assistance."
                )
        else:
            system_additional_context = (
                "It looks like you’d like to track a shipment, but I don’t see a valid tracking number in our system. "
                "Could you provide it again?"
            )

    elif user_intent == "check_inventory":
        product_match = re.search(r"(jeans|shirt|pants|dress)", user_input.lower())
        size_match = re.search(r"(32|34|s|m|l|xl|xxl|\d+)", user_input.lower())
        if product_match and size_match:
            product = product_match.group(1)
            size = size_match.group(1)

            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT quantity
                FROM inventory
                WHERE product = ? AND size = ?
            """, (product, size))
            result = cur.fetchone()
            conn.close()

            if result and result["quantity"] > 0:
                system_additional_context = (
                    f"We have {result['quantity']} {product} in size {size} available."
                )
            else:
                system_additional_context = (
                    f"Sorry, we don’t have {product} in size {size} in stock."
                )

    # 10) Summarize known user info from the session
    def memory_summary(mem):
        summary_parts = []
        if "user" in mem:
            summary_parts.append(f"The user's name is {mem['user']}.")
        if "email" in mem:
            summary_parts.append(f"The user's email is {mem['email']}.")
        if "phone" in mem:
            summary_parts.append(f"The user's phone number is {mem['phone']}.")
        if "tracking" in mem:
            summary_parts.append(f"The user's tracking number is {mem['tracking']}.")

        if summary_parts:
            return "Here is some known user info:\n" + "\n".join(summary_parts)
        else:
            return ""

    summary_text = memory_summary(session)

    # 11) Build the system messages
    messages = []
    messages.append({"role": "system", "content": contentType})
    if summary_text:
        messages.append({"role": "system", "content": summary_text})
    if system_additional_context:
        messages.append({"role": "system", "content": system_additional_context})

    # 12) Add user’s conversation from the session-based context window
    # (We already appended the user’s message above)
    # to the final messages we send to OpenAI
    messages += session['context_window']

    try:
        # 13) Call OpenAI with the final list of messages
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']

        # 14) Store the assistant's response in the session context
        session['context_window'].append({"role": "assistant", "content": reply})
        # Keep last 5
        session['context_window'] = session['context_window'][-5:]
        session.modified = True

        return jsonify({"response": reply})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

    

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return "Session cleared", 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get PORT from environment, default to 5000
    app.run(host='0.0.0.0', port=port)

