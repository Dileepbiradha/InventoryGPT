function DashboardCards({

  totalProducts,
  inventoryValue,
  lowStock

}) {

  return (

    <div
      style={{
        display: "flex",
        gap: "20px",
        marginTop: "30px"
      }}
    >

      <div
        style={{
          padding: "20px",
          background: "#1f2937",
          borderRadius: "10px",
          width: "250px"
        }}
      >
        <h3>Total Products</h3>
        <h1>{totalProducts}</h1>
      </div>

      <div
        style={{
          padding: "20px",
          background: "#1f2937",
          borderRadius: "10px",
          width: "250px"
        }}
      >
        <h3>Inventory Value</h3>
        <h1>{inventoryValue}</h1>
      </div>

      <div
        style={{
          padding: "20px",
          background: "#1f2937",
          borderRadius: "10px",
          width: "250px"
        }}
      >
        <h3>Low Stock</h3>
        <h1>{lowStock}</h1>
      </div>

    </div>
  );
}

export default DashboardCards;