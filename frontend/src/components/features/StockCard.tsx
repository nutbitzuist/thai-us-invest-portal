import Link from 'next/link';
import TrendBadge from '@/components/ui/TrendBadge';
import type { StockListItem } from '@/types';

interface StockCardProps {
  stock: StockListItem;
}

export default function StockCard({ stock }: StockCardProps) {
  const isPositive = (stock.change_percent ?? 0) >= 0;

  return (
    <Link
      href={`/stocks/${stock.symbol}`}
      className="block bg-white border-3 border-black shadow-brutal p-4 hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-brutal-lg transition-all"
    >
      <div className="flex justify-between items-start mb-2">
        <div>
          <span className="font-heading font-bold text-lg">{stock.symbol}</span>
          {stock.sector && (
            <span className="ml-2 text-xs bg-gray-200 px-2 py-0.5 border border-black">
              {stock.sector}
            </span>
          )}
        </div>
        <TrendBadge trend={stock.trend} size="sm" />
      </div>
      
      <p className="font-thai text-sm text-gray-600 truncate mb-3">
        {stock.name_th || stock.name}
      </p>
      
      <div className="flex justify-between items-center">
        <span className="font-heading font-bold text-xl">
          ${stock.price?.toFixed(2) ?? '—'}
        </span>
        {stock.change_percent != null && (
          <span className={`font-bold ${isPositive ? 'text-uptrend' : 'text-downtrend'}`}>
            {isPositive ? '+' : ''}{stock.change_percent.toFixed(2)}%
          </span>
        )}
      </div>
    </Link>
  );
}
