from flask import Blueprint
from flask import request
from flask import jsonify

from services.gemini_service import ask_gemini

from services.chroma_service import (
    search_inventory
)

from models.product import Product
from models.transaction import Transaction

import re


ai_inventory_bp = Blueprint(
    "ai_inventory",
    __name__
)


@ai_inventory_bp.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({
        "status": "ok"
    })


@ai_inventory_bp.route(
    "",
    methods=["POST"]
)



def ask_inventory():

    try:

        question = request.json.get(
            "question",
            ""
        ).lower().strip()

        print("=" * 50)
        print("QUESTION:", question)
        print("=" * 50)

        products = Product.query.all()

        if not products:

            return jsonify({
                "answer":
                "No products found in inventory."
            })

        
        # =====================
        # INVENTORY VALUE NEXT MONTH
        # =====================

        if any(
            phrase in question
            for phrase in [
                "predict inventory value next month",
                "inventory value next month"
            ]
        ):

            current_value = sum(
                p.price * p.quantity
                for p in products
            )

            predicted = current_value * 1.05

            return jsonify({
                "answer":
                f"Predicted inventory value next month: ₹{predicted:,.2f}"
            })
        
        # =====================
        # INVENTORY DASHBOARD
        # =====================

        if any(
            phrase in question
            for phrase in [
                "inventory dashboard",
                "inventory summary",
                "dashboard"
            ]
        ):

            total_products = len(products)

            total_stock = sum(
                p.quantity
                for p in products
            )

            inventory_value = sum(
                p.quantity * p.price
                for p in products
            )

            low_stock = len([
                p for p in products
                if p.quantity <
                p.minimum_stock
            ])

            return jsonify({
                "answer":
                f"""
            Inventory Summary

            Total Products: {total_products}
            Total Stock Units: {total_stock}
            Inventory Value: ₹{inventory_value:,.2f}
            Low Stock Products: {low_stock}
            """
                        })
        
        # =====================
        # INVENTORY VALUE BY CATEGORY
        # =====================

        if any(
            phrase in question
            for phrase in [
                "inventory value by category",
                "category inventory value"
            ]
        ):

            result = {}

            for product in products:

                category = product.category

                result[category] = result.get(
                    category,
                    0
                ) + (
                    product.price *
                    product.quantity
                )

            return jsonify({
                "answer":
                "\n".join(
                    [
                        f"{category}: ₹{value:,.2f}"
                        for category, value
                        in result.items()
                    ]
                )
            })
        
        
        # =====================
        # INVENTORY VALUE
        # =====================

        if any(
            phrase in question
            for phrase in [
                "inventory value",
                "total inventory value"
            ]
        ):

            value = sum(
                p.price * p.quantity
                for p in products
            )

            return jsonify({
                "answer":
                f"Inventory value is ₹{value:,.2f}"
            })

        # =====================
        # TOTAL PRODUCTS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "total products",
                "how many products"
            ]
        ):

            return jsonify({
                "answer":
                f"Total products: {len(products)}"
            })

        # =====================
        # TOTAL STOCK QUANTITY
        # =====================

        if any(
            phrase in question
            for phrase in [
                "total stock",
                "stock quantity",
                "total quantity",
                "total stock quantity",
                "all stock",
                "sum of stock"
            ]
        ):

            total_stock = sum(
                p.quantity
                for p in products
            )

            return jsonify({
                "answer":
                f"Total stock quantity: {total_stock} units"
            })

        # =====================
        # TOTAL TRANSACTIONS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "transactions",
                "total transactions"
            ]
        ):

            count = Transaction.query.count()

            return jsonify({
                "answer":
                f"Total transactions: {count}"
            })

        # =====================
        # TOTAL SUPPLIERS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "total suppliers",
                "how many suppliers"
            ]
        ):

            suppliers = set(
                p.supplier
                for p in products
            )

            return jsonify({
                "answer":
                f"Total suppliers: {len(suppliers)}"
            })

        # =====================
        # MOST EXPENSIVE PRODUCT
        # =====================

        if any(
            phrase in question
            for phrase in [
                "most expensive",
                "highest price"
            ]
        ):

            product = max(
                products,
                key=lambda p: p.price
            )

            return jsonify({
                "answer":
                f"{product.name} is the most expensive product at ₹{product.price:,.2f}"
            })

        # =====================
        # MOST VALUABLE PRODUCT
        # =====================

        if any(
            phrase in question
            for phrase in [
                "most valuable product",
                "highest inventory value"
            ]
        ):

            product = max(
                products,
                key=lambda p: (
                    p.price * p.quantity
                )
            )

            value = (
                product.price *
                product.quantity
            )

            return jsonify({
                "answer":
                f"{product.name} has inventory value of ₹{value:,.2f}"
            })

        # =====================
        # HIGHEST STOCK PRODUCT
        # =====================

        if any(
            phrase in question
            for phrase in [
                "highest stock",
                "most stock",
                "top stock product"
            ]
        ):

            product = max(
                products,
                key=lambda p: p.quantity
            )

            return jsonify({
                "answer":
                f"{product.name} has the highest stock ({product.quantity} units)"
            })

        # =====================
        # LOWEST STOCK PRODUCT
        # =====================

        if any(
            phrase in question
            for phrase in [
                "lowest stock",
                "least stock"
            ]
        ):

            product = min(
                products,
                key=lambda p: p.quantity
            )

            return jsonify({
                "answer":
                f"{product.name} has the lowest stock ({product.quantity} units)"
            })

        # =====================
        # AVERAGE STOCK
        # =====================

        if any(
            phrase in question
            for phrase in [
                "average stock",
                "average quantity"
            ]
        ):

            average_stock = (
                sum(
                    p.quantity
                    for p in products
                )
                / len(products)
            )

            return jsonify({
                "answer":
                f"Average stock per product: {average_stock:.2f}"
            })

        # =====================
        # LOW STOCK PRODUCTS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "low stock",
                "below minimum stock",
                "running low",
                "reorder",
                "reorder soon",
                "reorder recommendations",
                "below minimum stock"
            ]
        ):

            low_stock = Product.query.filter(
                Product.quantity <
                Product.minimum_stock
            ).all()

            if not low_stock:

                return jsonify({
                    "answer":
                    "No products are below minimum stock."
                })

            return jsonify({
                "answer":
                "Low stock products: " +
                ", ".join(
                    p.name
                    for p in low_stock
                )
            })

        # =====================
        # LOW STOCK PERCENTAGE
        # =====================

        if any(
            phrase in question
            for phrase in [
                "percentage of inventory is low stock",
                "low stock percentage",
                "inventory low stock percentage"
            ]
        ):

            low_stock_count = len([
                p for p in products
                if p.quantity < p.minimum_stock
            ])

            percentage = (
                low_stock_count /
                len(products)
            ) * 100

            return jsonify({
                "answer":
                f"{percentage:.2f}% of products are low stock."
            })

        # =====================
        # OUT OF STOCK PRODUCTS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "out of stock",
                "zero stock"
            ]
        ):

            matches = [
                p.name
                for p in products
                if p.quantity == 0
            ]

            if not matches:

                return jsonify({
                    "answer":
                    "No out-of-stock products."
                })

            return jsonify({
                "answer":
                "Out-of-stock products: " +
                ", ".join(matches)
            })

        # =====================
        # SUPPLIER LOOKUP
        # =====================

        if any(
            phrase in question
            for phrase in [
                "who supplies",
                "supplied by",
                "which supplier"
            ]
        ):

            for product in products:

                if product.name.lower() in question:

                    return jsonify({
                        "answer":
                        f"{product.supplier} supplies {product.name}"
                    })

        # =====================
        # PRODUCTS BY SUPPLIER
        # =====================

        if (
            "what products does" in question
            and "supply" in question
        ):

            matches = []

            for product in products:

                if (
                    product.supplier.lower()
                    in question
                ):

                    matches.append(
                        product.name
                    )

            return jsonify({
                "answer":
                "Products supplied: " +
                ", ".join(matches)
                if matches
                else "No products found."
            })

        # =====================
        # SUPPLIER ANALYTICS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "supplier analytics",
                "supplier analysis",
                "supplier report"
            ]
        ):

            suppliers = {}

            for product in products:

                suppliers.setdefault(
                    product.supplier,
                    {
                        "products": 0,
                        "value": 0
                    }
                )

                suppliers[product.supplier]["products"] += 1

                suppliers[product.supplier]["value"] += (
                    product.price *
                    product.quantity
                )

            result = []

            for supplier, data in suppliers.items():

                result.append(
                    f"{supplier}: "
                    f"{data['products']} products | "
                    f"Inventory Value ₹{data['value']:,.2f}"
                )

            return jsonify({
                "answer":
                "\n".join(result)
            })

        # =====================
        # PRODUCTS PER SUPPLIER
        # =====================

        if any(
            phrase in question
            for phrase in [
                "products per supplier",
                "supplier product count"
            ]
        ):

            result = {}

            for product in products:

                result[
                    product.supplier
                ] = result.get(
                    product.supplier,
                    0
                ) + 1

            return jsonify({
                "answer":
                "\n".join(
                    [
                        f"{supplier}: {count}"
                        for supplier, count
                        in result.items()
                    ]
                )
            })

        # =====================
        # SUPPLIER WITH MOST PRODUCTS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "supplier has most products",
                "which supplier has most products"
            ]
        ):

            supplier_counts = {}

            for product in products:

                supplier_counts[
                    product.supplier
                ] = supplier_counts.get(
                    product.supplier,
                    0
                ) + 1

            supplier = max(
                supplier_counts,
                key=supplier_counts.get
            )

            return jsonify({
                "answer":
                f"{supplier} supplies the most products ({supplier_counts[supplier]})"
            })

        # =====================
        # CATEGORY SEARCH
        # =====================

        for product in products:

            category = (
                product.category.lower()
            )

            if (
                f"show {category}" in question
                or f"list {category}" in question
                or f"{category} products" in question
                or f"products in {category}" in question
            ):

                matches = [
                    p.name
                    for p in products
                    if p.category.lower()
                    == category
                ]

                return jsonify({
                    "answer":
                    "Products: " +
                    ", ".join(matches)
                })

        # =====================
        # CATEGORY SUMMARY
        # =====================

        if "category summary" in question:

            categories = {}

            for product in products:

                categories[
                    product.category
                ] = categories.get(
                    product.category,
                    0
                ) + 1

            return jsonify({
                "answer":
                "\n".join(
                    [
                        f"{cat}: {count} products"
                        for cat, count
                        in categories.items()
                    ]
                )
            })

        # =====================
        # CATEGORY LOOKUP
        # =====================

        if any(
            phrase in question
            for phrase in [
                "category lookup",
                "show categories",
                "list categories"
            ]
        ):

            categories = sorted(
                list(
                    set(
                        p.category
                        for p in products
                    )
                )
            )

            return jsonify({
                "answer":
                "Categories: " +
                ", ".join(categories)
            })


        # =====================
        # SUPPLIER SUMMARY
        # =====================

        if "supplier summary" in question:

            suppliers = {}

            for product in products:

                suppliers.setdefault(
                    product.supplier,
                    []
                ).append(
                    product.name
                )

            return jsonify({
                "answer":
                "\n".join(
                    [
                        f"{supplier}: {', '.join(items)}"
                        for supplier, items
                        in suppliers.items()
                    ]
                )
            })

        # =====================
        # STOCK SHORTAGE PREDICTION
        # =====================

        if any(
            phrase in question
            for phrase in [
                "predict stock shortage",
                "stock shortage"
            ]
        ):

            risk_products = []

            for product in products:

                if (
                    product.minimum_stock > 0
                ):

                    ratio = (
                        product.quantity /
                        product.minimum_stock
                    )

                    if ratio <= 2:

                        risk_products.append(
                            product.name
                        )

            return jsonify({
                "answer":
                "Potential shortage risk: " +
                ", ".join(risk_products)
                if risk_products
                else "No products are currently at risk of stock shortage."
            })

        # =====================
        # PRODUCTS ABOVE PRICE
        # =====================

        if any(
            phrase in question
            for phrase in [
                "more than",
                "above",
                "cost more than"
            ]
        ):

            numbers = re.findall(
                r"\d+",
                question
            )

            if numbers:

                limit = float(
                    numbers[0]
                )

                matches = [
                    p.name
                    for p in products
                    if p.price > limit
                ]

                return jsonify({
                    "answer":
                    "Products: " +
                    ", ".join(matches)
                    if matches
                    else "No products found."
                })

        # =====================
        # PRODUCTS BELOW PRICE
        # =====================

        if any(
            phrase in question
            for phrase in [
                "less than",
                "below",
                "cost less than"
            ]
        ):

            numbers = re.findall(
                r"\d+",
                question
            )

            if numbers:

                limit = float(
                    numbers[0]
                )

                matches = [
                    p.name
                    for p in products
                    if p.price < limit
                ]

                return jsonify({
                    "answer":
                    "Products: " +
                    ", ".join(matches)
                    if matches
                    else "No products found."
                })


        # =====================
        # TOTAL SALES VALUE
        # =====================

        if any(
            phrase in question
            for phrase in [
                "total sales value",
                "sales value",
                "total revenue"
            ]
        ):

            transactions = Transaction.query.all()

            sales = {}

            for t in transactions:
                sales[t.product_id] = sales.get(
                    t.product_id,
                    0
                ) + t.quantity

            top_ids = sorted(
                sales,
                key=sales.get,
                reverse=True
            )[:5]

            names = []

            for pid in top_ids:

                product = Product.query.get(pid)

                if product:
                    names.append(product.name)

            return jsonify({
                "answer":
                "Top selling products: " +
                ", ".join(names)
            })


        # =====================
        # FAST MOVING PRODUCTS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "fast moving products",
                "top selling products",
                "suggest fast moving products"
            ]
        ):

            top_products = sorted(
                products,
                key=lambda p: p.quantity,
                reverse=True
            )[:5]

            return jsonify({
                "answer":
                "Fast moving products: " +
                ", ".join(
                    p.name
                    for p in top_products
                )
            })

        # =====================
        # REVENUE FORECAST
        # =====================

        if any(
            phrase in question
            for phrase in [
                "revenue forecast",
                "forecast revenue"
            ]
        ):

            inventory_value = sum(
                p.price * p.quantity
                for p in products
            )

            forecast = inventory_value * 1.10

            return jsonify({
                "answer":
                f"Predicted revenue next month: ₹{forecast:,.2f}"
            })

    
        # =====================
        # PRODUCT DETAILS
        # =====================

        if any(
            phrase in question
            for phrase in [
                "tell me about",
                "details",
                "information"
            ]
        ):

            for product in products:

                if product.name.lower() in question:

                    return jsonify({
                        "answer":
                        f"""
        Product Name: {product.name}

        SKU: {product.sku}

        Category: {product.category}

        Current Quantity: {product.quantity}

        Price: ₹{product.price}

        Supplier: {product.supplier}

        Minimum Stock: {product.minimum_stock}
        """
                    })

            docs = search_inventory(question)

            if docs:

                context = "\n\n".join(docs)

                prompt = f"""
            You are an inventory management AI assistant.

            Inventory Context:
            {context}

            User Question:
            {question}

            Answer the question using the inventory data.
            """
            print("=" * 50)
            print("CALLING GEMINI")
            print("=" * 50)
            answer = ask_gemini(prompt)

            print("=" * 50)
            print("GEMINI RESPONSE:")
            print(answer)
            print("=" * 50)

            return jsonify({
                    "answer": answer
                })

        # =====================
        # FIND PRODUCT
        # =====================

        if "find product" in question:

            search_term = (
                question
                .replace(
                    "find product",
                    ""
                )
                .strip()
            )

            for product in products:

                if (
                    search_term
                    in product.name.lower()
                ):

                    return jsonify({
                        "answer":
                        f"Found: {product.name} | Stock: {product.quantity}"
                    })

        # =====================
        # FALLBACK RAG SEARCH
        # =====================

        docs = search_inventory(
            question
        )

        if docs:

            return jsonify({
                "answer":
                docs[0]
            })

        return jsonify({
            "answer":
            "I couldn't understand that inventory question."
        })

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500