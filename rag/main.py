from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


# API endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload")
def upload_data(data: list):
    """
    Upload endpoint that receives a list of data in json format and returns a success message.
    """
    # Here you would typically process the data
    return {"message": "Data received successfully", "data": data}

def generate_prompt(context, message):
    """
    Function to generate a prompt for the chat bot.
    """
    # Here you would typically generate a prompt based on the context and message
    return f"Context: {context}, Message: {message}"

@app.post("/chat")
def chat_bot(message: str):
    """
    Chat bot endpoint that receives a list of messages and returns a response.
    """

    # if(id==restaurant_id):
    #     # Call the function to get restaurant data
    #     response = get_restaurant_data(id)
    #     menu_items_ids = response.get("menu_items", [])
    #     menu_items = []
    #     for menu_item_id in menu_items_ids:
    #         menu_item = get_menu_item_data(menu_item_id)
    #         menu_items.append(menu_item)
    #     response["menu_items"] = menu_items
    #     context= response
    #     prompt = generate_prompt(context, message)
    # else:
    #     # Call the function to get menu item data
    #     response = get_menu_item_data(id)
    #     restaurant_id = response.get("restaurant_id")
    #     restaurant = get_restaurant_data(restaurant_id)
    #     response["restaurant"] = restaurant
    #     context= response
    #     prompt = generate_prompt(context, message)


    


    
    return {"response": message}