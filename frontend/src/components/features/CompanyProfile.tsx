import { Stock, LatestQuote } from '@/types/stock';
import BrutalCard from '@/components/ui/BrutalCard';

interface Props {
  stock: Stock;
  quote?: LatestQuote;
}

export default function CompanyProfile({ stock, quote }: Props) {
  const fmtMoney = (val?: number) => val ? `$${(val/1e9).toFixed(2)}B` : '-';
  
  return (
    <div className="flex flex-col gap-4 sticky top-20">
       {/* Quick Facts */}
       <BrutalCard color="white" className="p-5 border-3 border-black shadow-brutal">
          <h3 className="font-heading font-bold text-xl mb-4 border-b-3 border-black pb-2 flex items-center gap-2">
            🏢 Quick Facts
          </h3>
          
          <div className="space-y-4 font-thai text-sm text-black">
             <div>
                <span className="font-bold text-gray-500 block uppercase text-xs">Sector / Industry</span>
                <span className="font-medium">{stock.sector || '-'} / {stock.industry || '-'}</span>
             </div>
             
             <div className="grid grid-cols-2 gap-2">
                 <div>
                    <span className="font-bold text-gray-500 block uppercase text-xs">CEO</span>
                    <span className="font-medium">{stock.ceo || '-'}</span>
                 </div>
                 <div>
                    <span className="font-bold text-gray-500 block uppercase text-xs">Employees</span>
                    <span className="font-medium">{stock.employees?.toLocaleString() || '-'}</span>
                 </div>
             </div>

             <div>
                <span className="font-bold text-gray-500 block uppercase text-xs">Headquarters</span>
                <span className="font-medium">{stock.headquarters || stock.country || '-'}</span>
             </div>

             {stock.founded_year && (
                 <div>
                    <span className="font-bold text-gray-500 block uppercase text-xs">Founded</span>
                    <span className="font-medium">{stock.founded_year}</span>
                 </div>
             )}
             
             {stock.website && (
                 <a 
                   href={stock.website} 
                   target="_blank" 
                   rel="noopener" 
                   className="block mt-6 bg-black text-white text-center py-3 font-bold hover:bg-gray-800 transition border-2 border-transparent hover:border-black"
                 >
                    🌐 Visit Website
                 </a>
             )}
          </div>
       </BrutalCard>
       
       {/* Valuation Metrics */}
       <BrutalCard color="mint" className="p-5 border-3 border-black shadow-brutal">
          <h3 className="font-heading font-bold text-xl mb-4 border-b-3 border-black pb-2">📊 Valuation</h3>
          <div className="space-y-3 text-black">
             <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium">Market Cap</span>
                <span className="font-bold font-mono text-lg">{fmtMoney(quote?.market_cap)}</span>
             </div>
             <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium">P/E Ratio</span>
                <span className="font-bold font-mono text-lg">{quote?.pe_ratio?.toFixed(2) || '-'}</span>
             </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium">EPS</span>
                <span className="font-bold font-mono text-lg">{quote?.eps?.toFixed(2) || '-'}</span>
             </div>
             <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium">52W High</span>
                <span className="font-bold font-mono text-lg">${quote?.week_52_high || '-'}</span>
             </div>
             <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium">Div Yield</span>
                <span className="font-bold font-mono text-lg">
                    {quote?.dividend_yield ? `${(quote.dividend_yield * 100).toFixed(2)}%` : '-'}
                </span>
             </div>
          </div>
       </BrutalCard>
    </div>
  );
}
