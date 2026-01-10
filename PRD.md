# Product Requirements Document (PRD)
# Thai U.S. Investment Portal (ศูนย์ข้อมูลลงทุนหุ้นสหรัฐ)

## Document Info
- **Version:** 1.0
- **Last Updated:** January 2025
- **Status:** Ready for Development

---

## 1. Executive Summary

### 1.1 Product Vision
Build the go-to website for Thai investors who want to understand and invest in U.S. stocks and ETFs. The platform provides comprehensive information about S&P 500, Nasdaq 100 indices, and top 50 ETFs with Thai language analysis and educational content.

### 1.2 Target Users
- Thai retail investors interested in U.S. markets
- Thai people new to U.S. stock investing
- Investors looking for Thai-language analysis of U.S. companies

### 1.3 Core Value Proposition
- All U.S. investment information in one place
- Thai language analysis and explanations
- Easy-to-understand trend indicators
- Professional charts via TradingView
- Direct links to Yahoo Finance for deeper research

---

## 2. Architecture Overview

### 2.1 System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                        │
│                    Next.js 14 + TypeScript                  │
│                    Neo-Brutalism Design                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (HTTPS)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Railway)                        │
│                    Python FastAPI                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   REST API  │  │  Scheduler  │  │   Workers   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                           │                                 │
│           ┌───────────────┼───────────────┐                │
│           ▼               ▼               ▼                │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│    │ PostgreSQL│    │  Redis   │    │ yfinance │           │
│    │ (Railway) │    │(Railway) │    │   API    │           │
│    └──────────┘    └──────────┘    └──────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Tech Stack

#### Frontend (Vercel)
| Technology | Purpose |
|------------|---------|
| Next.js 14 | React framework with App Router |
| TypeScript | Type safety |
| Tailwind CSS | Styling (Neo-Brutalism) |
| TanStack Query | Server state management |
| Axios | HTTP client |
| TradingView Widget | Stock charts |

#### Backend (Railway)
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Runtime |
| FastAPI | Web framework |
| SQLAlchemy | ORM (async) |
| PostgreSQL | Primary database |
| Redis | Caching layer |
| yfinance | Yahoo Finance data |
| APScheduler | Scheduled jobs |
| Alembic | Database migrations |

---

## 3. Design System: Neo-Brutalism

### 3.1 Design Principles
- **Bold borders:** 3px solid black on all interactive elements
- **Offset shadows:** 4px 4px 0px #000000
- **No rounded corners:** border-radius: 0
- **High contrast:** Dark text on bright backgrounds
- **Raw aesthetic:** Intentionally unpolished, bold look
- **Chunky typography:** Bold weights, clear hierarchy

### 3.2 Color Palette
```css
:root {
  /* Primary Colors */
  --color-primary: #FF6B6B;      /* Coral Red */
  --color-secondary: #4ECDC4;    /* Teal */
  
  /* Accent Colors */
  --color-accent-yellow: #FFE66D;
  --color-accent-mint: #95E1D3;
  --color-accent-salmon: #F38181;
  --color-accent-purple: #DDA0DD;
  
  /* Neutrals */
  --color-background: #FFF8E7;   /* Cream */
  --color-surface: #FFFFFF;
  --color-text: #2D3436;
  --color-border: #000000;
  
  /* Trend Colors */
  --color-uptrend: #00C851;
  --color-downtrend: #FF4444;
  --color-sideways: #FFBB33;
}
```

### 3.3 Typography
```css
/* Headings - English */
font-family: 'Space Grotesk', sans-serif;

/* Body - Thai */
font-family: 'IBM Plex Sans Thai', sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
--text-4xl: 2.25rem;
```

### 3.4 Component Styles

#### Brutal Card
```css
.brutal-card {
  background: white;
  border: 3px solid #000;
  box-shadow: 4px 4px 0px #000;
  padding: 1.5rem;
  transition: transform 0.1s, box-shadow 0.1s;
}

.brutal-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px #000;
}
```

#### Brutal Button
```css
.brutal-button {
  background: var(--color-primary);
  border: 3px solid #000;
  box-shadow: 4px 4px 0px #000;
  padding: 0.75rem 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
  cursor: pointer;
}

.brutal-button:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px #000;
}

.brutal-button:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0px #000;
}
```

#### Trend Badge
```css
.trend-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border: 2px solid #000;
  font-weight: 700;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.trend-badge.uptrend { background: var(--color-uptrend); color: white; }
.trend-badge.downtrend { background: var(--color-downtrend); color: white; }
.trend-badge.sideways { background: var(--color-sideways); color: black; }
```

