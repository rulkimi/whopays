"use client"

import { loginUser } from "@/actions/auth";
import { InputFormField } from "@/components/form-components/common-form-field";
import { PasswordFormField } from "@/components/form-components/password-form-field";
import { AppButton } from "@/components/ui-overide/app-button";
import { Form } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const loginSchema = z.object({
  username: z.string().min(1, { message: "Username is required"}),
  password: z.string().min(1, { message: "Password is required"}),
});

export type LoginValues = z.infer<typeof loginSchema>;
 
export default function LoginForm() {
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const form = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: "",
    }
  });

  const onSubmit = async (values: LoginValues) => {
    setLoading(true);
    const result = await loginUser(values);
    if (!result.success) {
      toast.error(result.message);
    } else {
      toast.success(result.message);
      router.push("/home");
    }
    setLoading(false);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 w-full">
        <div className="flex flex-col sm:flex-row gap-4">
          <InputFormField
            control={form.control}
            name="username"
            label="Username/Email"
            disabled={loading}
            placeholder="john_doe_339"
            required
          />
        </div>
        <PasswordFormField
          control={form.control}
          name="password"
          label="Password"
          disabled={loading}
          placeholder="At least 8 characters, use letters & numbers"
          required
        />
        <AppButton loading={loading} className="w-full">
          Login
        </AppButton>
      </form>
    </Form>
  )
}