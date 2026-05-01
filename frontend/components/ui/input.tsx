import * as React from "react";
import { cn } from "@/lib/utils";

export function Input({
  className,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-10 w-full rounded-md border bg-background px-3 text-sm outline-none ring-offset-background transition placeholder:text-muted-foreground focus:ring-2 focus:ring-primary/30",
        className,
      )}
      {...props}
    />
  );
}
