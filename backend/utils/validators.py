def validate_product(data):

    errors = []

    if not data.get("name"):
        errors.append("Product name is required")

    if not data.get("sku"):
        errors.append("SKU is required")

    if not data.get("price"):
        errors.append("Price is required")

    return errors