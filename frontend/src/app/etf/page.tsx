'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchTop50ETFs } from '@/lib/api';
import Link from 'next/link';
import TrendBadge from '@/components/ui/TrendBadge';

export default function ETFListPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['top50ETFs'],
    queryFn: fetchTop50ETFs,
  });

  const etfs = data?.data || [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="border-3 border-black bg-accent-yellow p-6 mb-8 shadow-brutal">
        <h1 className="font-heading text-4xl font-bold">50 กองทุน ETF ยอดนิยม</h1>
        <p className="font-thai text-xl mt-2">
          รวม ETF ที่นักลงทุนทั่วโลกนิยมลงทุนมากที่สุด
        </p>
      </div>

      {/* ETF Table */}
      <div className="border-3 border-black bg-white overflow-x-auto">
        <table className="w-full">
          <thead className="bg-accent-mint border-b-3 border-black">
            <tr>
              <th className="text-left p-4 font-heading">ETF</th>
              <th className="text-left p-4 font-heading">ชื่อกองทุน</th>
              <th className="text-left p-4 font-heading">ประเภท</th>
              <th className="text-left p-4 font-heading">ผู้ให้บริการ</th>
              <th className="text-right p-4 font-heading">ราคา</th>
              <th className="text-right p-4 font-heading">เปลี่ยนแปลง</th>
              <th className="text-center p-4 font-heading">เทรนด์</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={7} className="p-8 text-center font-thai">
                  <div className="animate-pulse">กำลังโหลด...</div>
                </td>
              </tr>
            ) : etfs.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-8 text-center font-thai text-gray-500">
                  ไม่พบข้อมูล - กรุณารันการ seed ข้อมูล
                </td>
              </tr>
            ) : (
              etfs.map((etf: any, idx: number) => (
                <tr
                  key={etf.symbol}
                  className={`border-b-2 border-black hover:bg-accent-yellow/30 transition-colors ${
                    idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                  }`}
                >
                  <td className="p-4">
                    <Link
                      href={`/etf/${etf.symbol}`}
                      className="font-heading font-bold text-lg hover:text-primary"
                    >
                      {etf.symbol}
                    </Link>
                  </td>
                  <td className="p-4 font-thai">{etf.name_th || etf.name}</td>
                  <td className="p-4">
                    {etf.category && (
                      <span className="text-sm bg-gray-200 px-2 py-1 border border-black">
                        {etf.category}
                      </span>
                    )}
                  </td>
                  <td className="p-4 font-thai text-sm">{etf.provider || '—'}</td>
                  <td className="p-4 text-right font-heading font-bold">
                    ${etf.price?.toFixed(2) ?? '—'}
                  </td>
                  <td className="p-4 text-right">
                    {etf.change_percent != null ? (
                      <span
                        className={`font-bold ${
                          etf.change_percent >= 0 ? 'text-uptrend' : 'text-downtrend'
                        }`}
                      >
                        {etf.change_percent >= 0 ? '+' : ''}
                        {etf.change_percent.toFixed(2)}%
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="p-4 text-center">
                    <TrendBadge trend={etf.trend} size="sm" />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
