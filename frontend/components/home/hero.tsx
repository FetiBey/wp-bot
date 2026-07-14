import { Button } from "@/components/ui/button";
import { sahibindenUrl, whatsappUrl } from "@/lib/constants";

export function Hero() {
  return (
    <section className="relative min-h-screen overflow-hidden bg-primary text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_72%_18%,rgba(181,138,60,.45),transparent_28%),linear-gradient(120deg,rgba(24,76,66,.72),rgba(8,25,22,.9)),url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=2400&q=85')] bg-cover bg-center" />
      <div className="absolute inset-0 bg-gradient-to-t from-black/65 via-black/10 to-black/20" />
      <div className="container-premium relative flex min-h-screen items-end pb-16 pt-36 lg:pb-24">
        <div className="max-w-6xl">
          <p className="mb-6 text-xs font-semibold uppercase tracking-[0.36em] text-white/70">Kumrular Group güvencesiyle</p>
          <h1 className="text-balance text-5xl font-semibold tracking-[-0.075em] sm:text-7xl lg:text-[104px] lg:leading-[0.92]">
            Gayrimenkul, yalnızca bir yatırım değildir. Bir gelecektir.
          </h1>
          <div className="mt-9 flex max-w-3xl flex-col gap-8 md:flex-row md:items-end md:justify-between">
            <p className="text-balance text-lg leading-8 text-white/76 sm:text-2xl">Kumrular Group güvencesiyle Ankara'da premium gayrimenkul danışmanlığı.</p>
            <div className="flex shrink-0 flex-wrap gap-3">
              <Button href={whatsappUrl} external variant="light">WhatsApp</Button>
              <Button href={sahibindenUrl} external variant="ghost">Portföy</Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
