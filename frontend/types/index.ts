export type Status =
  | "healthy"
  | "degraded"
  | "offline"
  | "unknown"
  | "queued"
  | "building"
  | "deploying"
  | "succeeded"
  | "failed"
  | "cancelled"
  | "rolled_back";

export type DeployableService = {
  id: string;
  name: string;
  description: string;
  ownerTeam: string;
  serviceType: "frontend" | "backend" | "worker" | "api";
  framework: "nextjs" | "fastapi" | "node" | "python" | "other";
  status: "healthy" | "degraded" | "offline" | "unknown";
};

export type Deployment = {
  id: string;
  serviceId: string;
  environmentId: string;
  version: string;
  commitSha: string;
  status: Status;
};

export type Incident = {
  id: string;
  title: string;
  severity: "low" | "medium" | "high" | "critical";
  status: "open" | "investigating" | "resolved";
  serviceId?: string;
};
