import pandas as pd

from database.db import get_connection


def import_products():

    df = pd.read_csv("data/clean_products.csv")

    db = get_connection()

    query = """
    INSERT INTO products(

        product_id,
        product_name,
        product_description,
        category,
        subcategory,
        brand,
        price,
        rating_avg,
        review_count,
        stock_quantity,
        date_added

    )

    VALUES(

        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s

    )
    """

    values = []

    for _, row in df.iterrows():

        values.append(

            (

                row["product_id"],
                row["product_name"],
                row["product_description"],
                row["category"],
                row["subcategory"],
                row["brand"],
                row["price"],
                row["rating_avg"],
                row["review_count"],
                row["stock_quantity"],
                row["date_added"]

            )

        )

    db.executemany(query, values)

    db.close()

    print(f"\nImported {len(values)} Products Successfully")


if __name__ == "__main__":

    import_products()