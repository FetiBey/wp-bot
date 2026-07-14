import Link from "next/link";
import { navigation, sahibindenUrl } from "@/lib/constants";
import { Button } from "@/components/ui/button";

export function Header() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 px-4 py-4">
      <div className="container-premium glass flex h-16 items-center justify-between rounded-full px-5 shadow-[0_24px_80px_rgba(17,17,17,0.08)]">
        <Link href="/" className="flex items-center gap-3" aria-label="Seyfeli Gayrimenkul ana sayfa">
          <span className="grid size-10 place-items-center rounded-full bg-primary text-sm font-bold text-white">SG</span>
          <span className="leading-none">
            <span className="block text-sm font-semibold tracking-[-0.02em]">Seyfeli Gayrimenkul</span>
            <span className="block text-[10px] uppercase tracking-[0.28em] text-ink/45">Kumrular Group</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-7 lg:flex" aria-label="Ana menü">
          {navigation.map((item) => (
            <Link key={item.href} href={item.href} className="text-sm font-medium text-ink/62 transition hover:text-primary">
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <Link href="/en" className="hidden rounded-full border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-ink/65 transition hover:border-primary/30 hover:text-primary sm:inline-flex">
            EN
          </Link>
          <Button href={sahibindenUrl} external className="px-5 py-2.5">Portföy</Button>
        </div>
      </div>
    </header>
  );
}
