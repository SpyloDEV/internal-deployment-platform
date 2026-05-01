import { AuthForm } from "@/components/forms/auth-form";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4">
      <AuthForm mode="login" />
    </main>
  );
}
