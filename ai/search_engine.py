import re

# CATEGORY KEYWORDS
CATEGORY_MAP = {

    "laptop": "Laptops",
    "laptops": "Laptops",
    "notebook": "Laptops",
    "ultrabook": "Laptops",

    "phone": "Smartphones",
    "phones": "Smartphones",
    "mobile": "Smartphones",
    "smartphone": "Smartphones",

    "headphone": "Headphones",
    "headphones": "Headphones",
    "earbuds": "Headphones",
    "earbud": "Headphones",
    "bluetooth": "Headphones",

    "shoe": "Shoes",
    "shoes": "Shoes",
    "sneakers": "Shoes",
    "boots": "Shoes",
    "sandals": "Shoes",

    "book": "Books",
    "books": "Books",
    "novel": "Books",
    "story": "Books",
    "fiction": "Books",
    "history": "Books",
    "philosophy": "Books",
    "algebra": "Books",

    "cycle": "Cycles",
    "bike": "Cycles",
    "cycling": "Cycles",
    "bicycle": "Cycles",
    "camping": "Cycles",
    "fitness": "Cycles",

    "beauty": "Beauty",
    "perfume": "Beauty",
    "serum": "Beauty",
    "makeup": "Beauty",
    "lotion": "Beauty",
    "gaming": "Laptops",
    "programming": "Laptops",
    "developer": "Laptops",

    "wireless": "Headphones",
    "bluetooth": "Headphones",

    "history": "Books",
    "deep": "Books",
    "learning": "Books",

    "trekking": "Cycles",
    "hiking": "Cycles",
    "scrub": "Beauty"
}

# PURPOSE KEYWORDS

PURPOSE_MAP = {

    "ai": [
        "ai",
        "machine learning",
        "deep learning",
        "developer",
        "programming"
    ],

    "gaming": [
        "gaming",
        "graphics",
        "performance"
    ],

    "office": [
        "office",
        "business",
        "student"
    ],

    "story": [
        "story",
        "fiction",
        "novel"
    ],

    "history": [
        "history"
    ],

    "wireless": [
        "wireless",
        "bluetooth"
    ],

    "trekking": [
        "trekking",
        "camping",
        "outdoor"
    ]
}
STOP_WORDS = {

    "best",
    "top",
    "good",
    "show",
    "find",
    "recommend",
    "recommended",

    "under",
    "below",
    "less",

    "than",

    "for",

    "with",

    "a",
    "an",
    "the",

    "of",
    "to",
    "in",

    "me"
}
def parse_query(query):

    query = query.lower()

    category = None

    budget = None

    purpose = []

    words = re.findall(r"[a-zA-Z]+", query)
    # Category

    for word in words:

        if word in CATEGORY_MAP:

            category = CATEGORY_MAP[word]

            break

    # Budget

    match = re.search(r"\d+", query)

    if match:

        budget = int(match.group())

    # Purpose

    for word in words:

        if word in PURPOSE_MAP:

            purpose.extend(PURPOSE_MAP[word])

    return {

        "category": category,

        "budget": budget,

        "purpose": purpose

    }
def extract_keywords(query):

    words = re.findall(r"[a-zA-Z]+", query.lower())

    keywords = []

    for word in words:

        if word in STOP_WORDS:
            continue

        keywords.append(word)

    return keywords
def search_products(products, query):

    parsed = parse_query(query)
    keywords = extract_keywords(query)

    category = parsed["category"]
    budget = parsed["budget"]
    purpose = parsed["purpose"]

    results = []

    for product in products:

        # Category
        if category:
            if product["category"] != category:
                continue

        # Budget
        if budget is not None:
            if product["price"] > budget:
                continue

        score = 0

        # Base score
        score += product["rating_avg"] * 10
        score += min(product["review_count"] / 100, 20)
        score += product["discount_percent"]

        if product["badge"] == "Best Seller":
            score += 15

        text = " ".join([
            product["product_name"] or "",
            product["brand"] or "",
            product.get("description") or "",
            product.get("tags") or ""
        ]).lower()

        # Purpose matching
        for word in purpose:
            if word.lower() in text:
                score += 25

        # Keyword matching
        for word in keywords:
            if word.lower() in text:
                score += 10

        product["search_score"] = score
        results.append(product)

    results.sort(
        key=lambda x: x["search_score"],
        reverse=True
    )

    return results