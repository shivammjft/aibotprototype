import React from 'react';
import { PieChart, Pie, Sector, Cell, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Group A', value: 400 },
  { name: 'Group B', value: 300 },
  { name: 'Group C', value: 300 },
  { name: 'Group D', value: 200 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
  index,
}) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? 'start' : 'end'}
      dominantBaseline="central"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const TotalSalesPieChart = () => {
  return (
    <div className=" h-full  flex items-start justify-start  flex-col">
      <ResponsiveContainer width="100%" height="70%">
        <PieChart width={100} height={100}>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            className="border border-green-800"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className=" h-[6rem] w-full flex gap-5 flex-wrap p-4">
        <div className="flex gap-1 items-center  h-[2rem] ">
          <div className=" w-[0.6rem] h-[0.6rem] bg-[#FF8042]"></div>
          <p>Direct</p>
        </div>
        <div className="flex gap-1 items-center   h-[2rem] ">
          <div className=" w-[0.6rem] h-[0.6rem] bg-[#FFBB28]"></div>
          <p>Affiliate</p>
        </div>
        <div className="flex gap-1 items-center  h-[2rem] ">
          <div className=" w-[0.6rem] h-[0.6rem] bg-[#00C49F]"></div>
          <p>Sponsored</p>
        </div>
        <div className="flex gap-1 items-center   h-[2rem] ">
          <div className=" w-[0.6rem] h-[0.6rem] bg-[#0088FE]"></div>
          <p>E-mail</p>
        </div>
      </div>
    </div>
  );
};

export default TotalSalesPieChart;
