import Link from 'next/link';
import BrutalCard from '@/components/ui/BrutalCard';
import BrutalButton from '@/components/ui/BrutalButton';
import SearchBar from '@/components/features/SearchBar';

export default function HomePage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-accent-yellow border-b-3 border-black">
        <div className="max-w-7xl mx-auto px-4 py-16 md:py-24">
          <h1 className="font-heading text-4xl md:text-6xl font-bold text-center mb-6">
            ศูนย์รวมข้อมูลการลงทุน<br />
            <span className="text-primary">หุ้นสหรัฐ</span>
          </h1>
          <p className="font-thai text-xl text-center max-w-2xl mx-auto mb-8">
            ข้อมูลหุ้น S&P 500, Nasdaq 100 และ ETF ยอดนิยม 
            พร้อมบทวิเคราะห์ภาษาไทยและกราฟจาก TradingView
          </p>
          <div className="max-w-xl mx-auto">
            <SearchBar />
          </div>
        </div>
      </section>

      {/* Index Cards */}
      <section className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* S&P 500 Card */}
          <BrutalCard href="/indices/sp500" color="primary">
            <div className="text-white">
              <h2 className="font-heading text-3xl font-bold">S&P 500</h2>
              <p className="font-thai text-lg mt-2 opacity-90">ดัชนี S&P 500</p>
              <p className="font-thai mt-4 text-4xl font-bold">500 หุ้น</p>
              <p className="font-thai text-sm mt-2 opacity-80">
                หุ้น 500 บริษัทขนาดใหญ่ที่สุดของสหรัฐ
              </p>
              <div className="mt-6">
                <span className="inline-block bg-white text-primary font-bold px-4 py-2 border-2 border-black">
                  ดูทั้งหมด →
                </span>
              </div>
            </div>
          </BrutalCard>

          {/* Nasdaq 100 Card */}
          <BrutalCard href="/indices/nasdaq100" color="secondary">
            <div>
              <h2 className="font-heading text-3xl font-bold">Nasdaq 100</h2>
              <p className="font-thai text-lg mt-2">ดัชนี Nasdaq 100</p>
              <p className="font-thai mt-4 text-4xl font-bold">100 หุ้น</p>
              <p className="font-thai text-sm mt-2 opacity-80">
                หุ้นเทคโนโลยีชั้นนำที่สุดของโลก
              </p>
              <div className="mt-6">
                <span className="inline-block bg-black text-white font-bold px-4 py-2 border-2 border-black">
                  ดูทั้งหมด →
                </span>
              </div>
            </div>
          </BrutalCard>

          {/* ETF Card */}
          <BrutalCard href="/etf" color="yellow">
            <div>
              <h2 className="font-heading text-3xl font-bold">Top 50 ETF</h2>
              <p className="font-thai text-lg mt-2">กองทุน ETF ยอดนิยม</p>
              <p className="font-thai mt-4 text-4xl font-bold">50 กองทุน</p>
              <p className="font-thai text-sm mt-2 opacity-80">
                ETF ที่นักลงทุนทั่วโลกนิยมมากที่สุด
              </p>
              <div className="mt-6">
                <span className="inline-block bg-black text-white font-bold px-4 py-2 border-2 border-black">
                  ดูทั้งหมด →
                </span>
              </div>
            </div>
          </BrutalCard>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white border-y-3 border-black py-12">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="font-heading text-3xl font-bold text-center mb-8">
            ฟีเจอร์หลัก
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary border-3 border-black mx-auto flex items-center justify-center text-3xl">
                📊
              </div>
              <h3 className="font-heading text-xl font-bold mt-4">กราฟ TradingView</h3>
              <p className="font-thai mt-2 text-gray-600">
                กราฟระดับมืออาชีพจาก TradingView<br />
                พร้อมเครื่องมือวิเคราะห์ทางเทคนิค
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-secondary border-3 border-black mx-auto flex items-center justify-center text-3xl">
                📈
              </div>
              <h3 className="font-heading text-xl font-bold mt-4">แสดงเทรนด์</h3>
              <p className="font-thai mt-2 text-gray-600">
                ระบบวิเคราะห์เทรนด์อัตโนมัติ<br />
                ขาขึ้น / ขาลง / ไซด์เวย์
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-accent-yellow border-3 border-black mx-auto flex items-center justify-center text-3xl">
                🇹🇭
              </div>
              <h3 className="font-heading text-xl font-bold mt-4">บทวิเคราะห์ภาษาไทย</h3>
              <p className="font-thai mt-2 text-gray-600">
                อ่านบทวิเคราะห์หุ้นสหรัฐ<br />
                เข้าใจง่ายเป็นภาษาไทย
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 py-12 text-center">
        <h2 className="font-heading text-2xl md:text-3xl font-bold mb-6">
          เริ่มต้นสำรวจหุ้นสหรัฐวันนี้
        </h2>
        <div className="flex flex-wrap justify-center gap-4">
          <BrutalButton href="/indices/sp500" variant="primary" size="lg">
            ดูหุ้น S&P 500
          </BrutalButton>
          <BrutalButton href="/etf" variant="yellow" size="lg">
            ดู ETF ยอดนิยม
          </BrutalButton>
        </div>
      </section>
    </div>
  );
}
