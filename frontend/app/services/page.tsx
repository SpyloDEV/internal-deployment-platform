import Link from "next/link";
import { Activity, GitBranch, Server, ShieldCheck } from "lucide-react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const services = [
  {
    id: "customer-api",
    name: "customer-api",
    type: "backend",
    framework: "fastapi",
    status: "healthy",
    repo: "github.com/acme/customer-api",
    owner: "Core Platform",
  },
  {
    id: "admin-dashboard",
    name: "admin-dashboard",
    type: "frontend",
    framework: "nextjs",
    status: "healthy",
    repo: "github.com/acme/admin-dashboard",
    owner: "Product Engineering",
  },
  {
    id: "notification-worker",
    name: "notification-worker",
    type: "worker",
    framework: "python",
    status: "degraded",
    repo: "github.com/acme/notification-worker",
    owner: "Messaging",
  },
] as const;

export default function ServicesPage() {
  return (
    <DashboardShell
      title="Service Catalog"
      description="Register deployable services, ownership, repositories, runtime frameworks, and health state across engineering teams."
      action={
        <Button>
          <Activity className="h-4 w-4" />
          New Service
        </Button>
      }
    >
      <div className="grid gap-4 lg:grid-cols-3">
        {services.map((service) => (
          <Card key={service.name}>
            <CardHeader>
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="rounded-md bg-primary/15 p-2 text-primary">
                    <Server className="h-5 w-5" />
                  </div>
                  <div>
                    <CardTitle>{service.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {service.type} / {service.framework}
                    </p>
                  </div>
                </div>
                <Badge tone={service.status}>{service.status}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2 rounded-md border bg-background p-3 text-sm">
                <GitBranch className="h-4 w-4 text-primary" />
                {service.repo}
              </div>
              <div className="flex items-center gap-2 rounded-md border bg-background p-3 text-sm">
                <ShieldCheck className="h-4 w-4 text-emerald-300" />
                {service.owner}
              </div>
              <div className="flex gap-2">
                <Button asChild variant="secondary" className="flex-1">
                  <Link href={`/services/${service.id}`}>Open</Link>
                </Button>
                <Button asChild variant="ghost" className="flex-1">
                  <Link href={`/services/${service.id}/environments`}>Envs</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </DashboardShell>
  );
}
