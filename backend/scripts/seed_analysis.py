
import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to sys.path so we can import app modules
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(backend_dir)

from sqlalchemy import select
from app.database import get_session_maker
from app.models.analysis import Analysis
from scripts.data.seed_content_aapl import aapl_analysis
from scripts.data.seed_content_msft import msft_analysis
from scripts.data.seed_content_nvda import nvda_analysis
from scripts.data.seed_content_spy import spy_analysis
from scripts.data.seed_content_googl import googl_analysis
from scripts.data.seed_content_amzn import amzn_analysis
from scripts.data.seed_content_meta import meta_analysis
from scripts.data.seed_content_tsla import tsla_analysis
from scripts.data.seed_content_amd import amd_analysis
from scripts.data.seed_content_nflx import nflx_analysis
from scripts.data.seed_content_qqq import qqq_analysis

async def seed_data():
    print("Starting analysis data seed...")
    
    session_maker = get_session_maker()
    
    data_map = [
        {
            "symbol": "AAPL",
            "type": "stock",
            "title": "Apple Inc. Deep Dive Analysis",
            "title_th": "เจาะลึก Apple Inc. (AAPL): อาณาจักรผลไม้ที่ครองโลก",
            "content": aapl_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "MSFT",
            "type": "stock",
            "title": "Microsoft Deep Dive Analysis",
            "title_th": "เจาะลึก Microsoft (MSFT): ยักษ์ใหญ่ที่ตื่นจากการหลับใหลสู่ผู้นำ AI",
            "content": msft_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "NVDA",
            "type": "stock",
            "title": "NVIDIA Deep Dive Analysis",
            "title_th": "เจาะลึก NVIDIA (NVDA): ผู้สร้างสมองของ AI",
            "content": nvda_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "SPY",
            "type": "etf",
            "title": "SPY ETF Analysis",
            "title_th": "เจาะลึก SPY ETF: กองทุนดัชนี S&P 500 ที่ดีที่สุด?",
            "content": spy_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "GOOGL",
            "type": "stock",
            "title": "Alphabet Inc. Deep Dive Analysis",
            "title_th": "เจาะลึก Alphabet (GOOGL): เจ้าแห่งการค้นหาและข้อมูลของโลก",
            "content": googl_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "AMZN",
            "type": "stock",
            "title": "Amazon.com Deep Dive Analysis",
            "title_th": "เจาะลึก Amazon (AMZN): จากร้านหนังสือสู่จักรวรรดิ E-commerce และ Cloud",
            "content": amzn_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "META",
            "type": "stock",
            "title": "Meta Platforms Deep Dive Analysis",
            "title_th": "เจาะลึก Meta Platforms (META): อาณาจักร Social Media ที่ใหญ่ที่สุด",
            "content": meta_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "TSLA",
            "type": "stock",
            "title": "Tesla Deep Dive Analysis",
            "title_th": "เจาะลึก Tesla (TSLA): มากกว่าแค่รถยนต์ไฟฟ้า มันคือ AI และหุ่นยนต์",
            "content": tsla_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "AMD",
            "type": "stock",
            "title": "AMD Deep Dive Analysis",
            "title_th": "เจาะลึก AMD: ผู้ท้าชิงบัลลังก์ชิปเซตที่น่ากลัวที่สุด",
            "content": amd_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "NFLX",
            "type": "stock",
            "title": "Netflix Deep Dive Analysis",
            "title_th": "เจาะลึก Netflix (NFLX): ราชาแห่งสตรีมมิ่งที่เปลี่ยนพฤติกรรมคนทั้งโลก",
            "content": nflx_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "QQQ",
            "type": "etf",
            "title": "Invesco QQQ Deep Dive Analysis",
            "title_th": "เจาะลึก QQQ: กองทุนรวมหุ้นเทคโนโลยีแห่งอนาคต",
            "content": qqq_analysis,
            "author": "Antigravity AI"
        }
    ]
    
    # Import Batch 2
    from scripts.data.seed_content_batch_2 import (
        brk_b_analysis, lly_analysis, avgo_analysis, jpm_analysis, v_analysis,
        unh_analysis, wmt_analysis, xom_analysis, ma_analysis, pg_analysis,
        jnj_analysis, hd_analysis, cost_analysis, orcl_analysis, abbv_analysis,
        ko_analysis, pep_analysis, adbe_analysis, dis_analysis, crm_analysis
    )

    batch_2_map = [
        {"symbol": "BRK.B", "title_th": "เจาะลึก Berkshire (BRK.B)", "content": brk_b_analysis},
        {"symbol": "LLY", "title_th": "เจาะลึก Eli Lilly (LLY)", "content": lly_analysis},
        {"symbol": "AVGO", "title_th": "เจาะลึก Broadcom (AVGO)", "content": avgo_analysis},
        {"symbol": "JPM", "title_th": "เจาะลึก JPMorgan (JPM)", "content": jpm_analysis},
        {"symbol": "V", "title_th": "เจาะลึก Visa (V)", "content": v_analysis},
        {"symbol": "UNH", "title_th": "เจาะลึก UnitedHealth (UNH)", "content": unh_analysis},
        {"symbol": "WMT", "title_th": "เจาะลึก Walmart (WMT)", "content": wmt_analysis},
        {"symbol": "XOM", "title_th": "เจาะลึก Exxon Mobil (XOM)", "content": xom_analysis},
        {"symbol": "MA", "title_th": "เจาะลึก Mastercard (MA)", "content": ma_analysis},
        {"symbol": "PG", "title_th": "เจาะลึก P&G (PG)", "content": pg_analysis},
        {"symbol": "JNJ", "title_th": "เจาะลึก Johnson & Johnson (JNJ)", "content": jnj_analysis},
        {"symbol": "HD", "title_th": "เจาะลึก Home Depot (HD)", "content": hd_analysis},
        {"symbol": "COST", "title_th": "เจาะลึก Costco (COST)", "content": cost_analysis},
        {"symbol": "ORCL", "title_th": "เจาะลึก Oracle (ORCL)", "content": orcl_analysis},
        {"symbol": "ABBV", "title_th": "เจาะลึก AbbVie (ABBV)", "content": abbv_analysis},
        {"symbol": "KO", "title_th": "เจาะลึก Coca-Cola (KO)", "content": ko_analysis},
        {"symbol": "PEP", "title_th": "เจาะลึก PepsiCo (PEP)", "content": pep_analysis},
        {"symbol": "ADBE", "title_th": "เจาะลึก Adobe (ADBE)", "content": adbe_analysis},
        {"symbol": "DIS", "title_th": "เจาะลึก Disney (DIS)", "content": dis_analysis},
        {"symbol": "CRM", "title_th": "เจาะลึก Salesforce (CRM)", "content": crm_analysis},
    ]

    for item in batch_2_map:
        data_map.append({
            "symbol": item["symbol"],
            "type": "stock",
            "title": f"{item['symbol']} Analysis",
            "title_th": item["title_th"],
            "content": item["content"],
            "author": "Antigravity AI"
        })

    # Import Batch 3
    from scripts.data.seed_content_batch_3 import (
        cvx_analysis, mrk_analysis, wfc_analysis, csco_analysis, acn_analysis,
        mcd_analysis, lin_analysis, abt_analysis, tmo_analysis, nke_analysis,
        pfe_analysis, dhr_analysis, txn_analysis, pm_analysis, nee_analysis,
        rtx_analysis, ms_analysis, hon_analysis, unp_analysis, amgn_analysis,
        intc_analysis, ibm_analysis, qcom_analysis, sbux_analysis, ge_analysis,
        ba_analysis, cat_analysis, gs_analysis, isrg_analysis, bkng_analysis,
        now_analysis, spgi_analysis, lmt_analysis, axp_analysis, syk_analysis,
        blk_analysis, uber_analysis, abnb_analysis, pltr_analysis, arm_analysis
    )

    batch_3_map = [
        {"symbol": "CVX", "title_th": "เจาะลึก Chevron (CVX)", "content": cvx_analysis},
        {"symbol": "MRK", "title_th": "เจาะลึก Merck (MRK)", "content": mrk_analysis},
        {"symbol": "WFC", "title_th": "เจาะลึก Wells Fargo (WFC)", "content": wfc_analysis},
        {"symbol": "CSCO", "title_th": "เจาะลึก Cisco (CSCO)", "content": csco_analysis},
        {"symbol": "ACN", "title_th": "เจาะลึก Accenture (ACN)", "content": acn_analysis},
        {"symbol": "MCD", "title_th": "เจาะลึก McDonald's (MCD)", "content": mcd_analysis},
        {"symbol": "LIN", "title_th": "เจาะลึก Linde (LIN)", "content": lin_analysis},
        {"symbol": "ABT", "title_th": "เจาะลึก Abbott (ABT)", "content": abt_analysis},
        {"symbol": "TMO", "title_th": "เจาะลึก Thermo Fisher (TMO)", "content": tmo_analysis},
        {"symbol": "NKE", "title_th": "เจาะลึก Nike (NKE)", "content": nke_analysis},
        {"symbol": "PFE", "title_th": "เจาะลึก Pfizer (PFE)", "content": pfe_analysis},
        {"symbol": "DHR", "title_th": "เจาะลึก Danaher (DHR)", "content": dhr_analysis},
        {"symbol": "TXN", "title_th": "เจาะลึก Texas Instruments (TXN)", "content": txn_analysis},
        {"symbol": "PM", "title_th": "เจาะลึก Philip Morris (PM)", "content": pm_analysis},
        {"symbol": "NEE", "title_th": "เจาะลึก NextEra Energy (NEE)", "content": nee_analysis},
        {"symbol": "RTX", "title_th": "เจาะลึก RTX Corp (RTX)", "content": rtx_analysis},
        {"symbol": "MS", "title_th": "เจาะลึก Morgan Stanley (MS)", "content": ms_analysis},
        {"symbol": "HON", "title_th": "เจาะลึก Honeywell (HON)", "content": hon_analysis},
        {"symbol": "UNP", "title_th": "เจาะลึก Union Pacific (UNP)", "content": unp_analysis},
        {"symbol": "AMGN", "title_th": "เจาะลึก Amgen (AMGN)", "content": amgn_analysis},
        {"symbol": "INTC", "title_th": "เจาะลึก Intel (INTC)", "content": intc_analysis},
        {"symbol": "IBM", "title_th": "เจาะลึก IBM", "content": ibm_analysis},
        {"symbol": "QCOM", "title_th": "เจาะลึก Qualcomm (QCOM)", "content": qcom_analysis},
        {"symbol": "SBUX", "title_th": "เจาะลึก Starbucks (SBUX)", "content": sbux_analysis},
        {"symbol": "GE", "title_th": "เจาะลึก GE Aerospace (GE)", "content": ge_analysis},
        {"symbol": "BA", "title_th": "เจาะลึก Boeing (BA)", "content": ba_analysis},
        {"symbol": "CAT", "title_th": "เจาะลึก Caterpillar (CAT)", "content": cat_analysis},
        {"symbol": "GS", "title_th": "เจาะลึก Goldman Sachs (GS)", "content": gs_analysis},
        {"symbol": "ISRG", "title_th": "เจาะลึก Intuitive Surgical (ISRG)", "content": isrg_analysis},
        {"symbol": "BKNG", "title_th": "เจาะลึก Booking Holdings (BKNG)", "content": bkng_analysis},
        {"symbol": "NOW", "title_th": "เจาะลึก ServiceNow (NOW)", "content": now_analysis},
        {"symbol": "SPGI", "title_th": "เจาะลึก S&P Global (SPGI)", "content": spgi_analysis},
        {"symbol": "LMT", "title_th": "เจาะลึก Lockheed Martin (LMT)", "content": lmt_analysis},
        {"symbol": "AXP", "title_th": "เจาะลึก American Express (AXP)", "content": axp_analysis},
        {"symbol": "SYK", "title_th": "เจาะลึก Stryker (SYK)", "content": syk_analysis},
        {"symbol": "BLK", "title_th": "เจาะลึก BlackRock (BLK)", "content": blk_analysis},
        {"symbol": "UBER", "title_th": "เจาะลึก Uber (UBER)", "content": uber_analysis},
        {"symbol": "ABNB", "title_th": "เจาะลึก Airbnb (ABNB)", "content": abnb_analysis},
        {"symbol": "PLTR", "title_th": "เจาะลึก Palantir (PLTR)", "content": pltr_analysis},
        {"symbol": "ARM", "title_th": "เจาะลึก Arm Holdings (ARM)", "content": arm_analysis},
    ]

    for item in batch_3_map:
        data_map.append({
            "symbol": item["symbol"],
            "type": "stock",
            "title": f"{item['symbol']} Analysis",
            "title_th": item["title_th"],
            "content": item["content"],
            "author": "Antigravity AI"
        })

    # Import Batch 4
    from scripts.data.seed_content_batch_4 import (
        amat_analysis, lrcx_analysis, mu_analysis, adi_analysis, t_analysis,
        vz_analysis, cmcsa_analysis, tmus_analysis, c_analysis, bac_analysis,
        schw_analysis, low_analysis, tgt_analysis, tjx_analysis, de_analysis,
        ups_analysis, fdx_analysis, cop_analysis, mo_analysis, gild_analysis,
        vrtx_analysis, regn_analysis, zts_analysis, cvs_analysis, el_analysis,
        lulu_analysis, panw_analysis, crwd_analysis, snps_analysis, cdns_analysis,
        adp_analysis, pypl_analysis, sq_analysis, shop_analysis, se_analysis,
        baba_analysis, pdd_analysis, tsm_analysis, jd_analysis, nio_analysis
    )

    batch_4_map = [
        {"symbol": "AMAT", "title_th": "เจาะลึก Applied Materials (AMAT)", "content": amat_analysis},
        {"symbol": "LRCX", "title_th": "เจาะลึก Lam Research (LRCX)", "content": lrcx_analysis},
        {"symbol": "MU", "title_th": "เจาะลึก Micron (MU)", "content": mu_analysis},
        {"symbol": "ADI", "title_th": "เจาะลึก Analog Devices (ADI)", "content": adi_analysis},
        {"symbol": "T", "title_th": "เจาะลึก AT&T (T)", "content": t_analysis},
        {"symbol": "VZ", "title_th": "เจาะลึก Verizon (VZ)", "content": vz_analysis},
        {"symbol": "CMCSA", "title_th": "เจาะลึก Comcast (CMCSA)", "content": cmcsa_analysis},
        {"symbol": "TMUS", "title_th": "เจาะลึก T-Mobile US (TMUS)", "content": tmus_analysis},
        {"symbol": "C", "title_th": "เจาะลึก Citigroup (C)", "content": c_analysis},
        {"symbol": "BAC", "title_th": "เจาะลึก Bank of America (BAC)", "content": bac_analysis},
        {"symbol": "SCHW", "title_th": "เจาะลึก Schwab (SCHW)", "content": schw_analysis},
        {"symbol": "LOW", "title_th": "เจาะลึก Lowe's (LOW)", "content": low_analysis},
        {"symbol": "TGT", "title_th": "เจาะลึก Target (TGT)", "content": tgt_analysis},
        {"symbol": "TJX", "title_th": "เจาะลึก TJX (TJX)", "content": tjx_analysis},
        {"symbol": "DE", "title_th": "เจาะลึก Deere (DE)", "content": de_analysis},
        {"symbol": "UPS", "title_th": "เจาะลึก UPS", "content": ups_analysis},
        {"symbol": "FDX", "title_th": "เจาะลึก FedEx (FDX)", "content": fdx_analysis},
        {"symbol": "COP", "title_th": "เจาะลึก ConocoPhillips (COP)", "content": cop_analysis},
        {"symbol": "MO", "title_th": "เจาะลึก Altria (MO)", "content": mo_analysis},
        {"symbol": "GILD", "title_th": "เจาะลึก Gilead (GILD)", "content": gild_analysis},
        {"symbol": "VRTX", "title_th": "เจาะลึก Vertex (VRTX)", "content": vrtx_analysis},
        {"symbol": "REGN", "title_th": "เจาะลึก Regeneron (REGN)", "content": regn_analysis},
        {"symbol": "ZTS", "title_th": "เจาะลึก Zoetis (ZTS)", "content": zts_analysis},
        {"symbol": "CVS", "title_th": "เจาะลึก CVS Health (CVS)", "content": cvs_analysis},
        {"symbol": "EL", "title_th": "เจาะลึก Estee Lauder (EL)", "content": el_analysis},
        {"symbol": "LULU", "title_th": "เจาะลึก Lululemon (LULU)", "content": lulu_analysis},
        {"symbol": "PANW", "title_th": "เจาะลึก Palo Alto (PANW)", "content": panw_analysis},
        {"symbol": "CRWD", "title_th": "เจาะลึก CrowdStrike (CRWD)", "content": crwd_analysis},
        {"symbol": "SNPS", "title_th": "เจาะลึก Synopsys (SNPS)", "content": snps_analysis},
        {"symbol": "CDNS", "title_th": "เจาะลึก Cadence (CDNS)", "content": cdns_analysis},
        {"symbol": "ADP", "title_th": "เจาะลึก ADP", "content": adp_analysis},
        {"symbol": "PYPL", "title_th": "เจาะลึก PayPal (PYPL)", "content": pypl_analysis},
        {"symbol": "SQ", "title_th": "เจาะลึก Block (SQ)", "content": sq_analysis},
        {"symbol": "SHOP", "title_th": "เจาะลึก Shopify (SHOP)", "content": shop_analysis},
        {"symbol": "SE", "title_th": "เจาะลึก Sea Ltd (SE)", "content": se_analysis},
        {"symbol": "BABA", "title_th": "เจาะลึก Alibaba (BABA)", "content": baba_analysis},
        {"symbol": "PDD", "title_th": "เจาะลึก Pinduoduo (PDD)", "content": pdd_analysis},
        {"symbol": "TSM", "title_th": "เจาะลึก TSMC (TSM)", "content": tsm_analysis},
        {"symbol": "JD", "title_th": "เจาะลึก JD.com (JD)", "content": jd_analysis},
        {"symbol": "NIO", "title_th": "เจาะลึก NIO", "content": nio_analysis},
    ]

    for item in batch_4_map:
        data_map.append({
            "symbol": item["symbol"],
            "type": "stock",
            "title": f"{item['symbol']} Analysis",
            "title_th": item["title_th"],
            "content": item["content"],
            "author": "Antigravity AI"
        })

    async with session_maker() as session:
        for item in data_map:
            print(f"Processing {item['symbol']}...")
            
            # Check if exists
            result = await session.execute(
                select(Analysis).where(
                    Analysis.symbol == item['symbol'],
                    Analysis.symbol_type == item['type']
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"Updating {item['symbol']}...")
                existing.content_th = item['content']
                existing.title_th = item['title_th']
                existing.updated_at = datetime.utcnow()
                existing.status = "published"
                existing.published_at = datetime.utcnow()
            else:
                print(f"Creating {item['symbol']}...")
                new_analysis = Analysis(
                    symbol=item['symbol'],
                    symbol_type=item['type'],
                    title=item['title'],
                    title_th=item['title_th'],
                    content_th=item['content'],
                    author=item['author'],
                    status="published",
                    published_at=datetime.utcnow()
                )
                session.add(new_analysis)
        
        await session.commit()
        print(f"Data seed completed successfully! ({len(data_map)} items processed)")
        return len(data_map)

if __name__ == "__main__":
    asyncio.run(seed_data())