---

## 4. Database Schema

### 4.1 Entity Relationship Diagram
```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   indices   │────<│ index_components │>────│   stocks    │
└─────────────┘     └──────────────────┘     └─────────────┘
                                                    │
                                                    │
┌─────────────┐     ┌──────────────────┐           │
│    etfs     │────<│   etf_holdings   │           │
└─────────────┘     └──────────────────┘           │
                                                    │
┌─────────────────┐                                │
│  latest_quotes  │<───────────────────────────────┤
└─────────────────┘                                │
                                                    │
┌─────────────────┐                                │
│  stock_prices   │<───────────────────────────────┤
└─────────────────┘                                │
                                                    │
┌─────────────────┐                                │
│    analysis     │<───────────────────────────────┘
└─────────────────┘
```

### 4.2 Table Definitions

#### indices
```sql
CREATE TABLE indices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,    -- 'SPX', 'NDX'
    name VARCHAR(255) NOT NULL,             -- 'S&P 500'
    name_th VARCHAR(255),                   -- 'ดัชนี S&P 500'
    description TEXT,
    description_th TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Seed data
INSERT INTO indices (symbol, name, name_th) VALUES
('SPX', 'S&P 500', 'ดัชนี S&P 500'),
('NDX', 'Nasdaq 100', 'ดัชนี Nasdaq 100');
```

#### stocks
```sql
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_th VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    description TEXT,
    description_th TEXT,
    logo_url VARCHAR(500),
    website VARCHAR(500),
    country VARCHAR(50) DEFAULT 'USA',
    exchange VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_stocks_symbol ON stocks(symbol);
CREATE INDEX idx_stocks_sector ON stocks(sector);
```

#### index_components
```sql
CREATE TABLE index_components (
    id SERIAL PRIMARY KEY,
    index_symbol VARCHAR(20) NOT NULL,
    stock_symbol VARCHAR(10) NOT NULL,
    weight DECIMAL(10, 6),
    added_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(index_symbol, stock_symbol),
    FOREIGN KEY (index_symbol) REFERENCES indices(symbol),
    FOREIGN KEY (stock_symbol) REFERENCES stocks(symbol)
);

CREATE INDEX idx_index_components_index ON index_components(index_symbol);
```

#### etfs
```sql
CREATE TABLE etfs (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_th VARCHAR(255),
    category VARCHAR(100),
    expense_ratio DECIMAL(5, 4),
    aum BIGINT,                             -- Assets Under Management
    description TEXT,
    description_th TEXT,
    provider VARCHAR(100),                  -- 'Vanguard', 'iShares', etc.
    inception_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_etfs_symbol ON etfs(symbol);
CREATE INDEX idx_etfs_category ON etfs(category);
```

#### etf_holdings
```sql
CREATE TABLE etf_holdings (
    id SERIAL PRIMARY KEY,
    etf_symbol VARCHAR(10) NOT NULL,
    holding_symbol VARCHAR(10),
    holding_name VARCHAR(255),
    weight DECIMAL(8, 4),
    shares BIGINT,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(etf_symbol, holding_symbol),
    FOREIGN KEY (etf_symbol) REFERENCES etfs(symbol)
);

CREATE INDEX idx_etf_holdings_etf ON etf_holdings(etf_symbol);
```

#### latest_quotes
```sql
CREATE TABLE latest_quotes (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    symbol_type VARCHAR(10) NOT NULL,       -- 'stock' or 'etf'
    price DECIMAL(12, 4),
    change_amount DECIMAL(12, 4),
    change_percent DECIMAL(8, 4),
    open_price DECIMAL(12, 4),
    high_price DECIMAL(12, 4),
    low_price DECIMAL(12, 4),
    volume BIGINT,
    market_cap BIGINT,
    pe_ratio DECIMAL(10, 2),
    eps DECIMAL(10, 4),
    week_52_high DECIMAL(12, 4),
    week_52_low DECIMAL(12, 4),
    avg_volume_10d BIGINT,
    dividend_yield DECIMAL(8, 4),
    sma_50 DECIMAL(12, 4),
    sma_200 DECIMAL(12, 4),
    trend VARCHAR(20),                      -- 'uptrend', 'downtrend', 'sideways'
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_latest_quotes_symbol ON latest_quotes(symbol);
CREATE INDEX idx_latest_quotes_type ON latest_quotes(symbol_type);
```

