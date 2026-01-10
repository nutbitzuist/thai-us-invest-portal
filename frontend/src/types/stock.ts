export interface Stock {
  id: number;
  symbol: string;
  name: string;
  name_th?: string;
  sector?: string;
  industry?: string;
  description?: string;
  description_th?: string;
  logo_url?: string;
  website?: string;
  ceo?: string;
  employees?: number;
  headquarters?: string;
  founded_year?: number;
  exchange?: string;
  country?: string;
  price?: number; // Optional if flattened
  change_percent?: number;
}

export interface LatestQuote {
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
  dividend_yield?: number;
  trend?: 'uptrend' | 'downtrend' | 'sideways';
  updated_at?: string;
}

export interface StockAnalysis {
    id: number;
    title: string;
    title_th?: string;
    summary_th?: string;
    content_th: string;
    trend_opinion?: string;
    target_price?: number;
    author?: string;
    published_at?: string;
}
