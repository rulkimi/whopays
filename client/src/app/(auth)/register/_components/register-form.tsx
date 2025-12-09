"use client"

import { registerUser } from "@/actions/auth";
import { InputFormField } from "@/components/form-components/common-form-field";
import { FileUploadForm } from "@/components/form-components/file-upload-form";
import { PasswordFormField } from "@/components/form-components/password-form-field";
import { AppButton } from "@/components/ui-overide/app-button";
import { Form } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const registerSchema = z.object({
  username: z.string(),
  name: z.string(),
  email: z.email(),
  password: z.string(),
  profile_photo: z.instanceof(File)
});

export type RegisterValues = z.infer<typeof registerSchema>;
 
export default function RegisterForm() {
  const [loading, setLoading] = useState(false);
  const form = useForm<RegisterValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      name: "",
      email: "",
      password: "",
      profile_photo: undefined
    }
  });

  const onSubmit = async (values: RegisterValues) => {
    setLoading(true);
    const result = await registerUser(values);
    if (!result.success) {
      toast.error(result.message);
    } else {
      toast.success(result.message);
    }
    setLoading(false);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <InputFormField
          control={form.control} 
          name="username" 
          label="Username"
          disabled={loading} 
          required
        />
        <InputFormField
          control={form.control}
          name="email"
          label="Email"
          disabled={loading}
          required
        />
        <PasswordFormField
          control={form.control}
          name="password"
          label="Password"
          disabled={loading}
          required
        />
        <InputFormField
          control={form.control} 
          name="name" 
          label="Name" 
          disabled={loading}
          required
        />
        <FileUploadForm
          control={form.control}
          name="profile_photo"
          label="Profile Photo"
          disabled={loading}
          required
        />
        <AppButton loading={loading}>
          Register
        </AppButton>
      </form>
    </Form>
  )
}