'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchETF, fetchETFQuote, fetchETFHoldings } from '@/lib/api';
import { useParams } from 'next/navigation';
import TrendBadge from '@/components/ui/TrendBadge';
import PriceDisplay from '@/components/features/PriceDisplay';
import BrutalButton from '@/components/ui/BrutalButton';
import TradingViewChart from '@/components/charts/TradingViewChart';
import Link from 'next/link';

export default function ETFDetailPage() {
  const params = useParams();
  const symbol = (params.symbol as string).toUpperCase();

  const { data: etfData, isLoading } = useQuery({
    queryKey: ['etf', symbol],
    queryFn: () => fetchETF(symbol),
  });

  const { data: quoteData } = useQuery({
    queryKey: ['etfQuote', symbol],
    queryFn: () => fetchETFQuote(symbol),
  });

  const { data: holdingsData } = useQuery({
    queryKey: ['etfHoldings', symbol],
    queryFn: () => fetchETFHoldings(symbol, 20),
  });

  const etf = etfData?.data;
  const quote = quoteData?.data;
  const holdings = holdingsData?.data || [];

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-12 bg-gray-200 w-1/3"></div>
          <div className="h-8 bg-gray-200 w-1/2"></div>
          <div className="h-96 bg-gray-200"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="border-3 border-black bg-white p-6 mb-6 shadow-brutal">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="font-heading text-4xl font-bold">{symbol}</h1>
            <p className="font-thai text-xl text-gray-600">
              {etf?.name_th || etf?.name}
            </p>
            <div className="flex flex-wrap gap-2 mt-4">
              {etf?.category && (
                <span className="bg-accent-yellow px-3 py-1 border-2 border-black text-sm font-medium">
                  {etf.category}
                </span>
              )}
              {etf?.provider && (
                <span className="bg-secondary px-3 py-1 border-2 border-black text-sm">
                  {etf.provider}
                </span>
              )}
              <TrendBadge trend={quote?.trend} size="md" />
            </div>
          </div>
          <div className="text-right">
            <PriceDisplay
              price={quote?.price}
              change={quote?.change_amount}
              changePercent={quote?.change_percent}
              size="lg"
            />
          </div>
        </div>
      </div>

      {/* TradingView Chart */}
      <div className="mb-6">
        <TradingViewChart symbol={symbol} height={500} />
      </div>

      {/* ETF Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[
          { label: 'สินทรัพย์รวม (AUM)', value: etf?.aum ? `$${(etf.aum / 1e9).toFixed(2)}B` : '—' },
          { label: 'ค่าใช้จ่าย (Expense)', value: etf?.expense_ratio ? `${(etf.expense_ratio * 100).toFixed(2)}%` : '—' },
          { label: 'ปันผล', value: quote?.dividend_yield ? `${(quote.dividend_yield * 100).toFixed(2)}%` : '—' },
          { label: 'วันจัดตั้ง', value: etf?.inception_date || '—' },
        ].map((item) => (
          <div key={item.label} className="border-3 border-black bg-white p-4 shadow-brutal-sm">
            <p className="font-thai text-sm text-gray-600">{item.label}</p>
            <p className="font-heading text-xl font-bold">{item.value}</p>
          </div>
        ))}
      </div>

      {/* Top Holdings */}
      {holdings.length > 0 && (
        <div className="border-3 border-black bg-white mb-6">
          <div className="bg-accent-mint border-b-3 border-black p-4">
            <h2 className="font-heading text-xl font-bold">สัดส่วนการถือครอง</h2>
          </div>
          <table className="w-full">
            <thead className="border-b-2 border-black bg-gray-50">
              <tr>
                <th className="text-left p-3 font-thai">หุ้น</th>
                <th className="text-left p-3 font-thai">ชื่อ</th>
                <th className="text-right p-3 font-thai">สัดส่วน</th>
              </tr>
            </thead>
            <tbody>
              {holdings.map((holding: any, idx: number) => (
                <tr key={idx} className="border-b border-gray-200">
                  <td className="p-3">
                    {holding.holding_symbol ? (
                      <Link
                        href={`/stocks/${holding.holding_symbol}`}
                        className="font-heading font-bold hover:text-primary"
                      >
                        {holding.holding_symbol}
                      </Link>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="p-3 font-thai text-sm">{holding.holding_name || '—'}</td>
                  <td className="p-3 text-right font-bold">
                    {holding.weight ? `${holding.weight.toFixed(2)}%` : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Description */}
      {etf?.description && (
        <div className="border-3 border-black bg-white p-6 mb-6 shadow-brutal">
          <h2 className="font-heading text-xl font-bold mb-4">เกี่ยวกับกองทุน</h2>
          <p className="font-thai">{etf.description_th || etf.description}</p>
        </div>
      )}

      {/* External Links */}
      <div className="flex flex-wrap gap-4">
        <BrutalButton
          variant="yellow"
          onClick={() => window.open(`https://finance.yahoo.com/quote/${symbol}`, '_blank')}
        >
          Yahoo Finance ↗
        </BrutalButton>
      </div>
    </div>
  );
}
