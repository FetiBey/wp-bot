import { services } from "@/lib/constants";

export function ServicesShowcase() {
  return (
    <section className="bg-white py-24 sm:py-32">
      <div className="container-premium">
        <div className="mb-16 max-w-3xl">
          <p className="mb-4 text-xs font-bold uppercase tracking-[0.3em] text-accent">Hizmetler</p>
          <h2 className="text-4xl font-semibold tracking-[-0.06em] sm:text-6xl">Her karar, ayrı bir strateji gerektirir.</h2>
        </div>
        <div className="divide-y divide-ink/10 border-y border-ink/10">
          {services.map(([title, description], index) => (
            <article key={title} className="group grid gap-8 py-10 transition hover:bg-primary/[0.025] lg:grid-cols-[0.2fr_0.8fr_1.2fr] lg:items-center">
              <span className="text-sm font-semibold text-accent">0{index + 1}</span>
              <h3 className="text-3xl font-semibold tracking-[-0.05em] sm:text-5xl">{title}</h3>
              <p className="max-w-2xl text-lg leading-8 text-ink/58">{description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
