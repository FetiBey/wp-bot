const lines = ["Biz ilan satmıyoruz.", "Doğru yatırımı buluyoruz.", "Güveni, veriyi ve vizyonu aynı masada buluşturuyoruz."];

export function Storytelling() {
  return (
    <section className="bg-background py-28 sm:py-40">
      <div className="container-premium">
        <div className="mx-auto max-w-5xl text-center">
          {lines.map((line, index) => (
            <p key={line} className="text-balance py-5 text-4xl font-semibold tracking-[-0.06em] text-ink sm:text-6xl lg:text-7xl" style={{ opacity: 1 - index * 0.18 }}>
              {line}
            </p>
          ))}
        </div>
      </div>
    </section>
  );
}
