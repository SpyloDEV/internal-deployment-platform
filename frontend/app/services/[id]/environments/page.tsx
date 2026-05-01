import { LockKeyhole, Rocket, ToggleRight } from "lucide-react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const environments = [
  { name: "development", branch: "main", status: "healthy", url: "dev.customer.internal" },
  { name: "staging", branch: "release", status: "healthy", url: "staging.customer.internal" },
  { name: "production", branch: "main", status: "degraded", url: "api.customer.internal" },
] as const;

const envVars = [
  { key: "DATABASE_URL", value: "********", secret: "yes" },
  { key: "REDIS_URL", value: "********", secret: "yes" },
  { key: "LOG_LEVEL", value: "INFO", secret: "no" },
] as const;

export default function ServiceEnvironmentsPage() {
  return (
    <DashboardShell
      title="Environments"
      description="Manage per-environment branches, base URLs, auto deploy settings, health checks, and masked secrets."
      action={
        <Button>
          <Rocket className="h-4 w-4" />
          Deploy Staging
        </Button>
      }
    >
      <div className="space-y-4">
        <div className="grid gap-4 lg:grid-cols-3">
          {environments.map((environment) => (
            <Card key={environment.name}>
              <CardHeader>
                <div className="flex items-center justify-between gap-3">
                  <CardTitle>{environment.name}</CardTitle>
                  <Badge tone={environment.status}>{environment.status}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <p className="text-muted-foreground">{environment.url}</p>
                <div className="flex items-center justify-between rounded-md border bg-background p-3">
                  <span>{environment.branch}</span>
                  <ToggleRight className="h-5 w-5 text-primary" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Environment Variables</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <thead>
                <tr>
                  <Th>Key</Th>
                  <Th>Value</Th>
                  <Th>Secret</Th>
                </tr>
              </thead>
              <tbody>
                {envVars.map((envVar) => (
                  <tr key={envVar.key}>
                    <Td className="font-medium">{envVar.key}</Td>
                    <Td>{envVar.value}</Td>
                    <Td>
                      <div className="flex items-center gap-2">
                        <LockKeyhole className="h-4 w-4 text-primary" />
                        {envVar.secret}
                      </div>
                    </Td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
