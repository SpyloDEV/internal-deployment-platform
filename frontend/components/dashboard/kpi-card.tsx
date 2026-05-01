import { Card, CardContent } from "@/components/ui/card";

export function KpiCard({
  label,
  value,
  delta,
}: {
  label: string;
  value: string | number;
  delta: string;
}) {
  return (
    <Card>
      <CardContent className="pt-5">
        <p className="text-sm text-muted-foreground">{label}</p>
        <div className="mt-3 flex items-end justify-between gap-3">
          <p className="text-3xl font-semibold tracking-normal">{value}</p>
          <span className="rounded-md bg-emerald-500/15 px-2 py-1 text-xs font-medium text-emerald-300">
            {delta}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
