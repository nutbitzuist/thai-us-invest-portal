'use client';

import { useEffect, useRef, useId } from 'react';

interface TradingViewChartProps {
  symbol: string;
  exchange?: string;
  theme?: 'light' | 'dark';
  height?: number;
}

export default function TradingViewChart({ symbol, exchange, theme = 'light', height = 400 }: TradingViewChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const rawId = useId();
  const chartId = `tradingview_${rawId.replace(/:/g, '-')}`;

  useEffect(() => {
    if (!containerRef.current) return;

    // Clear previous widget
    containerRef.current.innerHTML = '';

    // Create container div
    const widgetContainer = document.createElement('div');
    widgetContainer.id = chartId;
    widgetContainer.className = 'tradingview-widget-container__widget';
    widgetContainer.style.height = '100%';
    widgetContainer.style.width = '100%';
    containerRef.current.appendChild(widgetContainer);

    // Format symbol (e.g. NASDAQ:AAPL) if exchange provided
    // For ETFs like SPY/QQQ, TradingView auto-detects correctly without prefix
    // For stocks, we use common exchange mappings
    let chartSymbol = symbol;
    if (exchange) {
      chartSymbol = `${exchange}:${symbol}`;
    } else {
      // Try common US exchanges - TradingView prefers NASDAQ format for tech stocks
      // and AMEX (ARCX) for ETFs - but auto-detection usually works
      chartSymbol = symbol.toUpperCase();
    }

    // Create script
    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
    script.type = 'text/javascript';
    script.async = true;
    script.innerHTML = JSON.stringify({
      autosize: true,
      symbol: chartSymbol,
      interval: 'D',
      timezone: 'Asia/Bangkok',
      theme: theme,
      style: '1',
      locale: 'th_TH',
      enable_publishing: false,
      allow_symbol_change: true,
      calendar: false,
      support_host: 'https://www.tradingview.com',
      container_id: chartId,
    });

    const currentContainer = containerRef.current;
    currentContainer.appendChild(script);

    return () => {
      if (currentContainer) {
        currentContainer.innerHTML = '';
      }
    };
  }, [symbol, exchange, theme, height, chartId]);

  return (
    <div className="border-3 border-black bg-white overflow-hidden w-full" style={{ height: `${height}px` }}>
      <div className="tradingview-widget-container" ref={containerRef} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}
