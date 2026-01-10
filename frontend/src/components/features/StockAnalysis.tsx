import BrutalCard from '@/components/ui/BrutalCard';
import { StockAnalysis as IStockAnalysis } from '@/types/stock';
import { useState } from 'react';

interface Props {
  symbol: string;
  analysis?: IStockAnalysis | null;
  description?: string;
}

export default function StockAnalysis({ symbol, analysis, description }: Props) {
  const [activeTab, setActiveTab] = useState<'overview' | 'financials' | 'analysis'>('analysis');

  return (
    <div className="flex flex-col gap-6">
        {/* Tabs */}
        <div className="flex flex-wrap gap-2 border-b-3 border-black pb-1">
            <button 
                onClick={() => setActiveTab('analysis')}
                className={`px-6 py-2 font-bold font-thai text-lg border-t-3 border-x-3 border-black transition-all ${activeTab === 'analysis' ? 'bg-primary text-black -mb-4 pb-4 z-10' : 'bg-white text-gray-500 hover:bg-gray-100'}`}
            >
                บทวิเคราะห์ (Analysis)
            </button>
            <button 
                onClick={() => setActiveTab('overview')}
                className={`px-6 py-2 font-bold font-thai text-lg border-t-3 border-x-3 border-black transition-all ${activeTab === 'overview' ? 'bg-accent-yellow text-black -mb-4 pb-4 z-10' : 'bg-white text-gray-500 hover:bg-gray-100'}`}
            >
                เกี่ยวกับบริษัท (Overview)
            </button>
             <button 
                onClick={() => setActiveTab('financials')}
                className={`px-6 py-2 font-bold font-thai text-lg border-t-3 border-x-3 border-black transition-all ${activeTab === 'financials' ? 'bg-secondary text-black -mb-4 pb-4 z-10' : 'bg-white text-gray-500 hover:bg-gray-100'}`}
            >
                งบการเงิน (Financials)
            </button>
        </div>

        {/* Content */}
        <BrutalCard className="p-6 md:p-8 min-h-[400px] border-t-0 rounded-tl-none">
            {activeTab === 'analysis' && (
                <div className="prose max-w-none font-thai text-black text-lg">
                    {analysis ? (
                        <>
                            <h2 className="text-3xl font-bold mb-6 font-heading">{analysis.title_th || analysis.title}</h2>
                            <div className="whitespace-pre-wrap leading-relaxed space-y-4">
                                {analysis.content_th}
                            </div>
                            <div className="mt-8 pt-4 border-t-2 border-gray-200 text-sm text-gray-500 flex justify-between">
                                <span>Analysis by {analysis.author || 'AI Analyst'}</span>
                                <span>Published {new Date(analysis.published_at || '').toLocaleDateString('th-TH')}</span>
                            </div>
                        </>
                    ) : (
                        <div className="text-center py-12">
                            <span className="text-6xl mb-4 block">🤖</span>
                            <h3 className="text-2xl font-bold mb-2">ยังไม่มีบทวิเคราะห์เชิงลึก</h3>
                            <p className="text-gray-600 mb-6 max-w-lg mx-auto">
                                เรากำลังสร้างบทวิเคราะห์เชิงลึกสำหรับ {symbol} ครอบคลุมโมเดลธุรกิจ, ผลประกอบการ, และความเสี่ยง ตามโครงสร้างที่คุณต้องการ
                            </p>
                            <div className="p-6 bg-gray-50 border-2 border-dashed border-gray-300 inline-block text-left rounded-lg">
                                <p className="font-bold mb-3 text-primary text-center">หัวข้อที่จะวิเคราะห์</p>
                                <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2 text-sm text-gray-700 list-disc pl-5">
                                    <li>บริษัทนี้คืออะไร? ทำอะไร?</li>
                                    <li>โมเดลธุรกิจและรายได้</li>
                                    <li>ผลประกอบการย้อนหลัง</li>
                                    <li>การเติบโตและโอกาส</li>
                                    <li>ความเสี่ยงศก./ธุรกิจ</li>
                                    <li>การประเมินมูลค่า (Valuation)</li>
                                    <li>ผู้บริหารและธรรมาภิบาล</li>
                                    <li>สรุปมุมมองการลงทุน</li>
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {activeTab === 'overview' && (
                <div className="font-thai text-black text-lg leading-relaxed whitespace-pre-line">
                    <h3 className="font-bold text-2xl mb-4 font-heading">Business Description</h3>
                    <p>{description || "No description available from data provider."}</p>
                </div>
            )}

            {activeTab === 'financials' && (
                <div className="text-center py-16">
                    <span className="text-5xl mb-4 block">📊</span>
                    <h3 className="text-2xl font-bold font-thai mb-2">Financial Charts Coming Soon</h3>
                    <p className="text-gray-500">Revenue, Profit, and Margin charts will appear here.</p>
                </div>
            )}
        </BrutalCard>
    </div>
  );
}
