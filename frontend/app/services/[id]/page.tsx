import Link from "next/link";
import { GitBranch, Rocket, Server } from "lucide-react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const deployments = [
  { version: "v2.8.4", env: "production", status: "succeeded", duration: "3m 12s" },
  { version: "v2.8.5-rc1", env: "staging", status: "succeeded", duration: "2m 44s" },
  { version: "v2.8.3", env: "production", status: "rolled_back", duration: "18s" },
] as const;

export default function ServiceDetailPage() {
  return (
    <DashboardShell
      title="customer-api"
      description="Backend service detail with repository metadata, health, deployment history, environment policy state, and rollback controls."
      action={
        <Button>
          <Rocket className="h-4 w-4" />
          Deploy
        </Button>
      }
    >
      <div className="grid gap-4 xl:grid-cols-[0.8fr_1.2fr]">
        <Card>
          <CardHeader>
            <CardTitle>Service Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <div className="flex items-center gap-3 rounded-md border bg-background p-3">
              <Server className="h-4 w-4 text-primary" />
              FastAPI backend / Core Platform
            </div>
            <div className="flex items-center gap-3 rounded-md border bg-background p-3">
              <GitBranch className="h-4 w-4 text-primary" />
              github.com/acme/customer-api
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <p className="text-muted-foreground">Status</p>
                <Badge tone="healthy">healthy</Badge>
              </div>
              <div>
                <p className="text-muted-foreground">Owner Team</p>
                <p className="font-medium">Core Platform</p>
              </div>
            </div>
            <Button asChild variant="secondary" className="w-full">
              <Link href="/services/customer-api/environments">Manage Environments</Link>
            </Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Recent Deployments</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <thead>
                <tr>
                  <Th>Version</Th>
                  <Th>Environment</Th>
                  <Th>Status</Th>
                  <Th>Duration</Th>
                </tr>
              </thead>
              <tbody>
                {deployments.map((deployment) => (
                  <tr key={`${deployment.version}-${deployment.env}`}>
                    <Td className="font-medium">{deployment.version}</Td>
                    <Td>{deployment.env}</Td>
                    <Td>
                      <Badge tone={deployment.status}>{deployment.status}</Badge>
                    </Td>
                    <Td>{deployment.duration}</Td>
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
