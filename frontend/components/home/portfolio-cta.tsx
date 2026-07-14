import { Button } from "@/components/ui/button";
import { sahibindenUrl } from "@/lib/constants";

export function PortfolioCta() {
  return (
    <section className="bg-white py-24 sm:py-32">
      <div className="container-premium rounded-[2.5rem] bg-ink px-6 py-20 text-center text-white sm:px-12">
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-accent">Resmi Portföy</p>
        <h2 className="mx-auto mt-6 max-w-4xl text-balance text-4xl font-semibold tracking-[-0.06em] sm:text-6xl">Tüm portföyümüz resmi Sahibinden Kurumsal Mağazamızda yayınlanmaktadır.</h2>
        <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-white/62">Bu web sitesi ilan listelemez; doğru yatırım kararı için kurumsal danışmanlık deneyimini anlatır.</p>
        <div className="mt-10"><Button href={sahibindenUrl} external variant="light">Portföyü Görüntüle</Button></div>
      </div>
    </section>
  );
}