#### stock_prices (Historical)
```sql
CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(12, 4),
    high DECIMAL(12, 4),
    low DECIMAL(12, 4),
    close DECIMAL(12, 4),
    adj_close DECIMAL(12, 4),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(symbol, date)
);

CREATE INDEX idx_stock_prices_symbol_date ON stock_prices(symbol, date DESC);
```

#### etf_prices (Historical)
```sql
CREATE TABLE etf_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(12, 4),
    high DECIMAL(12, 4),
    low DECIMAL(12, 4),
    close DECIMAL(12, 4),
    adj_close DECIMAL(12, 4),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(symbol, date)
);

CREATE INDEX idx_etf_prices_symbol_date ON etf_prices(symbol, date DESC);
```

#### analysis
```sql
CREATE TABLE analysis (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    symbol_type VARCHAR(10) NOT NULL,       -- 'stock' or 'etf'
    title VARCHAR(255) NOT NULL,
    title_th VARCHAR(255),
    summary_th TEXT,
    content_th TEXT NOT NULL,
    trend_opinion VARCHAR(20),              -- Analyst's opinion
    target_price DECIMAL(12, 4),
    author VARCHAR(100),
    status VARCHAR(20) DEFAULT 'draft',     -- 'draft', 'published'
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_analysis_symbol ON analysis(symbol, symbol_type);
CREATE INDEX idx_analysis_status ON analysis(status);
```

#### sync_log
```sql
CREATE TABLE sync_log (
    id SERIAL PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,         -- 'quotes', 'prices', 'components'
    status VARCHAR(20) NOT NULL,            -- 'started', 'completed', 'failed'
    records_processed INT DEFAULT 0,
    records_updated INT DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

## 5. Backend API Specification

### 5.1 Base URL
- Production: `https://api.yourdomain.com` (Railway)
- Development: `http://localhost:8000`

### 5.2 Response Format

#### Success Response
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  }
}
```

#### Error Response
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Stock symbol 'XYZ' not found"
  }
}
```

### 5.3 Endpoints

#### Health Check
```
GET /health
Response: { "status": "healthy", "timestamp": "2025-01-10T12:00:00Z" }
```

#### Indices
```
GET /api/indices
Response: List of all indices (S&P 500, Nasdaq 100)

GET /api/indices/{symbol}
Response: Index details
Example: GET /api/indices/SPX

GET /api/indices/{symbol}/components
Query params: ?page=1&per_page=50&sector=Technology&sort=weight&order=desc
Response: List of stocks in the index with pagination
```

#### Stocks
```
GET /api/stocks
Query params: ?page=1&per_page=20&sector=Technology&search=apple
Response: Paginated list of stocks

GET /api/stocks/{symbol}
Response: Complete stock details
Example: GET /api/stocks/AAPL

GET /api/stocks/{symbol}/quote
Response: Latest price and quote data
{
  "symbol": "AAPL",
  "price": 185.50,
  "change": 2.30,
  "change_percent": 1.25,
  "volume": 52000000,
  "market_cap": 2850000000000,
  "pe_ratio": 28.5,
  "week_52_high": 199.62,
  "week_52_low": 164.08,
  "sma_50": 180.25,
  "sma_200": 175.50,
  "trend": "uptrend",
  "updated_at": "2025-01-10T12:00:00Z"
}

GET /api/stocks/{symbol}/history
Query params: ?period=1y (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
Response: Historical OHLCV data

GET /api/stocks/{symbol}/analysis
Response: Thai analysis content for the stock
```

#### ETFs
```
GET /api/etfs
Query params: ?page=1&per_page=20&category=Equity
Response: Paginated list of ETFs

GET /api/etfs/top50
Response: Top 50 ETFs list

GET /api/etfs/{symbol}
Response: Complete ETF details
Example: GET /api/etfs/SPY

GET /api/etfs/{symbol}/quote
Response: Latest price and quote data

GET /api/etfs/{symbol}/holdings
Query params: ?limit=20
Response: Top holdings of the ETF

GET /api/etfs/{symbol}/analysis
Response: Thai analysis content for the ETF
```

#### Search
```
GET /api/search
Query params: ?q=apple&type=all (all, stock, etf)
Response: {
  "stocks": [...],
  "etfs": [...]
}
```

#### Analysis (Admin)
```
GET /api/analysis
Query params: ?status=published&page=1
Response: List of analysis articles

POST /api/analysis
Body: { symbol, symbol_type, title, content_th, ... }
Response: Created analysis

PUT /api/analysis/{id}
Body: { title, content_th, status, ... }
Response: Updated analysis

DELETE /api/analysis/{id}
Response: { success: true }
```

