import { ExecutionChart } from "@/components/charts/execution-chart";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function AnalyticsPage() {
  return (
    <DashboardShell
      title="Analytics"
      description="Track deployment velocity, release success, rollback volume, failed rollouts, average duration, and service reliability."
    >
      <div className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <KpiCard label="Success rate" value="96.8%" delta="+2.4%" />
          <KpiCard label="Failed deploys" value={7} delta="-22%" />
          <KpiCard label="Avg duration" value="3m 18s" delta="-41s" />
          <KpiCard label="Rollbacks" value={3} delta="-40%" />
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Deployment Volume</CardTitle>
          </CardHeader>
          <CardContent>
            <ExecutionChart />
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
