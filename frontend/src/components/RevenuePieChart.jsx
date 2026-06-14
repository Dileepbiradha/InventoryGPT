import {
 PieChart,
 Pie,
 Tooltip,
 ResponsiveContainer
} from "recharts";

const data = [
 { name: "Electronics", value: 45 },
 { name: "Clothing", value: 30 },
 { name: "Books", value: 15 },
 { name: "Others", value: 10 }
];

export default function RevenuePieChart() {
 return (
  <ResponsiveContainer width="100%" height={300}>
   <PieChart>
    <Pie
      data={data}
      dataKey="value"
      nameKey="name"
      outerRadius={100}
    />
    <Tooltip />
   </PieChart>
  </ResponsiveContainer>
 );
}