### 5.4 Trend Calculation Logic
```python
def calculate_trend(price: float, sma_50: float, sma_200: float) -> str:
    """
    Calculate trend based on price and moving averages.
    
    Uptrend: Price > SMA50 > SMA200 (bullish)
    Downtrend: Price < SMA50 < SMA200 (bearish)
    Sideways: Everything else (consolidating)
    """
    if sma_50 is None or sma_200 is None:
        return "sideways"
    
    if price > sma_50 and sma_50 > sma_200:
        return "uptrend"
    elif price < sma_50 and sma_50 < sma_200:
        return "downtrend"
    else:
        return "sideways"
```

---

## 6. Frontend Pages & Components

### 6.1 Sitemap
```
/ (Homepage)
├── /indices
│   ├── /indices/sp500
│   └── /indices/nasdaq100
├── /stocks
│   └── /stocks/[symbol]
├── /etf
│   └── /etf/[symbol]
├── /search
└── /about
```

### 6.2 Page Specifications

#### Homepage (/)
**Purpose:** Landing page with overview and quick navigation

**Sections:**
1. **Hero**
   - Thai headline: "ศูนย์รวมข้อมูลการลงทุนหุ้นสหรัฐ"
   - Subheadline explaining site purpose
   - Search bar (prominent)
   - Background: Accent color

2. **Index Cards** (3 cards in a row)
   - S&P 500 card: Current value, change%, "500 หุ้น"
   - Nasdaq 100 card: Current value, change%, "100 หุ้น"
   - Top 50 ETF card: "50 กองทุน ETF ยอดนิยม"
   - Each card links to respective page

3. **Market Overview**
   - Today's date
   - Market status (open/closed)
   - Key metrics summary

4. **Featured Analysis**
   - Grid of 3-4 latest Thai analysis articles
   - Card shows: Title, symbol, date, summary

5. **How to Use** (Optional)
   - Brief guide for new users

**API Calls:**
- GET /api/indices (for index values)
- GET /api/analysis?status=published&limit=4

---

#### Index Page (/indices/sp500, /indices/nasdaq100)
**Purpose:** Show all components of an index

**Sections:**
1. **Header**
   - Index name (EN + TH)
   - Current value, daily change
   - Brief Thai description
   - Last updated timestamp

2. **Filter Bar**
   - Search input (filter by symbol/name)
   - Sector dropdown filter
   - Sort dropdown (Weight, Name, Change%, Trend)

3. **Stock Table**
   | Column | Description |
   |--------|-------------|
   | Symbol | Stock ticker (link to detail) |
   | Name | Company name |
   | Sector | Sector badge |
   | Price | Current price |
   | Change | Daily change % (colored) |
   | Trend | TrendBadge component |
   | Weight | Index weight % |

4. **Pagination**
   - 50 items per page
   - Page numbers + prev/next

**API Calls:**
- GET /api/indices/{symbol}
- GET /api/indices/{symbol}/components?page=1&per_page=50

---

#### Stock Detail (/stocks/[symbol])
**Purpose:** Comprehensive view of a single stock

**Sections:**
1. **Header**
   - Company logo (from Clearbit: `https://logo.clearbit.com/{domain}`)
   - Symbol (large)
   - Company name (EN + TH)
   - Sector/Industry badges
   - TrendBadge (large)

2. **Price Section**
   - Current price (large, bold)
   - Change amount and % (colored)
   - High/Low of day
   - 52-week range with progress bar

3. **TradingView Chart**
   - Embedded TradingView widget
   - Full width
   - Default: Daily, 1 year
   - Allow timeframe switching

4. **Key Metrics Grid** (2x3 or 3x2)
   - Market Cap
   - P/E Ratio
   - EPS
   - Dividend Yield
   - 52-Week High
   - 52-Week Low
   - Average Volume

5. **Thai Analysis Section**
   - Title
   - Author, Date
   - Full content in Thai
   - Analyst's trend opinion
   - Target price (if available)

6. **Company Description**
   - Thai description (if available)
   - English description (fallback)

7. **External Links**
   - Yahoo Finance button: `https://finance.yahoo.com/quote/{symbol}`
   - Company website button

8. **Related Stocks**
   - "หุ้นในกลุ่มเดียวกัน" (Same sector)
   - 4-6 stock cards

