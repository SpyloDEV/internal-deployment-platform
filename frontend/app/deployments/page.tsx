import Link from "next/link";
import { Rocket } from "lucide-react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const deployments = [
  {
    id: "dep_1048",
    service: "customer-api",
    environment: "production",
    version: "v2.8.4",
    status: "succeeded",
    duration: "3m 12s",
    actor: "SpyloDEV",
  },
  {
    id: "dep_1047",
    service: "admin-dashboard",
    environment: "preview",
    version: "pr-184",
    status: "building",
    duration: "1m 03s",
    actor: "Product Engineering",
  },
  {
    id: "dep_1046",
    service: "document-processor",
    environment: "production",
    version: "v1.9.2",
    status: "failed",
    duration: "2m 22s",
    actor: "Core Platform",
  },
] as const;

export default function DeploymentsPage() {
  return (
    <DashboardShell
      title="Deployments"
      description="Review release history, current rollout state, durations, failures, and rollback candidates across all services."
      action={
        <Button>
          <Rocket className="h-4 w-4" />
          Trigger Deploy
        </Button>
      }
    >
      <Card>
        <CardHeader>
          <CardTitle>Deployment History</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <Th>Deployment</Th>
                <Th>Service</Th>
                <Th>Environment</Th>
                <Th>Status</Th>
                <Th>Duration</Th>
                <Th>Triggered By</Th>
              </tr>
            </thead>
            <tbody>
              {deployments.map((deployment) => (
                <tr key={deployment.id}>
                  <Td>
                    <Link
                      className="font-medium text-primary"
                      href={`/deployments/${deployment.id}`}
                    >
                      {deployment.version}
                    </Link>
                  </Td>
                  <Td>{deployment.service}</Td>
                  <Td>{deployment.environment}</Td>
                  <Td>
                    <Badge tone={deployment.status}>{deployment.status}</Badge>
                  </Td>
                  <Td>{deployment.duration}</Td>
                  <Td>{deployment.actor}</Td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardContent>
      </Card>
    </DashboardShell>
  );
}
