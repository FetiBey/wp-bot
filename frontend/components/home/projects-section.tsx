import { projects } from "@/lib/constants";

export function ProjectsSection() {
  return (
    <section className="bg-background py-24 sm:py-32">
      <div className="container-premium">
        <div className="flex flex-col justify-between gap-8 lg:flex-row lg:items-end">
          <div className="max-w-3xl">
            <p className="mb-4 text-xs font-bold uppercase tracking-[0.3em] text-accent">Projeler</p>
            <h2 className="text-4xl font-semibold tracking-[-0.06em] sm:text-6xl">Portföy değil, şirket projeleri.</h2>
          </div>
          <p className="max-w-md text-lg leading-8 text-ink/58">Bu alanda yalnızca şirketin geliştirdiği veya stratejik olarak yönettiği proje hikâyeleri yer alır.</p>
        </div>
        <div className="mt-16 grid gap-5 lg:grid-cols-3">
          {projects.map((project, index) => (
            <article key={project.title} className="min-h-[440px] rounded-[2rem] bg-white p-6 shadow-[0_30px_80px_rgba(17,17,17,0.06)]">
              <div className="h-56 rounded-[1.5rem] bg-[radial-gradient(circle_at_30%_20%,rgba(181,138,60,.36),transparent_34%),linear-gradient(135deg,#184C42,#0f2f29)]" />
              <p className="mt-8 text-sm font-semibold text-accent">0{index + 1} · {project.location}</p>
              <h3 className="mt-3 text-3xl font-semibold tracking-[-0.05em]">{project.title}</h3>
              <p className="mt-4 leading-7 text-ink/58">{project.detail}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
