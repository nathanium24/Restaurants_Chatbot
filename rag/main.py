import os
import streamlit as st
import json
from bson import ObjectId
import asyncio
from dotenv import load_dotenv
from models.resturant import Restaurant
from models.menu_item import MenuItem
from db.pine_utils import upsert_data, fetch_data
from motor.motor_asyncio import AsyncIOMotorClient

from utils.generatePrompt import generatePrompt
from utils.llm import generate_content

# Load environment variables
load_dotenv()

uri = os.getenv("MONGODB_URI")

# MongoDB setup
client = AsyncIOMotorClient(uri)
db = client["zomato_rag"]
collection = db["zomato_collection"]

# Asyncio event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Upload function
async def upload_data():
    with open("../scraper/data/knowledgebase.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for restaurant_data in data:
        menu_items_data = restaurant_data.pop("menu_items", [])
        
        if not isinstance(restaurant_data.get('cuisine'), str):
            restaurant_data['cuisine'] = ', '.join(restaurant_data['cuisine'])

        restaurant_obj = Restaurant(**restaurant_data, menu_items=[])
        restaurant_inserted = await collection.insert_one(restaurant_obj.dict())
        restaurant_id = restaurant_inserted.inserted_id

        restaurant_string = " ".join(f"{key}: {value}" for key, value in restaurant_data.items())
        await upsert_data(restaurant_string, str(restaurant_id), "resturant")

        for menu_item in menu_items_data:
            menu_item_obj = MenuItem(**menu_item, restaurant_id=str(restaurant_id))
            menu_item_inserted = await collection.insert_one(menu_item_obj.dict())
            menu_item_id = menu_item_inserted.inserted_id

            menu_item_string = " ".join(f"{key}: {value}" for key, value in menu_item.items())
            await upsert_data(menu_item_string, str(menu_item_id), "menu")

            collection.update_one(
                {"_id": restaurant_id},
                {"$push": {"menu_items": str(menu_item_id)}}
            )

# Helper to fetch and enrich documents
async def get_doc(entry):
    raw = entry.get('_id', '')
    parts = raw.split()
    raw_id, vector_type = parts[0], parts[-1].lower()

    try:
        oid = ObjectId(raw_id)
    except Exception as e:
        print(f"Error converting ID to ObjectId: {e}")
        return None

    doc = await collection.find_one({'_id': oid})
    if not doc:
        return None

    doc['_id'] = str(oid)
    doc['_score'] = entry.get('_score')
    doc['vector_type'] = vector_type

    if vector_type == 'resturant':
        menus = []
        for mid in doc.get('menu_items', []):
            try:
                m_oid = ObjectId(mid)
            except Exception as e:
                print(f"Error converting menu item ID: {e}")
                continue
            mdoc = await collection.find_one({'_id': m_oid})
            if mdoc:
                mdoc['_id'] = str(m_oid)
                menus.append(mdoc)
        doc['menus'] = menus
    elif vector_type == 'menu':
        parent = await collection.find_one({'menu_items': raw_id})
        if parent:
            parent['_id'] = str(parent['_id'])
            parent.pop('menu_items', None)
            doc['restaurant'] = parent

    return doc

# Chat function
async def chat_bot(message):
    try:
        data = await fetch_data(message)
    except Exception as e:
        return f"Error fetching from vector store: {e}"

    if not data:
        return "No matches found."

    docs = []
    first_type = data[0].get('_id', '').split()[-1].lower()
    if first_type == 'resturant':
        doc = await get_doc(data[0])
        if doc:
            docs.append(doc)
    elif first_type == 'menu':
        for entry in data:
            doc = await get_doc(entry)
            if doc:
                docs.append(doc)
    else:
        for entry in data[:2]:
            doc = await get_doc(entry)
            if doc:
                docs.append(doc)

    if not docs:
        return "No valid documents found."
    
    prompt = generatePrompt(message, docs)

    try:
        response = generate_content(prompt)
    except Exception as e:
        return f"Error generating content: {e}"

    if not response:
        return "No response generated."

    return response

# ---------- STREAMLIT APP UI (Improved) ----------

st.set_page_config(page_title="🍽️ HungryBot - Your Restaurant Guide", page_icon="🤖", layout="wide")

# Custom CSS for header and chat bubbles
st.markdown("""
    <style>
    .header-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #FF6F00;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #D0F0FD;
        color: #000000;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        font-size: 18px;
    }
    .bot-message {
        background-color: #FFF5BA;
        color: #000000;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Big Chatbot Name
st.markdown("<div class='header-title'>🤖 HungryBot</div>", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.title("🔧 Admin Panel")

if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.messages = []

st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Suggestions:**")
for suggestion in [
    "Which restaurant has the best vegetarian options in their menu?",
    "Which restaurant have any gluten-free appetizers?",
    "What's the price range for Purple Basil restaurant's dessert menu?",
    "Compare the spice levels mentioned in the menus of restaurants Curry Leaf restaurant and Tanatan restaurant."
]:
    st.sidebar.markdown(f"- {suggestion}")

st.sidebar.markdown("---")
if st.sidebar.button("🚀 Upload Feast Data"):
    with st.spinner("Cooking up fresh data... 🍲"):
        loop.run_until_complete(upload_data())
    st.sidebar.success("Knowledgebase updated! 🎉")

# Initialize chat history or show intro
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("<div class='bot-message'>Hello, hungry friend! 🍽️ Ready to explore some tasty tidbits?</div>", unsafe_allow_html=True)

# Display chat history (user and bot messages together)
for i in range(0, len(st.session_state.messages), 2):
    if i < len(st.session_state.messages):
        user_msg = st.session_state.messages[i]
        if user_msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"<div class='user-message'>{user_msg['content']}</div>", unsafe_allow_html=True)
    if i + 1 < len(st.session_state.messages):
        bot_msg = st.session_state.messages[i + 1]
        if bot_msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(f"<div class='bot-message'>{bot_msg['content']}</div>", unsafe_allow_html=True)

# User input
if user_input := st.chat_input("Ask me anything... I'm all ears (and taste buds)! 🤤"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("Putting on my chef hat... 👩‍🍳"):
            bot_response = loop.run_until_complete(chat_bot(user_input))
        st.markdown(f"<div class='bot-message'>{bot_response}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
