import { DashboardOverview } from "@/components/dashboard/dashboard-overview";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  return (
    <DashboardShell
      title="Deployment Overview"
      description="Monitor services, release health, rollout velocity, failed deploys, rollbacks, and policy guardrails from one internal platform."
      action={<Button>Register Service</Button>}
    >
      <DashboardOverview />
    </DashboardShell>
  );
}
