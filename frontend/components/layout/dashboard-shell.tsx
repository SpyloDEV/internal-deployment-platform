import type React from "react";

import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";

export function DashboardShell({
  children,
  title,
  description,
  action,
}: {
  children: React.ReactNode;
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        <Sidebar />
        <main className="min-w-0 flex-1">
          <Topbar />
          <div className="dashboard-grid">
            <div className="mx-auto w-full max-w-7xl px-4 py-6 lg:px-8">
              <div className="mb-6 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
                <div>
                  <h1 className="text-2xl font-semibold tracking-normal">{title}</h1>
                  <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
                    {description}
                  </p>
                </div>
                {action}
              </div>
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
