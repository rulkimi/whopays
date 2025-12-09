"use client"

import { registerUser } from "@/actions/auth";
import { InputFormField } from "@/components/form-components/common-form-field";
import { FileUploadForm } from "@/components/form-components/file-upload-form";
import { PasswordFormField } from "@/components/form-components/password-form-field";
import { AppButton } from "@/components/ui-overide/app-button";
import { Form } from "@/components/ui/form";
import { generateUsernameSuggestion } from "@/lib/string";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const registerSchema = z.object({
  username: z.string().min(1, { message: "Username is required"}),
  name: z.string().min(1, { message: "Name is required"}),
  email: z.email({ message: "Invalid email address format." }).min(1, { message: "Email is required" }),
  password: z.string().min(1, { message: "Password is required"}),
  profile_photo: z.instanceof(File, { message: "Profile photo is required"})
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

  const watchedName = form.watch("name");

  useEffect(() => {
    if (watchedName && watchedName.trim().length > 0) {
      const suggestion = generateUsernameSuggestion(watchedName, form.getValues("username"));
      form.setValue("username", suggestion, { shouldValidate: true, shouldDirty: true });
    }
  }, [form, watchedName]);

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
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 w-full">
        <div className="flex flex-col sm:flex-row gap-4">
          <InputFormField
            control={form.control}
            name="name"
            label="Name"
            disabled={loading}
            placeholder="John Doe"
            required
          />
          <InputFormField
            control={form.control}
            name="username"
            label="Username"
            disabled={loading}
            placeholder="john_doe_339"
            required
          />
        </div>
        <InputFormField
          control={form.control}
          name="email"
          label="Email"
          disabled={loading}
          placeholder="johndoe@gmail.com"
          required
        />
        <PasswordFormField
          control={form.control}
          name="password"
          label="Password"
          disabled={loading}
          placeholder="At least 8 characters, use letters & numbers"
          required
        />
        <FileUploadForm
          control={form.control}
          name="profile_photo"
          label="Profile Photo"
          disabled={loading}
          config={{
            acceptedTypes: ["image/*"]
          }}
          required
        />
        <AppButton loading={loading} className="w-full">
          Register
        </AppButton>
      </form>
    </Form>
  )
}