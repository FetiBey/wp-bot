import Link from "next/link";
import { navigation, sahibindenUrl } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="border-t border-ink/10 bg-white">
      <div className="container-premium grid gap-10 py-14 lg:grid-cols-[1.2fr_1fr_1fr]">
        <div>
          <p className="text-2xl font-semibold tracking-[-0.04em]">Seyfeli Gayrimenkul</p>
          <p className="mt-4 max-w-sm text-sm leading-7 text-ink/58">Kumrular Group güvencesiyle Ankara'da premium gayrimenkul ve yatırım danışmanlığı.</p>
          <p className="mt-8 text-xs uppercase tracking-[0.24em] text-ink/40">Powered by Kumrular Group</p>
        </div>
        <div className="grid grid-cols-2 gap-3 text-sm text-ink/62">
          {navigation.map((item) => <Link className="hover:text-primary" key={item.href} href={item.href}>{item.label}</Link>)}
        </div>
        <div className="space-y-3 text-sm text-ink/62">
          <Link className="block hover:text-primary" href={sahibindenUrl} target="_blank" rel="noreferrer">Sahibinden Kurumsal Mağaza</Link>
          <Link className="block hover:text-primary" href="/gizlilik-politikasi">Gizlilik Politikası</Link>
          <Link className="block hover:text-primary" href="/kvkk">KVKK</Link>
          <Link className="block hover:text-primary" href="/cerez-politikasi">Çerez Politikası</Link>
        </div>
      </div>
    </footer>
  );
}
