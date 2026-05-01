import type React from "react";

import { cn } from "@/lib/utils";

const styles = {
  active: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  healthy: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  completed: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  succeeded: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  processing: "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
  running: "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
  building: "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
  deploying: "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
  queued: "bg-zinc-500/15 text-zinc-300 border-zinc-500/30",
  draft: "bg-zinc-500/15 text-zinc-300 border-zinc-500/30",
  inactive: "bg-zinc-500/15 text-zinc-300 border-zinc-500/30",
  unknown: "bg-zinc-500/15 text-zinc-300 border-zinc-500/30",
  paused: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  degraded: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  rolled_back: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  failed: "bg-red-500/15 text-red-300 border-red-500/30",
  cancelled: "bg-red-500/15 text-red-300 border-red-500/30",
  offline: "bg-red-500/15 text-red-300 border-red-500/30",
  revoked: "bg-red-500/15 text-red-300 border-red-500/30",
};

type BadgeProps = {
  children: React.ReactNode;
  tone?: keyof typeof styles;
  className?: string;
};

export function Badge({ children, tone = "draft", className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium capitalize",
        styles[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}
