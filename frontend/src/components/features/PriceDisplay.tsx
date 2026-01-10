interface PriceDisplayProps {
  price?: number | null;
  change?: number | null;
  changePercent?: number | null;
  size?: 'sm' | 'md' | 'lg';
}

export default function PriceDisplay({ price, change, changePercent, size = 'md' }: PriceDisplayProps) {
  const isPositive = (changePercent ?? 0) >= 0;

  const sizeClasses = {
    sm: { price: 'text-lg', change: 'text-sm' },
    md: { price: 'text-2xl', change: 'text-base' },
    lg: { price: 'text-4xl', change: 'text-lg' },
  };

  const formatPrice = (num: number) => {
    return num.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  const formatPercent = (num: number) => {
    const prefix = num >= 0 ? '+' : '';
    return `${prefix}${num.toFixed(2)}%`;
  };

  return (
    <div className="flex items-baseline gap-3">
      <span className={`font-heading font-bold ${sizeClasses[size].price}`}>
        ${price ? formatPrice(price) : '—'}
      </span>
      {changePercent != null && (
        <span
          className={`
            font-bold ${sizeClasses[size].change}
            ${isPositive ? 'text-uptrend' : 'text-downtrend'}
          `}
        >
          {formatPercent(changePercent)}
          {change != null && (
            <span className="ml-1 opacity-80">
              ({isPositive ? '+' : ''}{change.toFixed(2)})
            </span>
          )}
        </span>
      )}
    </div>
  );
}
