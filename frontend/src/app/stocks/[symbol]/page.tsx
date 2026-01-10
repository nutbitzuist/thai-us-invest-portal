'use client';

import { useQuery } from '@tanstack/react-query';
import { useParams } from 'next/navigation';
import { fetchStock, fetchStockQuote, fetchStockAnalysis } from '@/lib/api';
import TradingViewChart from '@/components/charts/TradingViewChart';
import CompanyProfile from '@/components/features/CompanyProfile';
import StockAnalysis from '@/components/features/StockAnalysis';
import { Stock, LatestQuote, StockAnalysis as IStockAnalysis } from '@/types/stock';

export default function StockDetailPage() {
  const params = useParams();
  const symbol = params.symbol as string;

  const { data: stockData, isLoading: stockLoading } = useQuery({
    queryKey: ['stock', symbol],
    queryFn: () => fetchStock(symbol),
  });

  const { data: quoteData } = useQuery({
    queryKey: ['quote', symbol],
    queryFn: () => fetchStockQuote(symbol),
    refetchInterval: 60000,
  });

  const { data: analysisData } = useQuery({
    queryKey: ['analysis', symbol],
    queryFn: () => fetchStockAnalysis(symbol),
  });

  const stock = stockData?.data as Stock;
  const quote = quoteData?.data as LatestQuote;
  const analysis = analysisData?.data as IStockAnalysis;

  if (stockLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="font-mono text-2xl font-bold animate-pulse">Loading {symbol}...</div>
      </div>
    );
  }

  if (!stock) return <div className="p-8 text-center font-bold text-xl">Stock not found</div>;

  const isPositive = quote?.change_amount && quote.change_amount >= 0;

  return (
    <div className="min-h-screen bg-background pb-20">
      <div className="container mx-auto px-4 py-8">
         {/* Row 1: Header */}
         <div className="mb-8 p-6 bg-white border-3 border-black shadow-brutal">
             <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                 <div>
                    <div className="flex items-center gap-3 mb-2">
                        {stock.logo_url && (
                             <img src={stock.logo_url} alt={stock.symbol} className="w-12 h-12 object-contain" />
                        )}
                        <h1 className="text-4xl md:text-6xl font-black font-heading tracking-tight uppercase">
                            {stock.symbol}
                        </h1>
                        <span className="bg-gray-200 border-2 border-black px-2 py-1 text-xs font-bold font-mono">
                            {stock.exchange || 'NYSE'}
                        </span>
                    </div>
                     <h2 className="text-xl font-thai font-bold text-gray-700">
                         {stock.name_th || stock.name}
                     </h2>
                 </div>
                 {quote && (
                    <div className="text-right">
                        <div className="text-5xl font-mono font-bold mb-1 tracking-tighter">
                            ${quote.price?.toFixed(2)}
                        </div>
                        <div className="flex justify-end items-center gap-2">
                             <span className={`font-bold font-mono text-lg ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                                {quote.change_amount && quote.change_amount > 0 ? '+' : ''}{quote.change_amount?.toFixed(2)}
                             </span>
                             <span className={`px-3 py-1 font-bold border-2 border-black text-sm ${isPositive ? 'bg-accent-mint' : 'bg-accent-salmon'}`}>
                                {isPositive ? '▲' : '▼'} {Math.abs(quote.change_percent || 0).toFixed(2)}%
                             </span>
                        </div>
                        <div className="text-xs text-gray-500 font-mono mt-1">
                            Updated: {quote.updated_at ? new Date(quote.updated_at).toLocaleTimeString() : '-'}
                        </div>
                    </div>
                 )}
             </div>
         </div>

         <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
             {/* Main Content (Chart + Analysis) */}
             <div className="lg:col-span-8 flex flex-col gap-8">
                 {/* Chart */}
                 <div className="h-[550px] w-full border-3 border-black shadow-brutal bg-white overflow-hidden relative">
                     <TradingViewChart symbol={stock.symbol} exchange={stock.exchange} />
                 </div>
                 
                 {/* Analysis */}
                 <StockAnalysis 
                    symbol={stock.symbol} 
                    analysis={analysis} 
                    description={stock.description} 
                 />
             </div>

             {/* Sidebar (Profile) */}
             <div className="lg:col-span-4">
                 <CompanyProfile stock={stock} quote={quote} />
             </div>
         </div>
      </div>
    </div>
  );
}
