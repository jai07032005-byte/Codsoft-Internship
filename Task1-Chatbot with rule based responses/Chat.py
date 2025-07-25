# app.py

import streamlit as st
import re
import random
import time
import string
from datetime import datetime

# --- Core Chatbot Logic (handles stateless responses) ---
def get_stateless_response(user_input):
    """Generates a stateless response or a trigger for a stateful one."""
    user_input = user_input.lower()

    # Utility: Simple Calculations
    calc_match = re.search(r'(what is|calculate|compute) (\d+)\s*([\+\-\*\/])\s*(\d+)', user_input)
    if calc_match:
        num1, op, num2 = int(calc_match.group(2)), calc_match.group(3), int(calc_match.group(4))
        if op == '+': result = num1 + num2
        elif op == '-': result = num1 - num2
        elif op == '*': result = num1 * num2
        elif op == '/': result = num1 / num2 if num2 != 0 else "Infinity (cannot divide by zero)"
        return f"The result is {result}."

    # Utility: Decision Maker
    choose_match = re.search(r'choose between (.+) and (.+)', user_input)
    if choose_match:
        return f"I choose: {random.choice([choose_match.group(1), choose_match.group(2)])}"
        
    # General Rules Dictionary
    rules = {
        r"hello|hi|hey": "Hello! How can I assist you?",
        r"how are you\?*": "I'm doing great, thanks for asking!",
        r"what is your name\?*": "You can call me Intellibot.",
        r"what can you do\?*": "I can do many things! Check the expander below for a list.",
        r"who (made|created) you\?*": "I was built using Python and Streamlit.",
        r".*(time|date).*": f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
        r".*joke.*": "Why don't scientists trust atoms? Because they make up everything!",
        r"flip a coin": f"It's {random.choice(['Heads', 'Tails'])}.",
        r"generate.*password": "trigger_password",
        r"thank you|thanks": "You're welcome!",
        r"bye|goodbye": "Goodbye! Have a great day.",
        r".*(todo|to-do|task|list).*": "trigger_todo",
        r".*(start|play).*game.*": "trigger_game",
        r".*(show me a|what does a).*(dog|puppy).*": "trigger_image_dog",
        r"help": "trigger_help",
        r".*my name is (\w+).*": "trigger_name_set",
        r"what is my name\?*": "trigger_name_get",
        r".*": "I'm not sure how to handle that. You can check my capabilities below!"
    }

    for pattern, response in rules.items():
        if re.match(pattern, user_input):
            return response
            
    return "I am not sure how to respond."

# --- Streamlit Web App Interface ---
st.set_page_config(page_title="Intellibot", layout="centered")

st.title("😊 Intellibot")

# Expander to show rules on the main page
with st.expander("Wondering what I can do? Click here!"):
    st.markdown("""
    I am a rule-based chatbot with a variety of features. Here are some examples of what you can ask me:

    **🛠️ Utilities**
    - `what is 15 * 20?` - I can do basic math.
    - `generate a password` - I'll create a secure password for you.
    - `flip a coin` - Can't decide? I'll do it for you.
    - `choose between cats and dogs` - I can make a choice for you.

    **📝 Personal Assistant**
    - `add milk to my list` - Add an item to your to-do list.
    - `show my list` - View all items on your list.
    - `remove milk from my list` - Remove a specific item.
    - `my name is [Your Name]` - I'll remember your name for the session.

    **🎮 Games & Fun**
    - `start a game` - Play a "Guess the Number" game with me.
    - `tell me a joke` - I'll share one of my favorite jokes.
    - `show me a dog` - I'll show you a cute picture.
    """)

