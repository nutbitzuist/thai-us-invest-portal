'use client';

import Link from 'next/link';
import { useState } from 'react';
import SearchBar from '@/components/features/SearchBar';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="bg-white border-b-3 border-black sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-primary border-3 border-black flex items-center justify-center">
              <span className="text-black font-bold text-lg">US</span>
            </div>
            <span className="font-heading font-bold text-lg hidden sm:block">
              Thai US Invest
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            <Link href="/indices/sp500" className="font-thai font-medium hover:text-primary transition-colors">
              S&P 500
            </Link>
            <Link href="/indices/nasdaq100" className="font-thai font-medium hover:text-primary transition-colors">
              Nasdaq 100
            </Link>
            <Link href="/etf" className="font-thai font-medium hover:text-primary transition-colors">
              ETF
            </Link>
          </div>

          {/* Search */}
          <div className="hidden md:block w-64">
            <SearchBar />
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 border-3 border-black bg-white"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t-3 border-black">
            <div className="mb-4">
              <SearchBar />
            </div>
            <div className="flex flex-col gap-2">
              <Link 
                href="/indices/sp500" 
                className="py-2 px-4 bg-accent-yellow border-3 border-black font-thai font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                S&P 500 (500 หุ้น)
              </Link>
              <Link 
                href="/indices/nasdaq100" 
                className="py-2 px-4 bg-secondary border-3 border-black font-thai font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                Nasdaq 100 (100 หุ้น)
              </Link>
              <Link 
                href="/etf" 
                className="py-2 px-4 bg-primary border-3 border-black font-thai font-medium text-black"
                onClick={() => setMobileMenuOpen(false)}
              >
                ETF ยอดนิยม
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
