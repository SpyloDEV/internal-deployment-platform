import { Siren } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const incidents = [
  { title: "failed production deploy", severity: "high", status: "investigating", service: "document-processor" },
  { title: "staging health degraded", severity: "medium", status: "open", service: "notification-worker" },
  { title: "preview deploy cancelled", severity: "low", status: "resolved", service: "admin-dashboard" },
] as const;

export default function IncidentsPage() {
  return (
    <DashboardShell
      title="Incidents"
      description="Track release incidents, failed production deployments, health regressions, and incident timelines through resolution."
      action={
        <Button>
          <Siren className="h-4 w-4" />
          New Incident
        </Button>
      }
    >
      <div className="grid gap-4 lg:grid-cols-3">
        {incidents.map((incident) => (
          <Card key={incident.title}>
            <CardHeader>
              <div className="flex items-start justify-between gap-3">
                <CardTitle>{incident.title}</CardTitle>
                <Badge tone={incident.status === "resolved" ? "completed" : "failed"}>{incident.severity}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">{incident.service}</p>
              <div className="rounded-md border bg-background p-3 text-sm">
                Status: {incident.status}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </DashboardShell>
  );
}
