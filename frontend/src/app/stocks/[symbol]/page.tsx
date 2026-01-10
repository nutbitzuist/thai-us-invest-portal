'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchStock, fetchStockQuote, fetchStockAnalysis } from '@/lib/api';
import { useParams } from 'next/navigation';
import TrendBadge from '@/components/ui/TrendBadge';
import PriceDisplay from '@/components/features/PriceDisplay';
import BrutalButton from '@/components/ui/BrutalButton';
import TradingViewChart from '@/components/charts/TradingViewChart';

export default function StockDetailPage() {
  const params = useParams();
  const symbol = (params.symbol as string).toUpperCase();

  const { data: stockData, isLoading: stockLoading } = useQuery({
    queryKey: ['stock', symbol],
    queryFn: () => fetchStock(symbol),
  });

  const { data: quoteData } = useQuery({
    queryKey: ['stockQuote', symbol],
    queryFn: () => fetchStockQuote(symbol),
  });

  const { data: analysisData } = useQuery({
    queryKey: ['stockAnalysis', symbol],
    queryFn: () => fetchStockAnalysis(symbol),
  });

  const stock = stockData?.data;
  const quote = quoteData?.data;
  const analysis = analysisData?.data;

  if (stockLoading) {
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
            <div className="flex items-center gap-4">
              {stock?.logo_url && (
                <img
                  src={stock.logo_url}
                  alt={stock.name}
                  className="w-16 h-16 border-3 border-black object-contain bg-white"
                  onError={(e) => (e.currentTarget.style.display = 'none')}
                />
              )}
              <div>
                <h1 className="font-heading text-4xl font-bold">{symbol}</h1>
                <p className="font-thai text-xl text-gray-600">
                  {stock?.name_th || stock?.name}
                </p>
              </div>
            </div>
            <div className="flex flex-wrap gap-2 mt-4">
              {stock?.sector && (
                <span className="bg-accent-yellow px-3 py-1 border-2 border-black text-sm font-medium">
                  {stock.sector}
                </span>
              )}
              {stock?.industry && (
                <span className="bg-gray-200 px-3 py-1 border-2 border-black text-sm">
                  {stock.industry}
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
            {quote?.updated_at && (
              <p className="font-thai text-sm text-gray-500 mt-2">
                อัพเดท: {new Date(quote.updated_at).toLocaleString('th-TH')}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* TradingView Chart */}
      <div className="mb-6">
        <TradingViewChart symbol={symbol} exchange={stock?.exchange} height={500} />
      </div>

      {/* Metrics Grid */}
      {quote && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {[
            { label: 'มูลค่าตลาด', value: quote.market_cap ? `$${(quote.market_cap / 1e9).toFixed(2)}B` : '—' },
            { label: 'P/E Ratio', value: quote.pe_ratio?.toFixed(2) || '—' },
            { label: 'EPS', value: quote.eps ? `$${quote.eps.toFixed(2)}` : '—' },
            { label: 'ปันผล', value: quote.dividend_yield ? `${(quote.dividend_yield * 100).toFixed(2)}%` : '—' },
            { label: 'สูงสุด 52 สัปดาห์', value: quote.week_52_high ? `$${quote.week_52_high.toFixed(2)}` : '—' },
            { label: 'ต่ำสุด 52 สัปดาห์', value: quote.week_52_low ? `$${quote.week_52_low.toFixed(2)}` : '—' },
            { label: 'SMA 50', value: quote.sma_50 ? `$${quote.sma_50.toFixed(2)}` : '—' },
            { label: 'SMA 200', value: quote.sma_200 ? `$${quote.sma_200.toFixed(2)}` : '—' },
          ].map((item) => (
            <div key={item.label} className="border-3 border-black bg-white p-4 shadow-brutal-sm">
              <p className="font-thai text-sm text-gray-600">{item.label}</p>
              <p className="font-heading text-xl font-bold">{item.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* Analysis Section */}
      {analysis && (
        <div className="border-3 border-black bg-accent-mint p-6 mb-6 shadow-brutal">
          <h2 className="font-heading text-2xl font-bold mb-4">บทวิเคราะห์</h2>
          <h3 className="font-thai text-xl font-bold mb-2">{analysis.title_th || analysis.title}</h3>
          {analysis.author && (
            <p className="font-thai text-sm text-gray-600 mb-4">
              โดย {analysis.author} • {analysis.published_at ? new Date(analysis.published_at).toLocaleDateString('th-TH') : ''}
            </p>
          )}
          <div className="font-thai whitespace-pre-wrap">{analysis.content_th}</div>
          {analysis.trend_opinion && (
            <div className="mt-4 p-4 bg-white border-3 border-black">
              <span className="font-bold">ความเห็นนักวิเคราะห์: </span>
              <TrendBadge trend={analysis.trend_opinion} />
              {analysis.target_price && (
                <span className="ml-4">ราคาเป้าหมาย: <strong>${analysis.target_price.toFixed(2)}</strong></span>
              )}
            </div>
          )}
        </div>
      )}

      {/* Description */}
      {stock?.description && (
        <div className="border-3 border-black bg-white p-6 mb-6 shadow-brutal">
          <h2 className="font-heading text-xl font-bold mb-4">เกี่ยวกับบริษัท</h2>
          <p className="font-thai">{stock.description_th || stock.description}</p>
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
        {stock?.website && (
          <BrutalButton
            variant="outline"
            onClick={() => window.open(stock.website, '_blank')}
          >
            เว็บไซต์บริษัท ↗
          </BrutalButton>
        )}
      </div>
    </div>
  );
}
