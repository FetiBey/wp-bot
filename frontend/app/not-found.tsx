import Link from "next/link";

export default function NotFound() {
  return <main className="grid min-h-screen place-items-center bg-background px-6 text-center"><div><p className="text-sm font-bold uppercase tracking-[0.3em] text-accent">404</p><h1 className="mt-4 text-5xl font-semibold tracking-[-0.06em]">Sayfa bulunamadı.</h1><Link className="mt-8 inline-flex rounded-full bg-primary px-6 py-3 text-white" href="/">Ana sayfaya dön</Link></div></main>;
}
