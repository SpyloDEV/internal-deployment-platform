import { ShieldCheck } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const violations = [
  { service: "document-processor", policy: "staging_success_required", severity: "blocker" },
  { service: "notification-worker", policy: "owner_team_required", severity: "warning" },
  { service: "customer-api", policy: "production_env_var_audit", severity: "warning" },
] as const;

export default function GovernancePage() {
  return (
    <DashboardShell
      title="Governance"
      description="Evaluate deployments against production guardrails, ownership checks, staging promotion policy, and offline-service blocks."
      action={
        <Button>
          <ShieldCheck className="h-4 w-4" />
          Evaluate
        </Button>
      }
    >
      <div className="grid gap-4 xl:grid-cols-[0.8fr_1.2fr]">
        <Card>
          <CardHeader>
            <CardTitle>Policy Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              "production deploy requires admin",
              "staging must pass before production",
              "offline service deploy blocked",
            ].map((policy) => (
              <div key={policy} className="rounded-md border bg-background p-3 text-sm">
                {policy}
              </div>
            ))}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Violations</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <thead>
                <tr>
                  <Th>Service</Th>
                  <Th>Policy</Th>
                  <Th>Severity</Th>
                </tr>
              </thead>
              <tbody>
                {violations.map((violation) => (
                  <tr key={`${violation.service}-${violation.policy}`}>
                    <Td className="font-medium">{violation.service}</Td>
                    <Td>{violation.policy}</Td>
                    <Td>
                      <Badge tone={violation.severity === "blocker" ? "failed" : "paused"}>{violation.severity}</Badge>
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
