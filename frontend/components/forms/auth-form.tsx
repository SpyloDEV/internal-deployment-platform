"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { apiRequest } from "@/lib/api";
import { setToken } from "@/lib/auth";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  full_name: z.string().optional(),
});

type AuthValues = z.infer<typeof schema>;

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const router = useRouter();
  const form = useForm<AuthValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      email: "demo@acme.ai",
      password: "SecurePass123!",
      full_name: "Demo Operator",
    },
  });

  async function onSubmit(values: AuthValues) {
    try {
      const path = mode === "login" ? "/auth/login" : "/auth/register";
      const payload =
        mode === "login"
          ? { email: values.email, password: values.password }
          : values;
      const response = await apiRequest<{ access_token: string }>(path, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setToken(response.access_token);
      toast.success("Session started");
      router.push("/dashboard");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Authentication failed");
    }
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>{mode === "login" ? "Log in" : "Create account"}</CardTitle>
        <p className="text-sm text-muted-foreground">
          {mode === "login"
          ? "Access the internal deployment platform."
            : "Start a workspace for platform engineering."}
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          {mode === "register" ? (
            <Input placeholder="Full name" {...form.register("full_name")} />
          ) : null}
          <Input placeholder="Email" type="email" {...form.register("email")} />
          <Input placeholder="Password" type="password" {...form.register("password")} />
          <Button className="w-full" type="submit" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? "Working..." : "Continue"}
          </Button>
        </form>
        <p className="mt-5 text-sm text-muted-foreground">
          {mode === "login" ? "Need an account? " : "Already registered? "}
          <Link
            className="font-medium text-primary"
            href={mode === "login" ? "/register" : "/login"}
          >
            {mode === "login" ? "Register" : "Log in"}
          </Link>
        </p>
      </CardContent>
    </Card>
  );
}
