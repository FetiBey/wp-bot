const milestones = ["Kurumsal yatırım disiplini", "Ankara odaklı güçlü saha bilgisi", "Şeffaf danışmanlık süreçleri", "Grup ölçeğinde sürdürülebilir güven"];

export function GroupSection() {
  return (
    <section className="overflow-hidden bg-primary py-24 text-white sm:py-32">
      <div className="container-premium grid gap-16 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <div>
          <p className="mb-5 text-xs font-bold uppercase tracking-[0.3em] text-accent">Kumrular Group</p>
          <h2 className="text-balance text-5xl font-semibold tracking-[-0.07em] sm:text-7xl">A powerful group. A trusted future.</h2>
          <p className="mt-8 max-w-xl text-lg leading-8 text-white/68">Seyfeli Gayrimenkul, bireysel satış reflekslerinden çok daha fazlasıdır. Kumrular Group'un kurumsal hafızası, yatırım yaklaşımı ve güven kültürüyle hareket eder.</p>
        </div>
        <div className="rounded-[2rem] border border-white/12 bg-white/[0.06] p-5 shadow-2xl backdrop-blur">
          <div className="rounded-[1.5rem] bg-[linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.03)),url('https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1600&q=85')] bg-cover bg-center p-8 sm:p-12">
            <div className="ml-auto max-w-md rounded-3xl bg-black/40 p-8 backdrop-blur-md">
              {milestones.map((item, index) => (
                <div key={item} className="flex gap-5 border-b border-white/15 py-5 last:border-0">
                  <span className="text-sm font-semibold text-accent">{String(index + 1).padStart(2, "0")}</span>
                  <p className="text-xl font-semibold tracking-[-0.03em]">{item}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
