import requests
from config import HF_API_URL, HF_MODEL, HF_TOKEN


def generate_ai_explanation(query, products):

    if not products:
        return "No suitable products were found."

    product_list = "\n".join(
        [
            f"- {p['product_name']} | ₹{p['price']} | Rating {p['rating_avg']}"
            for p in products
        ]
    )

    prompt = f"""
You are ShopBuddy AI.

The user searched for:

{query}

Available products:

{product_list}

Recommend these products in 4-6 lines.

Explain:

• Why these products fit the user's needs.
• Mention ratings.
• Mention price.
• Mention overall value.

Keep the answer friendly and concise.
"""

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": HF_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 200,
        "temperature": 0.6
    }

    try:

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=40
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        print(e)

        return "ShopBuddy AI is currently unavailable."