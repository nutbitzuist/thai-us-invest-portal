'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchSearch } from '@/lib/api';
import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';
import Link from 'next/link';
import TrendBadge from '@/components/ui/TrendBadge';
import SearchBar from '@/components/features/SearchBar';

function SearchContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';

  const { data, isLoading } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetchSearch(query),
    enabled: query.length > 0,
  });

  const stocks = data?.data?.stocks || [];
  const etfs = data?.data?.etfs || [];
  const hasResults = stocks.length > 0 || etfs.length > 0;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Search Header */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold mb-4">ค้นหา</h1>
        <div className="max-w-xl">
          <SearchBar />
        </div>
        {query && (
          <p className="font-thai mt-4 text-gray-600">
            ผลการค้นหา "{query}"
          </p>
        )}
      </div>

      {isLoading && (
        <div className="animate-pulse space-y-4">
          <div className="h-16 bg-gray-200"></div>
          <div className="h-16 bg-gray-200"></div>
          <div className="h-16 bg-gray-200"></div>
        </div>
      )}

      {!isLoading && query && !hasResults && (
        <div className="border-3 border-black bg-white p-8 text-center">
          <p className="font-thai text-xl text-gray-600">
            ไม่พบผลการค้นหาสำหรับ "{query}"
          </p>
          <p className="font-thai mt-2 text-gray-500">
            ลองค้นหาด้วยคำอื่น เช่น AAPL, MSFT, SPY
          </p>
        </div>
      )}

      {/* Stock Results */}
      {stocks.length > 0 && (
        <div className="mb-8">
          <h2 className="font-heading text-2xl font-bold mb-4 flex items-center gap-2">
            หุ้น
            <span className="bg-primary text-black text-sm px-2 py-1 border-2 border-black">
              {stocks.length}
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stocks.map((stock: any) => (
              <Link
                key={stock.symbol}
                href={`/stocks/${stock.symbol}`}
                className="border-3 border-black bg-white p-4 shadow-brutal hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-brutal-lg transition-all"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <span className="font-heading font-bold text-lg">{stock.symbol}</span>
                    <p className="font-thai text-sm text-gray-600 mt-1">
                      {stock.name_th || stock.name}
                    </p>
                  </div>
                  <TrendBadge trend={stock.trend} size="sm" />
                </div>
                <div className="flex justify-between items-center mt-4">
                  <span className="font-heading font-bold">
                    ${stock.price?.toFixed(2) ?? '—'}
                  </span>
                  {stock.change_percent != null && (
                    <span className={`font-bold ${stock.change_percent >= 0 ? 'text-uptrend' : 'text-downtrend'}`}>
                      {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent.toFixed(2)}%
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* ETF Results */}
      {etfs.length > 0 && (
        <div>
          <h2 className="font-heading text-2xl font-bold mb-4 flex items-center gap-2">
            ETF
            <span className="bg-secondary text-black text-sm px-2 py-1 border-2 border-black">
              {etfs.length}
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {etfs.map((etf: any) => (
              <Link
                key={etf.symbol}
                href={`/etf/${etf.symbol}`}
                className="border-3 border-black bg-white p-4 shadow-brutal hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-brutal-lg transition-all"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <span className="font-heading font-bold text-lg">{etf.symbol}</span>
                    <p className="font-thai text-sm text-gray-600 mt-1">
                      {etf.name_th || etf.name}
                    </p>
                  </div>
                  <TrendBadge trend={etf.trend} size="sm" />
                </div>
                {etf.category && (
                  <span className="inline-block mt-2 text-xs bg-accent-yellow px-2 py-0.5 border border-black">
                    {etf.category}
                  </span>
                )}
                <div className="flex justify-between items-center mt-4">
                  <span className="font-heading font-bold">
                    ${etf.price?.toFixed(2) ?? '—'}
                  </span>
                  {etf.change_percent != null && (
                    <span className={`font-bold ${etf.change_percent >= 0 ? 'text-uptrend' : 'text-downtrend'}`}>
                      {etf.change_percent >= 0 ? '+' : ''}{etf.change_percent.toFixed(2)}%
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">กำลังโหลด...</div>}>
      <SearchContent />
    </Suspense>
  );
}