**API Calls:**
- GET /api/stocks/{symbol}
- GET /api/stocks/{symbol}/quote
- GET /api/stocks/{symbol}/analysis

---

#### ETF Listing (/etf)
**Purpose:** Show top 50 ETFs

**Sections:**
1. **Header**
   - Page title: "50 กองทุน ETF ยอดนิยม"
   - Brief description

2. **Filter Bar**
   - Search input
   - Category dropdown filter
   - Sort dropdown (AUM, Expense Ratio, Change%)

3. **ETF Grid/Table**
   | Column | Description |
   |--------|-------------|
   | Symbol | ETF ticker (link) |
   | Name | ETF name |
   | Category | Category badge |
   | Price | Current price |
   | Change | Daily change % |
   | Expense | Expense ratio |
   | AUM | Assets under management |
   | Trend | TrendBadge |

**API Calls:**
- GET /api/etfs/top50

---

#### ETF Detail (/etf/[symbol])
**Purpose:** Comprehensive view of a single ETF

**Sections:**
1. **Header** (similar to stock)
   - ETF logo/provider logo
   - Symbol, Name
   - Category badge
   - TrendBadge

2. **Price Section** (same as stock)

3. **TradingView Chart**

4. **ETF Metrics Grid**
   - AUM
   - Expense Ratio
   - Dividend Yield
   - Inception Date
   - Provider

5. **Top Holdings**
   - Table of top 10-20 holdings
   - Symbol, Name, Weight%
   - Link to stock detail if available

6. **Thai Analysis Section**

7. **External Links**
   - Yahoo Finance
   - Provider website

**API Calls:**
- GET /api/etfs/{symbol}
- GET /api/etfs/{symbol}/quote
- GET /api/etfs/{symbol}/holdings
- GET /api/etfs/{symbol}/analysis

---

#### Search Page (/search)
**Purpose:** Search results page

**Sections:**
1. **Search Bar** (pre-filled with query)

2. **Tabs**
   - All | Stocks | ETFs

3. **Results**
   - Stock results (cards or list)
   - ETF results (cards or list)
   - "No results" state

**API Calls:**
- GET /api/search?q={query}

---

### 6.3 Components Library

#### UI Components (src/components/ui/)
```
BrutalCard.tsx        - Card with border and shadow
BrutalButton.tsx      - Button with variants (primary, secondary, outline)
BrutalInput.tsx       - Text input with brutal styling
BrutalSelect.tsx      - Dropdown select
BrutalBadge.tsx       - Small badge/tag
BrutalTable.tsx       - Table with brutal styling
TrendBadge.tsx        - Uptrend/Downtrend/Sideways badge
Skeleton.tsx          - Loading skeleton with brutal style
Modal.tsx             - Modal/dialog
Pagination.tsx        - Page navigation
```

#### Layout Components (src/components/layout/)
```
Navbar.tsx            - Top navigation with search
Footer.tsx            - Site footer
Container.tsx         - Max-width container
PageHeader.tsx        - Page title section
```

#### Feature Components (src/components/features/)
```
StockCard.tsx         - Stock preview card
StockRow.tsx          - Stock table row
ETFCard.tsx           - ETF preview card
ETFRow.tsx            - ETF table row
IndexCard.tsx         - Index summary card
AnalysisCard.tsx      - Analysis preview card
SearchBar.tsx         - Global search component
PriceDisplay.tsx      - Price with change indicator
MetricsGrid.tsx       - Key metrics display
HoldingsTable.tsx     - ETF holdings table
RelatedStocks.tsx     - Related stocks section
```

#### Chart Components (src/components/charts/)
```
TradingViewChart.tsx  - TradingView widget wrapper
MiniChart.tsx         - Small sparkline chart (optional)
```

---

