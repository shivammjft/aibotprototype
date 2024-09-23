import React from 'react'
import TotalSalesPieChart from '../charts/TotalSalesPieChart'

const TotalSalesContainer = () => {
  return (
    <div className="w-[25%]  shadow-md bg-white p-3 text-[#6D767E]  flex flex-col">
    <span className="flex items-center justify-between font-bold mt-[1rem]">
      TOTAL SALES
    </span>
    <TotalSalesPieChart />
  </div>
  )
}

export default TotalSalesContainer
