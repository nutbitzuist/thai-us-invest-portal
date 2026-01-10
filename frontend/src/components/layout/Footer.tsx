import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-text-primary text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-primary border-3 border-white flex items-center justify-center">
                <span className="text-white font-bold">US</span>
              </div>
              <span className="font-heading font-bold text-xl">Thai US Invest</span>
            </div>
            <p className="font-thai text-gray-300 mb-4">
              ศูนย์รวมข้อมูลหุ้นและ ETF สหรัฐอเมริกา<br />
              สำหรับนักลงทุนไทย พร้อมบทวิเคราะห์ภาษาไทย
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-heading font-bold text-lg mb-4">ลิงก์ด่วน</h4>
            <ul className="space-y-2 font-thai">
              <li>
                <Link href="/indices/sp500" className="text-gray-300 hover:text-primary transition-colors">
                  ดัชนี S&P 500
                </Link>
              </li>
              <li>
                <Link href="/indices/nasdaq100" className="text-gray-300 hover:text-primary transition-colors">
                  ดัชนี Nasdaq 100
                </Link>
              </li>
              <li>
                <Link href="/etf" className="text-gray-300 hover:text-primary transition-colors">
                  50 ETF ยอดนิยม
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-heading font-bold text-lg mb-4">แหล่งข้อมูล</h4>
            <ul className="space-y-2 font-thai">
              <li>
                <a 
                  href="https://finance.yahoo.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-primary transition-colors"
                >
                  Yahoo Finance ↗
                </a>
              </li>
              <li>
                <a 
                  href="https://www.tradingview.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-primary transition-colors"
                >
                  TradingView ↗
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center font-thai text-gray-400">
          <p>© 2025 Thai U.S. Investment Portal. ข้อมูลจาก Yahoo Finance</p>
          <p className="text-sm mt-2">
            ข้อมูลในเว็บไซต์นี้มีไว้เพื่อการศึกษาเท่านั้น ไม่ใช่คำแนะนำการลงทุน
          </p>
        </div>
      </div>
    </footer>
  );
}
