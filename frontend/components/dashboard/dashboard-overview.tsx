"use client";

import { KpiCard } from "@/components/dashboard/kpi-card";
import { LiveLogViewer } from "@/components/dashboard/live-log-viewer";
import { ExecutionChart } from "@/components/charts/execution-chart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useDashboardData } from "@/hooks/use-dashboard-data";

export function DashboardOverview() {
  const { data, isLoading } = useDashboardData();

  if (isLoading || !data) {
    return (
      <div className="grid gap-4 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className="h-32" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {data.kpis.map((item) => (
          <KpiCard key={item.label} {...item} />
        ))}
      </div>
      <div className="grid gap-4 xl:grid-cols-[1.4fr_0.9fr]">
        <Card>
          <CardHeader>
            <CardTitle>Deployments Per Day</CardTitle>
          </CardHeader>
          <CardContent>
            <ExecutionChart />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {data.activity.map((item) => (
              <div key={item} className="rounded-md border bg-background/70 p-3 text-sm">
                {item}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
      <LiveLogViewer />
    </div>
  );
}
