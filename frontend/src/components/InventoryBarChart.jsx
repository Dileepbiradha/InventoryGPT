import {
 BarChart,
 Bar,
 XAxis,
 YAxis,
 Tooltip,
 ResponsiveContainer
} from "recharts";

const data = [
 { name: "Laptop", quantity: 120 },
 { name: "Mouse", quantity: 200 },
 { name: "Keyboard", quantity: 80 },
 { name: "Monitor", quantity: 140 }
];

export default function InventoryBarChart() {
 return (
  <ResponsiveContainer width="100%" height={300}>
   <BarChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
    <Bar dataKey="quantity" />
   </BarChart>
  </ResponsiveContainer>
 );
}