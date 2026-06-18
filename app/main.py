import logging

from fastapi import FastAPI, HTTPException

from app.database import get_connection
from app.schemas import Product, QuantityUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_cursor():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        return connection, cursor
    except Exception as exc:
        logger.error("Database connection failed: %s", exc)
        raise HTTPException(status_code=500, detail="Database connection error")


app = FastAPI(title="Retail Mart Inventory API")


@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"message": "Retail Mart Inventory API is running"}


@app.post("/products")
def add_product(product: Product):
    logger.info(f"Adding product: {product.name} category={product.category} price={product.price} quantity={product.quantity}")
    connection, cursor = get_db_cursor() # cursor is the object that actually sends SQL commands to the database and fetches results.

    query = """
        INSERT INTO products (name, category, price, quantity)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (product.name, product.category, product.price, product.quantity))
    connection.commit()

    new_product_id = cursor.lastrowid

    cursor.close()
    connection.close()

    logger.info("Product added successfully id=%s", new_product_id)
    return {
        "message": "Product added successfully",
        "product_id": new_product_id
    }


@app.get("/products")
def get_all_products():
    logger.info("Fetching all products")
    connection, cursor = get_db_cursor() # cursor is the object that actually sends SQL commands to the database and fetches results.

    query = "SELECT * FROM products"
    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    logger.info("Fetched %s products", len(products))
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    logger.info("Fetching product id=%s", product_id)
    connection, cursor = get_db_cursor()

    query = "SELECT * FROM products WHERE id = %s"
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    cursor.close()
    connection.close()

    if product is None:
        logger.warning("Product not found id=%s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    logger.info("Product found id=%s", product_id)
    return product


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    logger.info("Updating product id=%s to name=%s category=%s price=%s quantity=%s", product_id, product.name, product.category, product.price, product.quantity)
    connection, cursor = get_db_cursor()

    check_query = "SELECT * FROM products WHERE id = %s"
    cursor.execute(check_query, (product_id,))
    existing_product = cursor.fetchone()

    if existing_product is None:
        cursor.close()
        connection.close()
        logger.warning("Product not found for update id=%s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    update_query = """
        UPDATE products
        SET name = %s, category = %s, price = %s, quantity = %s
        WHERE id = %s
    """

    cursor.execute(
        update_query,
        (product.name, product.category, product.price, product.quantity, product_id)
    )
    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Product updated successfully id=%s", product_id)
    return {"message": "Product updated successfully"}


@app.patch("/products/{product_id}/quantity")
def update_product_quantity(product_id: int, data: QuantityUpdate):
    logger.info("Updating quantity for product id=%s to %s", product_id, data.quantity)
    connection, cursor = get_db_cursor()

    check_query = "SELECT * FROM products WHERE id = %s"
    cursor.execute(check_query, (product_id,))
    existing_product = cursor.fetchone()

    if existing_product is None:
        cursor.close()
        connection.close()
        logger.warning("Product not found for quantity update id=%s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    update_query = "UPDATE products SET quantity = %s WHERE id = %s"
    cursor.execute(update_query, (data.quantity, product_id))
    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Quantity updated successfully id=%s new_quantity=%s", product_id, data.quantity)
    return {
        "message": "Quantity updated successfully",
        "product_id": product_id,
        "new_quantity": data.quantity
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    logger.info("Deleting product id=%s", product_id)
    connection, cursor = get_db_cursor()

    check_query = "SELECT * FROM products WHERE id = %s"
    cursor.execute(check_query, (product_id,))
    existing_product = cursor.fetchone()

    if existing_product is None:
        cursor.close()
        connection.close()
        logger.warning("Product not found for delete id=%s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    delete_query = "DELETE FROM products WHERE id = %s"
    cursor.execute(delete_query, (product_id,))
    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Product deleted successfully id=%s", product_id)
    return {"message": "Product deleted successfully"}



# New API added by Raghu