## 7. Backend Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Settings from env vars
│   ├── database.py                 # DB connection setup
│   │
│   ├── models/                     # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── index.py
│   │   ├── stock.py
│   │   ├── etf.py
│   │   ├── price.py
│   │   ├── analysis.py
│   │   └── sync_log.py
│   │
│   ├── schemas/                    # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── index.py
│   │   ├── stock.py
│   │   ├── etf.py
│   │   ├── analysis.py
│   │   └── common.py               # Pagination, responses
│   │
│   ├── routers/                    # API route handlers
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── indices.py
│   │   ├── stocks.py
│   │   ├── etfs.py
│   │   ├── search.py
│   │   └── analysis.py
│   │
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   ├── yahoo_finance.py        # yfinance wrapper
│   │   ├── trend_calculator.py     # Technical analysis
│   │   ├── data_sync.py            # Sync orchestration
│   │   └── cache.py                # Redis caching
│   │
│   ├── jobs/                       # Scheduled tasks
│   │   ├── __init__.py
│   │   ├── scheduler.py            # APScheduler setup
│   │   ├── sync_quotes.py          # Update latest quotes
│   │   ├── sync_prices.py          # Update historical prices
│   │   └── sync_components.py      # Update index components
│   │
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── exceptions.py           # Custom exceptions
│
├── alembic/                        # Database migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
├── data/                           # Seed data files
│   ├── sp500_components.json
│   ├── nasdaq100_components.json
│   └── top50_etfs.json
│
├── tests/
│   ├── __init__.py
│   ├── test_stocks.py
│   ├── test_etfs.py
│   └── test_indices.py
│
├── requirements.txt
├── Dockerfile
├── railway.toml
├── .env.example
└── README.md
```

---

## 8. Frontend Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Homepage
│   │   ├── globals.css             # Global styles
│   │   ├── providers.tsx           # React Query provider
│   │   │
│   │   ├── indices/
│   │   │   ├── page.tsx            # Indices overview
│   │   │   ├── sp500/
│   │   │   │   └── page.tsx
│   │   │   └── nasdaq100/
│   │   │       └── page.tsx
│   │   │
│   │   ├── stocks/
│   │   │   └── [symbol]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── etf/
│   │   │   ├── page.tsx            # ETF listing
│   │   │   └── [symbol]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── search/
│   │   │   └── page.tsx
│   │   │
│   │   └── about/
│   │       └── page.tsx
│   │
│   ├── components/
│   │   ├── ui/
│   │   │   ├── BrutalCard.tsx
│   │   │   ├── BrutalButton.tsx
│   │   │   ├── BrutalInput.tsx
│   │   │   ├── BrutalSelect.tsx
│   │   │   ├── BrutalBadge.tsx
│   │   │   ├── BrutalTable.tsx
│   │   │   ├── TrendBadge.tsx
│   │   │   ├── Skeleton.tsx
│   │   │   └── Pagination.tsx
│   │   │
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Container.tsx
│   │   │   └── PageHeader.tsx
│   │   │
│   │   ├── features/
│   │   │   ├── StockCard.tsx
│   │   │   ├── StockRow.tsx
│   │   │   ├── ETFCard.tsx
│   │   │   ├── ETFRow.tsx
│   │   │   ├── IndexCard.tsx
│   │   │   ├── AnalysisCard.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── PriceDisplay.tsx
│   │   │   ├── MetricsGrid.tsx
│   │   │   ├── HoldingsTable.tsx
│   │   │   └── RelatedStocks.tsx
│   │   │
│   │   └── charts/
│   │       └── TradingViewChart.tsx
│   │
│   ├── lib/
│   │   ├── api.ts                  # Axios client setup
│   │   ├── queryClient.ts          # React Query config
│   │   └── utils.ts                # Utility functions
│   │
│   ├── hooks/
│   │   ├── useStocks.ts
│   │   ├── useETFs.ts
│   │   ├── useIndices.ts
│   │   ├── useSearch.ts
│   │   └── useAnalysis.ts
│   │
│   └── types/
│       └── index.ts                # TypeScript types
│
├── public/
│   ├── favicon.ico
│   └── images/
│
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── .env.local
```

---

## 9. Scheduled Jobs

### 9.1 Job Schedule

| Job | Frequency | Time (UTC) | Description |
|-----|-----------|------------|-------------|
| sync_quotes | Every 15 min | During market hours | Update latest_quotes table |
| sync_daily_prices | Daily | 06:00 | Sync previous day's OHLCV |
| sync_components | Weekly | Sunday 00:00 | Update index components |
| sync_etf_holdings | Weekly | Sunday 01:00 | Update ETF holdings |
| cleanup_old_logs | Monthly | 1st, 00:00 | Delete old sync logs |

### 9.2 Market Hours Detection
```python
import pytz
from datetime import datetime, time

def is_market_open() -> bool:
    """Check if US stock market is currently open."""
    et = pytz.timezone('America/New_York')
    now = datetime.now(et)
    
    # Weekend check
    if now.weekday() >= 5:
        return False
    
    # Market hours: 9:30 AM - 4:00 PM ET
    market_open = time(9, 30)
    market_close = time(16, 0)
    
    return market_open <= now.time() <= market_close
```

