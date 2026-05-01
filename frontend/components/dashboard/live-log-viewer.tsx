import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const logs = [
  "[10:42:01] deployment service=customer-api env=production status=succeeded",
  "[10:42:02] policy warning service=document-processor code=staging_success_required",
  "[10:42:03] health service=notification-worker env=staging status=degraded",
  "[10:42:04] rollback service=document-processor source=dep_1046 status=rolled_back",
];

export function LiveLogViewer() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Realtime Deployment Events</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border bg-slate-950 p-4 font-mono text-xs text-cyan-100">
          {logs.map((line) => (
            <p key={line} className="py-1">
              {line}
            </p>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
