import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const fetchIndices = async () => {
  const { data } = await api.get('/api/indices');
  return data;
};

export const fetchIndex = async (symbol: string) => {
  const { data } = await api.get(`/api/indices/${symbol}`);
  return data;
};

export const fetchIndexComponents = async (
  symbol: string,
  page = 1,
  perPage = 50,
  sector?: string,
  sort = 'weight',
  order = 'desc'
) => {
  const params = new URLSearchParams({
    page: page.toString(),
    per_page: perPage.toString(),
    sort,
    order,
  });
  if (sector) params.set('sector', sector);
  
  const { data } = await api.get(`/api/indices/${symbol}/components?${params}`);
  return data;
};

export const fetchStocks = async (page = 1, perPage = 20, sector?: string, search?: string) => {
  const params = new URLSearchParams({
    page: page.toString(),
    per_page: perPage.toString(),
  });
  if (sector) params.set('sector', sector);
  if (search) params.set('search', search);
  
  const { data } = await api.get(`/api/stocks?${params}`);
  return data;
};

export const fetchStock = async (symbol: string) => {
  const { data } = await api.get(`/api/stocks/${symbol}`);
  return data;
};

export const fetchStockQuote = async (symbol: string) => {
  const { data } = await api.get(`/api/stocks/${symbol}/quote`);
  return data;
};

export const fetchStockHistory = async (symbol: string, period = '1y') => {
  const { data } = await api.get(`/api/stocks/${symbol}/history?period=${period}`);
  return data;
};

export const fetchStockAnalysis = async (symbol: string) => {
  const { data } = await api.get(`/api/stocks/${symbol}/analysis`);
  return data;
};

export const fetchETFs = async (page = 1, perPage = 20, category?: string) => {
  const params = new URLSearchParams({
    page: page.toString(),
    per_page: perPage.toString(),
  });
  if (category) params.set('category', category);
  
  const { data } = await api.get(`/api/etfs?${params}`);
  return data;
};

export const fetchTop50ETFs = async () => {
  const { data } = await api.get('/api/etfs/top50');
  return data;
};

export const fetchETF = async (symbol: string) => {
  const { data } = await api.get(`/api/etfs/${symbol}`);
  return data;
};

export const fetchETFQuote = async (symbol: string) => {
  const { data } = await api.get(`/api/etfs/${symbol}/quote`);
  return data;
};

export const fetchETFHoldings = async (symbol: string, limit = 20) => {
  const { data } = await api.get(`/api/etfs/${symbol}/holdings?limit=${limit}`);
  return data;
};

export const fetchSearch = async (query: string, type = 'all') => {
  const { data } = await api.get(`/api/search?q=${encodeURIComponent(query)}&type=${type}`);
  return data;
};
