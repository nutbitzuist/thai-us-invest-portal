import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";

export const metadata: Metadata = {
  title: "ศูนย์ข้อมูลลงทุนหุ้นสหรัฐ | Thai U.S. Investment Portal",
  description: "แหล่งรวมข้อมูลหุ้นและ ETF สหรัฐอเมริกา สำหรับนักลงทุนไทย พร้อมบทวิเคราะห์ภาษาไทย",
  keywords: ["หุ้นสหรัฐ", "ลงทุนต่างประเทศ", "S&P 500", "Nasdaq 100", "ETF", "US stocks"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="th">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="min-h-screen flex flex-col">
        <Providers>
          <Navbar />
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
