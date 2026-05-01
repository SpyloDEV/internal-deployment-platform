import Link from "next/link";
import {
  Activity,
  ChartSpline,
  ClipboardList,
  LayoutDashboard,
  ListChecks,
  Rocket,
  Settings,
  ShieldCheck,
  Siren,
} from "lucide-react";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/services", label: "Services", icon: Activity },
  { href: "/deployments", label: "Deployments", icon: Rocket },
  { href: "/analytics", label: "Analytics", icon: ChartSpline },
  { href: "/governance", label: "Governance", icon: ShieldCheck },
  { href: "/audit-logs", label: "Audit Logs", icon: ClipboardList },
  { href: "/incidents", label: "Incidents", icon: Siren },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-72 border-r bg-card/70 px-4 py-5 lg:block">
      <Link href="/dashboard" className="mb-8 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <ListChecks className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold">DeployOps</p>
          <p className="text-xs text-muted-foreground">Internal Delivery Platform</p>
        </div>
      </Link>
      <nav className="space-y-1">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 rounded-md px-3 py-2.5 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground"
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
