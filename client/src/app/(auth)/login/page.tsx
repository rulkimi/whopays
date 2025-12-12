import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import LoginForm from "./_components/login-form";
import AuthCardText from "../_components/auth-card-text";
import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="flex w-4xl">
      <Card className="w-full md:rounded-r-none">
        <CardHeader>
          <CardTitle className="text-xl">Login your account</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-8">
            <LoginForm />
          </div>
        </CardContent>
        <CardFooter>
          Don&apos;t have an account?&nbsp;
          <Link href="/register" className="text-primary hover:underline">Register Now</Link>
        </CardFooter>
      </Card>
      <AuthCardText
        title="Let&apos;s Settle Up!"
        description="Login to keep tabs on expenses and pass the bill with ease using WhoPays."
      />
    </div>
  )
}