# Sidebar Controls
with st.sidebar:
    st.header("Controls")
    if st.button("Clear Conversation"):
        st.session_state.clear()
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "🧠 Hello! Ask me something, or check the expander above for ideas."}]
for key in ["conversation_state", "todo_list", "game_state", "user_name"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "todo_list" else []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message: st.image(message["image"])
        else: st.markdown(message["content"])

# Main Interaction Logic
if prompt := st.chat_input("What would you like to say?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(0.5)

        bot_reply, bot_image = "", None
        current_state = st.session_state.conversation_state

        if current_state == "game_active":
            try:
                guess = int(prompt)
                secret = st.session_state.game_state['secret_number']
                st.session_state.game_state['attempts'] -= 1
                attempts_left = st.session_state.game_state['attempts']
                if guess == secret:
                    bot_reply = f"🎉 Congratulations! You guessed the number {secret} correctly!"
                    st.session_state.conversation_state = None
                elif attempts_left == 0:
                    bot_reply = f"😞 Game over! The number was {secret}."
                    st.session_state.conversation_state = None
                elif guess < secret: bot_reply = f"Higher... You have {attempts_left} attempts left."
                else: bot_reply = f"Lower... You have {attempts_left} attempts left."
            except ValueError: bot_reply = "Please enter a valid number."
        else:
            response_trigger = get_stateless_response(prompt)
            
            if response_trigger == "trigger_todo":
                add_m = re.search(r"add (.+?) to my", prompt, re.IGNORECASE)
                rem_m = re.search(r"remove (.+?) from my", prompt, re.IGNORECASE)
                if add_m:
                    item = add_m.group(1); st.session_state.todo_list.append(item); bot_reply = f"✅ Added '{item}'."
                elif rem_m:
                    item = rem_m.group(1)
                    if item in st.session_state.todo_list: st.session_state.todo_list.remove(item); bot_reply = f"🗑️ Removed '{item}'."
                    else: bot_reply = f"Could not find '{item}'."
                elif re.search(r"show|view", prompt, re.IGNORECASE):
                    if st.session_state.todo_list:
                        tasks = "\n".join(f"- {task}" for task in st.session_state.todo_list)
                        bot_reply = f"**Your To-Do List:**\n{tasks}"
                    else: bot_reply = "Your to-do list is empty."
                elif re.search(r"clear|reset", prompt, re.IGNORECASE): st.session_state.todo_list = []; bot_reply = "Cleared your to-do list."
                else: bot_reply = "I can 'add', 'remove', 'show', or 'clear' items from your list."
            elif response_trigger == "trigger_game":
                st.session_state.conversation_state = "game_active"
                st.session_state.game_state = {'secret_number': random.randint(1, 100), 'attempts': 5}
                bot_reply = "I've thought of a number between 1 and 100. You have 5 attempts. Go!"
            elif response_trigger == "trigger_image_dog":
                bot_reply = "Here is a cute dog!"; bot_image = "dog.jpg"
            elif response_trigger == "trigger_password":
                chars = string.ascii_letters + string.digits + string.punctuation
                bot_reply = f"Here is a secure password: `{ ''.join(random.choice(chars) for i in range(12))}`"
            elif response_trigger == "trigger_name_set":
                name_match = re.search(r"my name is (\w+)", prompt, re.IGNORECASE)
                if name_match: st.session_state.user_name = name_match.group(1).capitalize(); bot_reply = f"Nice to meet you, {st.session_state.user_name}!"
            elif response_trigger == "trigger_name_get":
                if st.session_state.user_name: bot_reply = f"Your name is {st.session_state.user_name}."
                else: bot_reply = "I don't know your name yet. Tell me by saying 'my name is...'."
            elif response_trigger == "trigger_help":
                 bot_reply = "You can find my main commands in the expander at the top of the page!"
            else: bot_reply = response_trigger
        
        # Add brain emoji to every final response
        final_response = f"🧠 {bot_reply}"
        
        if bot_image: st.image(bot_image)
        st.markdown(final_response)

    # Add bot response to history, including the emoji
    msg_to_add = {"role": "assistant", "content": final_response}
    if bot_image: msg_to_add["image"] = bot_image
    st.session_state.messages.append(msg_to_add)