import chromadb

from sentence_transformers import (
    SentenceTransformer
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="inventory"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

from models.product import Product


def index_inventory():

    collection.delete(
        ids=[
            str(p.id)
            for p in Product.query.all()
        ]
    )

    products = Product.query.all()

    for product in products:

        document = f"""
            Product Name: {product.name}

            SKU: {product.sku}

            Category: {product.category}

            Current Quantity: {product.quantity}

            Price: {product.price}

            Supplier Name: {product.supplier}

            Minimum Stock Level: {product.minimum_stock}

            Description:
            {product.name} belongs to category {product.category}.
            The supplier is {product.supplier}.
            Current stock is {product.quantity}.
            The minimum stock requirement is {product.minimum_stock}.
            """

        embedding = model.encode(
            document
        ).tolist()

        collection.add(
            ids=[str(product.id)],
            documents=[document],
            embeddings=[embedding]
        )
def search_inventory(question):

    embedding = model.encode(
        question
    ).tolist()

    results = collection.query(
    query_embeddings=[embedding],
    n_results=3
    )
    documents = results["documents"][0]

    return documents