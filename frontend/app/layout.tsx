import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import "./globals.css";

const manrope = Manrope({ subsets: ["latin", "latin-ext"], variable: "--font-manrope", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL("https://seyfeligayrimenkul.com"),
  title: { default: "Seyfeli Gayrimenkul | Kumrular Group", template: "%s | Seyfeli Gayrimenkul" },
  description: "Kumrular Group güvencesiyle Ankara'da premium gayrimenkul ve yatırım danışmanlığı.",
  openGraph: {
    title: "Seyfeli Gayrimenkul | Kumrular Group",
    description: "Ankara'da premium gayrimenkul danışmanlığı.",
    type: "website",
    locale: "tr_TR"
  },
  twitter: { card: "summary_large_image", title: "Seyfeli Gayrimenkul", description: "Kumrular Group güvencesiyle premium danışmanlık." },
  robots: { index: true, follow: true }
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    name: "Seyfeli Gayrimenkul",
    parentOrganization: { "@type": "Organization", name: "Kumrular Group" },
    areaServed: "Ankara",
    url: "https://seyfeligayrimenkul.com"
  };

  return (
    <html lang="tr" className={manrope.variable}>
      <body>
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
        {children}
      </body>
    </html>
  );
}
