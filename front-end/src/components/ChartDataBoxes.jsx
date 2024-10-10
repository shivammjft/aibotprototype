import React from 'react';
import BarChart2 from './charts/BarChart2';
import BarChart1 from './charts/BarChart1';

const colors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', 'red', 'pink'];

const data2 = [
  {
    name: 'Page A',
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: 'Page B',
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: 'Page C',
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: 'Page D',
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: 'Page E',
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: 'Page F',
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: 'Page G',
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

const getPath = (x, y, width, height) => {
  return `M${x},${y + height}C${x + width / 3},${y + height} ${x + width / 2},${
    y + height / 3
  }
    ${x + width / 2}, ${y}
    C${x + width / 2},${y + height / 3} ${x + (2 * width) / 3},${y + height} ${
    x + width
  }, ${y + height}
    Z`;
};

const TriangleBar = (props) => {
  const { fill, x, y, width, height } = props;

  return <path d={getPath(x, y, width, height)} stroke="none" fill={fill} />;
};

const ChartDataBoxes = ({companies}) => {
  return (
    <div className="h-auto mt-[2rem] flex gap-5 ">
      <div className=" h-full w-[50%] rounded-md bg-white h-[25rem] flex flex-col items-center">
        <span className="text-2xl text-[#767B8B] font-bold mt-[1.5rem] mb-[1rem]">
         QUERIES BY COMPANIES
        </span>
        <BarChart1 companies={companies} />
      </div>
      <div className=" h-full w-[50%] rounded-md bg-white h-[25rem] flex flex-col items-center">
        <span className="text-2xl text-[#767B8B] font-bold mt-[1.5rem]">
          COMPANY WISE COSTING ($)
        </span>
        <div className="p-3">
          <BarChart2 companies={companies} />
        </div>
      </div>
    </div>
  );
};

export default ChartDataBoxes;
