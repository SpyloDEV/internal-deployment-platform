import { Bell, ChevronsUpDown, Search } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Topbar() {
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b bg-background/90 px-4 backdrop-blur lg:px-8">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <div className="hidden h-10 w-full max-w-md items-center gap-2 rounded-md border bg-card px-3 md:flex">
          <Search className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm text-muted-foreground">
            Search services, deployments, logs, incidents
          </span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="secondary" className="hidden sm:inline-flex">
          SpyloDEV Platform
          <ChevronsUpDown className="h-4 w-4" />
        </Button>
        <Button variant="ghost" className="h-10 w-10 px-0" aria-label="Notifications">
          <Bell className="h-4 w-4" />
        </Button>
        <div className="flex h-10 w-10 items-center justify-center rounded-full border bg-card text-sm font-semibold">
          SD
        </div>
      </div>
    </header>
  );
}
