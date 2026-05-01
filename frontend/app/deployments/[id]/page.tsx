import { RotateCcw, Terminal } from "lucide-react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const timeline = [
  { step: "queued", status: "succeeded", message: "Deployment queued by platform API." },
  { step: "build", status: "succeeded", message: "Dependencies installed and tests passed." },
  { step: "release", status: "succeeded", message: "Release promoted to production." },
  { step: "health", status: "succeeded", message: "Health check passed in 83 ms." },
] as const;

const logs = [
  "Cloning repository github.com/acme/customer-api",
  "Installing dependencies",
  "Running test suite",
  "Building deployment image",
  "Deploying release to production",
  "Running health check",
  "Deployment succeeded",
];

export default function DeploymentDetailPage() {
  return (
    <DashboardShell
      title="Deployment dep_1048"
      description="Live release detail with status timeline, deployment logs, policy result, health check output, and rollback controls."
      action={
        <Button variant="secondary">
          <RotateCcw className="h-4 w-4" />
          Rollback
        </Button>
      }
    >
      <div className="grid gap-4 xl:grid-cols-[0.85fr_1.15fr]">
        <Card>
          <CardHeader>
            <CardTitle>Status Timeline</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {timeline.map((item) => (
              <div key={item.step} className="rounded-md border bg-background p-3">
                <div className="mb-2 flex items-center justify-between gap-3">
                  <p className="font-medium capitalize">{item.step}</p>
                  <Badge tone={item.status}>{item.status}</Badge>
                </div>
                <p className="text-sm text-muted-foreground">{item.message}</p>
              </div>
            ))}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Terminal className="h-4 w-4 text-primary" />
              <CardTitle>Live Logs</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="h-[360px] overflow-y-auto rounded-md border bg-black p-4 font-mono text-xs text-emerald-200">
              {logs.map((line) => (
                <p key={line} className="py-1">
                  <span className="text-muted-foreground">$</span> {line}
                </p>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
