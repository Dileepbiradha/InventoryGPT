import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function LowStock() {

  const [products, setProducts] =
    useState([]);

  useEffect(() => {

    loadProducts();

  }, []);

  const loadProducts = async () => {

    const response =
      await api.get(
        "/low-stock"
      );

    setProducts(
      response.data
    );
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "30px" }}>

        <h1>
          Low Stock Products
        </h1>

        <table
          border="1"
          cellPadding="10"
          width="100%"
        >
          <thead>
            <tr>
              <th>Name</th>
              <th>SKU</th>
              <th>Quantity</th>
              <th>Minimum</th>
              <th>Supplier</th>
            </tr>
          </thead>

          <tbody>

            {products.map(
              (product) => (

                <tr key={product.id}>

                  <td>
                    {product.name}
                  </td>

                  <td>
                    {product.sku}
                  </td>

                  <td>
                    {product.quantity}
                  </td>

                  <td>
                    {product.minimum_stock}
                  </td>

                  <td>
                    {product.supplier}
                  </td>

                </tr>
              )
            )}

          </tbody>
        </table>

      </div>
    </>
  );
}

export default LowStock;