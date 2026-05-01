import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const logs = [
  { action: "deployment_triggered", actor: "platform@example.com", target: "customer-api", time: "4 min ago" },
  { action: "env_var_updated", actor: "platform@example.com", target: "DATABASE_URL", time: "18 min ago" },
  { action: "rollback_triggered", actor: "system", target: "document-processor", time: "22 min ago" },
] as const;

export default function AuditLogsPage() {
  return (
    <DashboardShell
      title="Audit Logs"
      description="Review security-relevant actions across services, environments, deployments, rollbacks, secrets, policies, and incidents."
    >
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <Th>Action</Th>
                <Th>Actor</Th>
                <Th>Target</Th>
                <Th>Time</Th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={`${log.action}-${log.time}`}>
                  <Td className="font-medium">{log.action}</Td>
                  <Td>{log.actor}</Td>
                  <Td>{log.target}</Td>
                  <Td className="text-muted-foreground">{log.time}</Td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardContent>
      </Card>
    </DashboardShell>
  );
}
