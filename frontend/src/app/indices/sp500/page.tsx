'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchIndexComponents, fetchIndex } from '@/lib/api';
import Link from 'next/link';
import TrendBadge from '@/components/ui/TrendBadge';

export default function SP500Page() {
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState('weight');
  const [order, setOrder] = useState('desc');
  const [perPage, setPerPage] = useState(50);

  const { data: indexData } = useQuery({
    queryKey: ['index', 'SPX'],
    queryFn: () => fetchIndex('SPX'),
  });

  const { data: componentsData, isLoading } = useQuery({
    queryKey: ['indexComponents', 'SPX', page, sort, order, perPage],
    queryFn: () => fetchIndexComponents('SPX', page, perPage, undefined, sort, order),
  });

  const index = indexData?.data;
  const components = componentsData?.data || [];

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    if (value === 'name_asc') {
      setSort('name');
      setOrder('asc');
    } else if (value === 'change_desc') {
      setSort('change');
      setOrder('desc');
    } else if (value === 'change_asc') {
      setSort('change');
      setOrder('asc');
    } else if (value === 'trend_desc') {
      setSort('trend');
      setOrder('desc');
    } else {
      // Default / Market Cap
      setSort('weight');
      setOrder('desc');
    }
    setPage(1); // Reset to page 1 on sort change
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="border-3 border-black bg-primary text-black p-6 mb-8 shadow-brutal">
        <h1 className="font-heading text-4xl font-bold">S&P 500</h1>
        <p className="font-thai text-xl mt-2">{index?.name_th || 'ดัชนี S&P 500'}</p>
        <p className="font-thai mt-4 opacity-90">
          {index?.description_th || 'ดัชนีหุ้น 500 บริษัทขนาดใหญ่ที่สุดของสหรัฐอเมริกา'}
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
        <div className="flex items-center gap-4">
          <label className="font-heading font-bold">Sort By:</label>
          <select 
            className="border-2 border-black p-2 font-thai bg-white shadow-brutal-sm"
            onChange={handleSortChange}
            defaultValue="weight_desc"
          >
            <option value="weight_desc">Market Cap (High-Low)</option>
            <option value="name_asc">Alphabet (A-Z)</option>
            <option value="change_desc">Price Change (Best)</option>
            <option value="change_asc">Price Change (Worst)</option>
            <option value="trend_desc">Trend</option>
          </select>
        </div>
        
        <div className="flex items-center gap-4">
            <span className="font-thai text-sm bg-gray-100 px-3 py-1 border border-black">
                Total: {componentsData?.meta?.total || 0} Stocks
            </span>
        </div>
      </div>

      {/* Stock Table */}
      <div className="border-3 border-black bg-white overflow-x-auto min-h-[500px]">
        <table className="w-full">
          <thead className="bg-accent-yellow border-b-3 border-black">
            <tr>
              <th className="text-left p-4 font-heading">หุ้น</th>
              <th className="text-left p-4 font-heading">ชื่อบริษัท</th>
              <th className="text-left p-4 font-heading">กลุ่ม</th>
              <th className="text-right p-4 font-heading">ราคา</th>
              <th className="text-right p-4 font-heading">เปลี่ยนแปลง</th>
              <th className="text-center p-4 font-heading">เทรนด์</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              [...Array(10)].map((_, i) => (
                 <tr key={i} className="animate-pulse opacity-50">
                    <td colSpan={6} className="p-4 border-b border-gray-200 h-16 bg-gray-50"></td>
                 </tr>
              ))
            ) : components.length === 0 ? (
              <tr>
                <td colSpan={6} className="p-8 text-center font-thai text-gray-500">
                  ไม่พบข้อมูล - กรุณารันการ seed ข้อมูล
                </td>
              </tr>
            ) : (
              components.map((stock: any, idx: number) => (
                <tr
                  key={stock.symbol}
                  className={`border-b-2 border-black hover:bg-accent-mint/30 transition-colors ${
                    idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                  }`}
                >
                  <td className="p-4">
                    <Link
                      href={`/stocks/${stock.symbol}`}
                      className="font-heading font-bold text-lg hover:text-primary"
                    >
                      {stock.symbol}
                    </Link>
                  </td>
                  <td className="p-4 font-thai">{stock.name_th || stock.name}</td>
                  <td className="p-4">
                    {stock.sector && (
                      <span className="text-sm bg-gray-200 px-2 py-1 border border-black">
                        {stock.sector}
                      </span>
                    )}
                  </td>
                  <td className="p-4 text-right font-heading font-bold">
                    ${stock.price?.toFixed(2) ?? '—'}
                  </td>
                  <td className="p-4 text-right">
                    {stock.change_percent != null ? (
                      <span
                        className={`font-bold ${
                          stock.change_percent >= 0 ? 'text-uptrend' : 'text-downtrend'
                        }`}
                      >
                        {stock.change_percent >= 0 ? '+' : ''}
                        {stock.change_percent.toFixed(2)}%
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="p-4 text-center">
                    <TrendBadge trend={stock.trend} size="sm" />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {componentsData?.meta && componentsData.meta.total_pages > 1 && (
        <div className="mt-8 flex justify-center gap-4 items-center">
          <button 
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 border-2 border-black font-heading font-bold disabled:opacity-50 hover:bg-black hover:text-white transition-colors"
          >
            PREV
          </button>
          
          <span className="font-thai font-bold">
            หน้า {componentsData.meta.page} จาก {componentsData.meta.total_pages}
          </span>
          
          <button 
            onClick={() => setPage(p => Math.min(componentsData.meta.total_pages, p + 1))}
            disabled={page >= componentsData.meta.total_pages}
            className="px-4 py-2 border-2 border-black font-heading font-bold disabled:opacity-50 hover:bg-black hover:text-white transition-colors"
          >
            NEXT
          </button>
        </div>
      )}
    </div>
  );
}
