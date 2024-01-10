from dotenv import load_dotenv
import os

# Load variables from the .env file into the environment
load_dotenv()

# Access environment variables
Server = os.getenv('SERVER')
Port = os.getenv('PORT')
Debug = os.getenv('DEBUG')