---

## 10. Caching Strategy

### 10.1 Redis Cache Keys
```
quote:{symbol}              # TTL: 5 minutes
stock:{symbol}              # TTL: 1 hour
etf:{symbol}                # TTL: 1 hour
index_components:{symbol}   # TTL: 24 hours
etf_holdings:{symbol}       # TTL: 24 hours
search:{query}              # TTL: 15 minutes
```

### 10.2 Cache Invalidation
- Quotes: Auto-expire after 5 minutes
- After sync jobs complete, invalidate related keys
- Manual invalidation endpoint for admin

---

## 11. Environment Variables

### 11.1 Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://default:password@host:6379

# App Config
ENVIRONMENT=production
DEBUG=false
API_PREFIX=/api

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Yahoo Finance (optional rate limiting)
YFINANCE_RATE_LIMIT=5

# Admin
ADMIN_API_KEY=your-secret-key
```

### 11.2 Frontend (.env.local)
```bash
# API
NEXT_PUBLIC_API_URL=https://api.yourdomain.com

# Site
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
NEXT_PUBLIC_SITE_NAME=Thai U.S. Investment Portal

# Analytics (optional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

---

## 12. Deployment

### 12.1 Backend (Railway)

**railway.toml:**
```toml
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations and start server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Railway Services:**
1. Web service (FastAPI app)
2. PostgreSQL database
3. Redis cache

### 12.2 Frontend (Vercel)

**vercel.json:**
```json
{
  "framework": "nextjs",
  "regions": ["sin1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  }
}
```

---

## 13. Development Workflow

### 13.1 Phase 1: Backend Foundation (Week 1)
- [ ] Set up FastAPI project structure
- [ ] Configure database models and migrations
- [ ] Implement Yahoo Finance service
- [ ] Create stock and ETF endpoints
- [ ] Set up Redis caching
- [ ] Deploy to Railway

### 13.2 Phase 2: Frontend Foundation (Week 2)
- [ ] Set up Next.js project
- [ ] Create Neo-Brutalism design system
- [ ] Build layout components (Navbar, Footer)
- [ ] Set up API client and React Query
- [ ] Deploy to Vercel

### 13.3 Phase 3: Core Features (Week 3)
- [ ] Build Homepage
- [ ] Build Index pages (S&P 500, Nasdaq 100)
- [ ] Build Stock detail page
- [ ] Integrate TradingView widget

### 13.4 Phase 4: ETF & Search (Week 4)
- [ ] Build ETF listing page
- [ ] Build ETF detail page
- [ ] Implement search functionality
- [ ] Add loading and error states

### 13.5 Phase 5: Content & Polish (Week 5)
- [ ] Set up Thai analysis content management
- [ ] Add seed data (components, ETFs)
- [ ] Implement scheduled jobs
- [ ] SEO optimization
- [ ] Mobile responsiveness

### 13.6 Phase 6: Testing & Launch (Week 6)
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security review
- [ ] Production deployment
- [ ] Monitoring setup

---

## 14. Success Metrics

- Page load time < 3 seconds
- API response time < 500ms
- Data freshness: Quotes updated every 15 minutes
- Mobile responsive on all pages
- Thai content available for top 50 stocks

---

## 15. Future Enhancements (v2.0)

- User accounts and watchlists
- Price alerts
- Portfolio tracker
- More Thai educational content
- Comparison tool
- Mobile app (React Native)

---

## Appendix A: Top 50 ETF List

```json
[
  {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "category": "Large Cap Blend"},
  {"symbol": "QQQ", "name": "Invesco QQQ Trust", "category": "Large Cap Growth"},
  {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF", "category": "Total Market"},
  {"symbol": "IVV", "name": "iShares Core S&P 500 ETF", "category": "Large Cap Blend"},
  {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "category": "Large Cap Blend"},
  {"symbol": "VEA", "name": "Vanguard FTSE Developed Markets ETF", "category": "International"},
  {"symbol": "IEFA", "name": "iShares Core MSCI EAFE ETF", "category": "International"},
  {"symbol": "AGG", "name": "iShares Core U.S. Aggregate Bond ETF", "category": "Bond"},
  {"symbol": "BND", "name": "Vanguard Total Bond Market ETF", "category": "Bond"},
  {"symbol": "VWO", "name": "Vanguard FTSE Emerging Markets ETF", "category": "Emerging Markets"},
  {"symbol": "VTV", "name": "Vanguard Value ETF", "category": "Large Cap Value"},
  {"symbol": "IJR", "name": "iShares Core S&P Small-Cap ETF", "category": "Small Cap"},
  {"symbol": "VUG", "name": "Vanguard Growth ETF", "category": "Large Cap Growth"},
  {"symbol": "IWM", "name": "iShares Russell 2000 ETF", "category": "Small Cap"},
  {"symbol": "VIG", "name": "Vanguard Dividend Appreciation ETF", "category": "Dividend"},
  {"symbol": "EFA", "name": "iShares MSCI EAFE ETF", "category": "International"},
  {"symbol": "GLD", "name": "SPDR Gold Shares", "category": "Commodity"},
  {"symbol": "VNQ", "name": "Vanguard Real Estate ETF", "category": "Real Estate"},
  {"symbol": "LQD", "name": "iShares iBoxx Investment Grade Corporate Bond ETF", "category": "Bond"},
  {"symbol": "VGT", "name": "Vanguard Information Technology ETF", "category": "Technology"},
  {"symbol": "SCHD", "name": "Schwab U.S. Dividend Equity ETF", "category": "Dividend"},
  {"symbol": "XLK", "name": "Technology Select Sector SPDR Fund", "category": "Technology"},
  {"symbol": "XLF", "name": "Financial Select Sector SPDR Fund", "category": "Financial"},
  {"symbol": "XLV", "name": "Health Care Select Sector SPDR Fund", "category": "Healthcare"},
  {"symbol": "DIA", "name": "SPDR Dow Jones Industrial Average ETF", "category": "Large Cap"},
  {"symbol": "ARKK", "name": "ARK Innovation ETF", "category": "Thematic"},
  {"symbol": "XLE", "name": "Energy Select Sector SPDR Fund", "category": "Energy"},
  {"symbol": "TLT", "name": "iShares 20+ Year Treasury Bond ETF", "category": "Bond"},
  {"symbol": "HYG", "name": "iShares iBoxx High Yield Corporate Bond ETF", "category": "Bond"},
  {"symbol": "EEM", "name": "iShares MSCI Emerging Markets ETF", "category": "Emerging Markets"},
  {"symbol": "SHY", "name": "iShares 1-3 Year Treasury Bond ETF", "category": "Bond"},
  {"symbol": "IWF", "name": "iShares Russell 1000 Growth ETF", "category": "Large Cap Growth"},
  {"symbol": "IWD", "name": "iShares Russell 1000 Value ETF", "category": "Large Cap Value"},
  {"symbol": "VYM", "name": "Vanguard High Dividend Yield ETF", "category": "Dividend"},
  {"symbol": "XLI", "name": "Industrial Select Sector SPDR Fund", "category": "Industrial"},
  {"symbol": "XLY", "name": "Consumer Discretionary Select Sector SPDR Fund", "category": "Consumer"},
  {"symbol": "XLP", "name": "Consumer Staples Select Sector SPDR Fund", "category": "Consumer"},
  {"symbol": "IEMG", "name": "iShares Core MSCI Emerging Markets ETF", "category": "Emerging Markets"},
  {"symbol": "IEF", "name": "iShares 7-10 Year Treasury Bond ETF", "category": "Bond"},
  {"symbol": "MBB", "name": "iShares MBS ETF", "category": "Bond"},
  {"symbol": "VCIT", "name": "Vanguard Intermediate-Term Corporate Bond ETF", "category": "Bond"},
  {"symbol": "EMB", "name": "iShares J.P. Morgan USD Emerging Markets Bond ETF", "category": "Bond"},
  {"symbol": "TIP", "name": "iShares TIPS Bond ETF", "category": "Bond"},
  {"symbol": "SLV", "name": "iShares Silver Trust", "category": "Commodity"},
  {"symbol": "XLU", "name": "Utilities Select Sector SPDR Fund", "category": "Utilities"},
  {"symbol": "XLRE", "name": "Real Estate Select Sector SPDR Fund", "category": "Real Estate"},
  {"symbol": "XLB", "name": "Materials Select Sector SPDR Fund", "category": "Materials"},
  {"symbol": "XLC", "name": "Communication Services Select Sector SPDR Fund", "category": "Communication"},
  {"symbol": "JEPI", "name": "JPMorgan Equity Premium Income ETF", "category": "Income"},
  {"symbol": "JEPQ", "name": "JPMorgan Nasdaq Equity Premium Income ETF", "category": "Income"}
]
```

---

*End of PRD Document*
