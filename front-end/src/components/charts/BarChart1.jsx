import React, { PureComponent, useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const data = [];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div
        className="custom-tooltip"
        style={{
          padding: '10px',
          color: '#767B8B',
          backgroundColor: '#fff',
          border: '1px solid #ccc',
        }}
      >
        <p className="label">{`Name: ${payload[0].payload.name}`}</p>
        <p className="intro">{`Total Queries: ${payload[0].payload.total_queries}`}</p>
      </div>
    );
  }

  return null;
};

const BarChart1 = ({ companies }) => {
  const [barChartData, setBarChartData] = useState(data);

  useEffect(() => {
    async function getBarChartData() {
      if (companies.length > 0) {
        const updatedCompanies = companies.map((company) => {
          const cost = (
            company.input_token_cost + company.output_token_cost
          ).toFixed(3);
          const barchartobj = {
            name: company.company_name,
            total_queries: company.total_queries,
            output_tokens: company.output_tokens,
            cost: cost,
          };
          return barchartobj;
        });

        setBarChartData(updatedCompanies);
      }
    }
    getBarChartData();
  }, [companies]);
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        width={500}
        height={300}
        data={barChartData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
        barSize={20}
      >
        <XAxis dataKey="name" scale="point" padding={{ left: 10, right: 10 }} />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <CartesianGrid strokeDasharray="3 3" />
        <Bar
          dataKey="total_queries"
          fill="#8884d8"
          background={{ fill: '#eee' }}
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default BarChart1;
