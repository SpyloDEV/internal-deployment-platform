import { useQuery } from "@tanstack/react-query";

export function useDashboardData() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => ({
      kpis: [
        { label: "Services", value: 24, delta: "+3" },
        { label: "Deployments", value: 418, delta: "+12%" },
        { label: "Success rate", value: "96.8%", delta: "+2.4%" },
        { label: "Avg duration", value: "3m 18s", delta: "-41s" },
      ],
      activity: [
        "customer-api promoted release v2.8.4 to production",
        "admin-dashboard preview environment auto-deployed from main",
        "document-processor rollback completed after failed health check",
        "notification-worker updated REDIS_URL in staging",
      ],
    }),
  });
}
