"""Initial migration - create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create indices table
    op.create_table(
        'indices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(20), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('name_th', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('description_th', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Create stocks table
    op.create_table(
        'stocks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(10), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('name_th', sa.String(255)),
        sa.Column('sector', sa.String(100)),
        sa.Column('industry', sa.String(100)),
        sa.Column('description', sa.Text()),
        sa.Column('description_th', sa.Text()),
        sa.Column('logo_url', sa.String(500)),
        sa.Column('website', sa.String(500)),
        sa.Column('country', sa.String(50), server_default='USA'),
        sa.Column('exchange', sa.String(20)),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('idx_stocks_symbol', 'stocks', ['symbol'])
    op.create_index('idx_stocks_sector', 'stocks', ['sector'])
    
    # Create index_components table
    op.create_table(
        'index_components',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('index_symbol', sa.String(20), sa.ForeignKey('indices.symbol', ondelete='CASCADE'), nullable=False),
        sa.Column('stock_symbol', sa.String(10), sa.ForeignKey('stocks.symbol', ondelete='CASCADE'), nullable=False),
        sa.Column('weight', sa.Numeric(10, 6)),
        sa.Column('added_date', sa.Date()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('index_symbol', 'stock_symbol', name='uq_index_stock'),
    )
    op.create_index('idx_index_components_index', 'index_components', ['index_symbol'])
    
    # Create etfs table
    op.create_table(
        'etfs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(10), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('name_th', sa.String(255)),
        sa.Column('category', sa.String(100)),
        sa.Column('expense_ratio', sa.Numeric(5, 4)),
        sa.Column('aum', sa.BigInteger()),
        sa.Column('description', sa.Text()),
        sa.Column('description_th', sa.Text()),
        sa.Column('provider', sa.String(100)),
        sa.Column('inception_date', sa.Date()),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('idx_etfs_symbol', 'etfs', ['symbol'])
    op.create_index('idx_etfs_category', 'etfs', ['category'])
    
    # Create etf_holdings table
    op.create_table(
        'etf_holdings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('etf_symbol', sa.String(10), sa.ForeignKey('etfs.symbol', ondelete='CASCADE'), nullable=False),
        sa.Column('holding_symbol', sa.String(10)),
        sa.Column('holding_name', sa.String(255)),
        sa.Column('weight', sa.Numeric(8, 4)),
        sa.Column('shares', sa.BigInteger()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint('etf_symbol', 'holding_symbol', name='uq_etf_holding'),
    )
    op.create_index('idx_etf_holdings_etf', 'etf_holdings', ['etf_symbol'])
    
    # Create latest_quotes table
    op.create_table(
        'latest_quotes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(10), unique=True, nullable=False),
        sa.Column('symbol_type', sa.String(10), nullable=False),
        sa.Column('price', sa.Numeric(12, 4)),
        sa.Column('change_amount', sa.Numeric(12, 4)),
        sa.Column('change_percent', sa.Numeric(8, 4)),
        sa.Column('open_price', sa.Numeric(12, 4)),
        sa.Column('high_price', sa.Numeric(12, 4)),
        sa.Column('low_price', sa.Numeric(12, 4)),
        sa.Column('volume', sa.BigInteger()),
        sa.Column('market_cap', sa.BigInteger()),
        sa.Column('pe_ratio', sa.Numeric(10, 2)),
        sa.Column('eps', sa.Numeric(10, 4)),
        sa.Column('week_52_high', sa.Numeric(12, 4)),
        sa.Column('week_52_low', sa.Numeric(12, 4)),
        sa.Column('avg_volume_10d', sa.BigInteger()),
        sa.Column('dividend_yield', sa.Numeric(8, 4)),
        sa.Column('sma_50', sa.Numeric(12, 4)),
        sa.Column('sma_200', sa.Numeric(12, 4)),
        sa.Column('trend', sa.String(20)),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('idx_latest_quotes_symbol', 'latest_quotes', ['symbol'])
    op.create_index('idx_latest_quotes_type', 'latest_quotes', ['symbol_type'])
    
    # Create stock_prices table
    op.create_table(
        'stock_prices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Numeric(12, 4)),
        sa.Column('high', sa.Numeric(12, 4)),
        sa.Column('low', sa.Numeric(12, 4)),
        sa.Column('close', sa.Numeric(12, 4)),
        sa.Column('adj_close', sa.Numeric(12, 4)),
        sa.Column('volume', sa.BigInteger()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('symbol', 'date', name='uq_stock_price_date'),
    )
    op.create_index('idx_stock_prices_symbol_date', 'stock_prices', ['symbol', 'date'])
    
    # Create etf_prices table
    op.create_table(
        'etf_prices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Numeric(12, 4)),
        sa.Column('high', sa.Numeric(12, 4)),
        sa.Column('low', sa.Numeric(12, 4)),
        sa.Column('close', sa.Numeric(12, 4)),
        sa.Column('adj_close', sa.Numeric(12, 4)),
        sa.Column('volume', sa.BigInteger()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('symbol', 'date', name='uq_etf_price_date'),
    )
    op.create_index('idx_etf_prices_symbol_date', 'etf_prices', ['symbol', 'date'])
    
    # Create analysis table
    op.create_table(
        'analysis',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('symbol_type', sa.String(10), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('title_th', sa.String(255)),
        sa.Column('summary_th', sa.Text()),
        sa.Column('content_th', sa.Text(), nullable=False),
        sa.Column('trend_opinion', sa.String(20)),
        sa.Column('target_price', sa.Numeric(12, 4)),
        sa.Column('author', sa.String(100)),
        sa.Column('status', sa.String(20), server_default='draft'),
        sa.Column('published_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('idx_analysis_symbol', 'analysis', ['symbol', 'symbol_type'])
    op.create_index('idx_analysis_status', 'analysis', ['status'])
    
    # Create sync_log table
    op.create_table(
        'sync_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sync_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('records_processed', sa.Integer(), server_default='0'),
        sa.Column('records_updated', sa.Integer(), server_default='0'),
        sa.Column('error_message', sa.Text()),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
    )
    
    # Seed initial data for indices
    op.execute("""
        INSERT INTO indices (symbol, name, name_th, description_th) VALUES
        ('SPX', 'S&P 500', 'ดัชนี S&P 500', 'ดัชนีหุ้น 500 บริษัทขนาดใหญ่ที่สุดของสหรัฐอเมริกา'),
        ('NDX', 'Nasdaq 100', 'ดัชนี Nasdaq 100', 'ดัชนีหุ้น 100 บริษัทเทคโนโลยีชั้นนำที่จดทะเบียนใน Nasdaq')
    """)


def downgrade() -> None:
    op.drop_table('sync_log')
    op.drop_table('analysis')
    op.drop_table('etf_prices')
    op.drop_table('stock_prices')
    op.drop_table('latest_quotes')
    op.drop_table('etf_holdings')
    op.drop_table('etfs')
    op.drop_table('index_components')
    op.drop_table('stocks')
    op.drop_table('indices')
