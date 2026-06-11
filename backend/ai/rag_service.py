from models.product import Product


class RAGService:

    @staticmethod
    def build_inventory_context():

        products = Product.query.all()

        context = []

        for product in products:

            context.append(
                f"""
                Product: {product.name}
                SKU: {product.sku}
                Category: {product.category}
                Quantity: {product.quantity}
                Price: {product.price}
                Supplier: {product.supplier}
                """
            )

        return "\n".join(context)