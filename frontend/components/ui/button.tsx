import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";

type ButtonProps = {
  href: string;
  children: ReactNode;
  variant?: "primary" | "light" | "ghost";
  external?: boolean;
  className?: string;
};

export function Button({ href, children, variant = "primary", external, className }: ButtonProps) {
  return (
    <Link
      href={href}
      target={external ? "_blank" : undefined}
      rel={external ? "noreferrer" : undefined}
      className={cn(
        "group inline-flex items-center justify-center gap-3 rounded-full px-6 py-3 text-sm font-semibold tracking-[-0.01em] transition duration-300 focus:outline-none focus:ring-2 focus:ring-accent/60 focus:ring-offset-2",
        variant === "primary" && "bg-primary text-white hover:bg-[#123b34]",
        variant === "light" && "bg-white text-ink hover:bg-white/90",
        variant === "ghost" && "border border-white/30 text-white hover:bg-white/10",
        className
      )}
    >
      {children}
      <ArrowUpRight className="size-4 transition group-hover:-translate-y-0.5 group-hover:translate-x-0.5" aria-hidden />
    </Link>
  );
}
