import pandas as pd

# Load dataset
df = pd.read_csv("data/products.csv")

# Categories we want
wanted_categories = {
    "Electronics",
    "Clothing & Accessories",
    "Beauty & Personal Care",
    "Sports & Outdoors",
    "Books"
}

# Keep only required categories
df = df[df["category"].isin(wanted_categories)].copy()

# Convert to our custom categories

def get_category(row):

    category = row["category"]
    sub = str(row["subcategory"]).lower()
    name = str(row["product_name"]).lower()

    # ---------------- Smartphones ----------------

    if category == "Electronics":

        if any(x in name for x in [
            "iphone","phone","smartphone",
            "galaxy","pixel","oneplus",
            "mobile"
        ]):
            return "Smartphones"

        elif any(x in name for x in [
            "laptop",
            "notebook",
            "macbook",
            "thinkpad",
            "ideapad",
            "vivobook",
            "inspiron",
            "pavilion",
            "aspire",
            "gram",
            "surface"
        ]):
            return "Laptops"

        elif any(x in name for x in [
            "headphone","earbud",
            "earphone","headset"
        ]):
            return "Headphones"

        else:
            return None

    # ---------------- Shoes ----------------

    elif category == "Clothing & Accessories":

        if any(x in name for x in [
            "shoe","shoes","sneaker",
            "boot","sandal"
        ]):
            return "Shoes"

        return None

    # ---------------- Beauty ----------------

    elif category == "Beauty & Personal Care":

        return "Beauty"

    # ---------------- Sports ----------------

    elif category == "Sports & Outdoors":

        return "Sports"

    # ---------------- Books ----------------

    elif category == "Books":

        return "Books"

    return None


df["new_category"] = df.apply(get_category, axis=1)

# Remove unwanted rows
df = df[df["new_category"].notna()]

# Remove duplicates
df = df.drop_duplicates(subset=["product_name"])

# Keep only first 8 products from each category
df = (
    df.groupby("new_category")
      .head(8)
      .reset_index(drop=True)
)

# Rename category column
df["category"] = df["new_category"]
df = df.drop(columns=["new_category"])

# Save cleaned dataset
df.to_csv("data/clean_products.csv", index=False)

print("=" * 50)
print("Dataset cleaned successfully!")
print("=" * 50)

print(df["category"].value_counts())

print("\nTotal Products:", len(df))