import React from 'react'
import DownloadIcon from '../assets/icons/DownloadIcon'


const TopSellingProductsTable = () => {
  return (
    <div className=" w-[60%] shadow-md bg-white  text-[#6D767E]  flex flex-col h-[28rem] rounded-md p-5 ">
              <span className="flex items-center justify-between font-bold">
                TOP SELLING PRODUCTS
                <button className="bg-[#EEF2F7] p-2 w-[7rem] text-black text-sm flex gap-2 items-center justify-center">
                  Export <DownloadIcon/>
                </button>
              </span>
              <ul className=" flex flex-col ">
                <li className=" flex items-center justify-between mt-[1rem] p-2 ">
                  <span className="flex flex-col gap-1">
                    <p>ASOS Ridley High Waist</p>
                    <p className="text-sm text-[#959EA2]">07 April 2018</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$79.49</p>
                    <p className="text-sm text-[#959EA2]">Price</p>
                  </span>
                  <span className="flex flex-col gap-1">
                    <p>82</p>
                    <p className="text-sm text-[#959EA2]">Quantity</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$6,518.18</p>
                    <p className="text-sm text-[#959EA2]">Amount</p>
                  </span>
                </li>
                <hr className="mt-[0.5rem]" />
                <li className=" flex items-center justify-between mt-[1rem] p-2 ">
                  <span className="flex flex-col gap-1">
                    <p>ASOS Ridley High Waist</p>
                    <p className="text-sm text-[#959EA2]">07 April 2018</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$79.49</p>
                    <p className="text-sm text-[#959EA2]">Price</p>
                  </span>
                  <span className="flex flex-col gap-1">
                    <p>82</p>
                    <p className="text-sm text-[#959EA2]">Quantity</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$6,518.18</p>
                    <p className="text-sm text-[#959EA2]">Amount</p>
                  </span>
                </li>
                <hr className="mt-[0.5rem]" />
                <li className=" flex items-center justify-between mt-[1rem] p-2 ">
                  <span className="flex flex-col gap-1">
                    <p>ASOS Ridley High Waist</p>
                    <p className="text-sm text-[#959EA2]">07 April 2018</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$79.49</p>
                    <p className="text-sm text-[#959EA2]">Price</p>
                  </span>
                  <span className="flex flex-col gap-1">
                    <p>82</p>
                    <p className="text-sm text-[#959EA2]">Quantity</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$6,518.18</p>
                    <p className="text-sm text-[#959EA2]">Amount</p>
                  </span>
                </li>
                <hr className="mt-[0.5rem]" />
                <li className=" flex items-center justify-between mt-[1rem] p-2 ">
                  <span className="flex flex-col gap-1">
                    <p>ASOS Ridley High Waist</p>
                    <p className="text-sm text-[#959EA2]">07 April 2018</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$79.49</p>
                    <p className="text-sm text-[#959EA2]">Price</p>
                  </span>
                  <span className="flex flex-col gap-1">
                    <p>82</p>
                    <p className="text-sm text-[#959EA2]">Quantity</p>
                  </span>
                  <span className=" flex flex-col gap-1">
                    <p>$6,518.18</p>
                    <p className="text-sm text-[#959EA2]">Amount</p>
                  </span>
                </li>
                <hr className="mt-[0.5rem]" />
              </ul>
            </div>
  )
}

export default TopSellingProductsTable