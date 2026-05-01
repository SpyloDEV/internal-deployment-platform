"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { day: "Mon", deployments: 32 },
  { day: "Tue", deployments: 48 },
  { day: "Wed", deployments: 41 },
  { day: "Thu", deployments: 63 },
  { day: "Fri", deployments: 74 },
  { day: "Sat", deployments: 52 },
  { day: "Sun", deployments: 68 },
];

export function ExecutionChart() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ left: -24, right: 8, top: 10, bottom: 0 }}>
        <defs>
          <linearGradient id="deployments" x1="0" x2="0" y1="0" y2="1">
            <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.5} />
            <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid stroke="hsl(var(--border))" vertical={false} />
        <XAxis dataKey="day" tickLine={false} axisLine={false} />
        <YAxis tickLine={false} axisLine={false} />
        <Tooltip
          contentStyle={{
            background: "hsl(var(--card))",
            border: "1px solid hsl(var(--border))",
            borderRadius: 8,
          }}
        />
        <Area
          type="monotone"
          dataKey="deployments"
          stroke="hsl(var(--primary))"
          fill="url(#deployments)"
          strokeWidth={2}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
