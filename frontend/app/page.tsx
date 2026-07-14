import { Footer } from "@/components/layout/footer";
import { Header } from "@/components/layout/header";
import { GroupSection } from "@/components/home/group-section";
import { Hero } from "@/components/home/hero";
import { PortfolioCta } from "@/components/home/portfolio-cta";
import { ProjectsSection } from "@/components/home/projects-section";
import { ServicesShowcase } from "@/components/home/services-showcase";
import { Storytelling } from "@/components/home/storytelling";

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Storytelling />
        <ServicesShowcase />
        <GroupSection />
        <ProjectsSection />
        <PortfolioCta />
      </main>
      <Footer />
    </>
  );
}
