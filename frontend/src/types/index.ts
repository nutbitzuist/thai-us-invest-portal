// TypeScript types for the application

// Stock types
export interface Stock {
  symbol: string;
  name: string;
  name_th?: string;
  sector?: string;
  industry?: string;
  description?: string;
  description_th?: string;
  logo_url?: string;
  website?: string;
  exchange?: string;
  country?: string;
}

export interface StockQuote {
  symbol: string;
  price?: number;
  change_amount?: number;
  change_percent?: number;
  open_price?: number;
  high_price?: number;
  low_price?: number;
  volume?: number;
  market_cap?: number;
  pe_ratio?: number;
  eps?: number;
  week_52_high?: number;
  week_52_low?: number;
  avg_volume_10d?: number;
  dividend_yield?: number;
  sma_50?: number;
  sma_200?: number;
  trend?: 'uptrend' | 'downtrend' | 'sideways';
  updated_at?: string;
}

export interface StockListItem {
  symbol: string;
  name: string;
  name_th?: string;
  sector?: string;
  price?: number;
  change_percent?: number;
  trend?: 'uptrend' | 'downtrend' | 'sideways';
  weight?: number;
}

// ETF types
export interface ETF {
  symbol: string;
  name: string;
  name_th?: string;
  category?: string;
  provider?: string;
  expense_ratio?: number;
  aum?: number;
  description?: string;
  description_th?: string;
  inception_date?: string;
}

export interface ETFHolding {
  holding_symbol?: string;
  holding_name?: string;
  weight?: number;
  shares?: number;
}

export interface ETFListItem {
  symbol: string;
  name: string;
  name_th?: string;
  category?: string;
  provider?: string;
  expense_ratio?: number;
  aum?: number;
  price?: number;
  change_percent?: number;
  trend?: 'uptrend' | 'downtrend' | 'sideways';
}

// Index types
export interface Index {
  symbol: string;
  name: string;
  name_th?: string;
  description_th?: string;
  component_count?: number;
}

export interface IndexComponent {
  symbol: string;
  name: string;
  name_th?: string;
  sector?: string;
  weight?: number;
  price?: number;
  change_percent?: number;
  trend?: 'uptrend' | 'downtrend' | 'sideways';
}

// Analysis types
export interface Analysis {
  id: number;
  symbol: string;
  symbol_type: 'stock' | 'etf';
  title: string;
  title_th?: string;
  summary_th?: string;
  content_th: string;
  trend_opinion?: string;
  target_price?: number;
  author?: string;
  published_at?: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  meta: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

export interface SearchResult {
  stocks: StockListItem[];
  etfs: ETFListItem[];
}

// Historical price data
export interface PriceData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
