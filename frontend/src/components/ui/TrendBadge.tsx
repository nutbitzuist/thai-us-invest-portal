interface TrendBadgeProps {
  trend?: 'uptrend' | 'downtrend' | 'sideways' | string | null;
  size?: 'sm' | 'md' | 'lg';
}

export default function TrendBadge({ trend, size = 'md' }: TrendBadgeProps) {
  if (!trend) return null;

  const trendConfig = {
    uptrend: {
      bg: 'bg-uptrend',
      text: 'text-white',
      label: 'ขาขึ้น',
      icon: '↑',
    },
    downtrend: {
      bg: 'bg-downtrend',
      text: 'text-white',
      label: 'ขาลง',
      icon: '↓',
    },
    sideways: {
      bg: 'bg-sideways',
      text: 'text-black',
      label: 'ไซด์เวย์',
      icon: '→',
    },
  };

  const config = trendConfig[trend as keyof typeof trendConfig] || trendConfig.sideways;

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-1.5',
  };

  return (
    <span
      className={`
        inline-flex items-center gap-1 font-bold border-2 border-black
        ${config.bg} ${config.text} ${sizeClasses[size]}
      `}
    >
      <span>{config.icon}</span>
      <span className="font-thai">{config.label}</span>
    </span>
  );
}
