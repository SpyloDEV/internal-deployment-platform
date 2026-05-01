import * as React from "react";
import { cn } from "@/lib/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  asChild?: boolean;
};

const variants = {
  primary: "bg-primary text-primary-foreground hover:bg-primary/90",
  secondary: "bg-muted text-foreground hover:bg-muted/80",
  ghost: "hover:bg-muted text-muted-foreground hover:text-foreground",
  danger: "bg-destructive text-white hover:bg-destructive/90",
};

export function Button({
  className,
  variant = "primary",
  asChild = false,
  children,
  ...props
}: ButtonProps) {
  const classes = cn(
    "inline-flex h-10 items-center justify-center gap-2 rounded-md px-4 text-sm font-medium transition disabled:pointer-events-none disabled:opacity-50",
    variants[variant],
    className,
  );

  if (asChild && React.isValidElement<{ className?: string }>(children)) {
    return React.cloneElement(children, {
      className: cn(classes, children.props.className),
    });
  }

  return (
    <button
      className={classes}
      {...props}
    >
      {children}
    </button>
  );
}
