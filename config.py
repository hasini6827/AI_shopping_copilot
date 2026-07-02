import os
from dotenv import load_dotenv

load_dotenv()

# FLASK

SECRET_KEY = os.getenv("SECRET_KEY", "shopbuddy_secret_key")

# DATABASE
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ai_shopping_copilot")
}

# PROJECT PATHS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FAISS_INDEX = os.path.join(BASE_DIR, "faiss_index", "products.index")
PRODUCT_METADATA = os.path.join(BASE_DIR, "faiss_index", "product_metadata.pkl")

# HUGGING FACE

HF_TOKEN = os.getenv("HF_TOKEN")

HF_MODEL = "Qwen/Qwen2.5-7B-Instruct"

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

# SEARCH

TOP_K_RESULTS = 5

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"