import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import RegisterForm from "./_components/register-form";
import AuthCardText from "../_components/auth-card-text";
import Link from "next/link";

export default function RegisterPage() {
  return (
    <div className="flex">
      <Card className="w-full md:rounded-r-none">
        <CardHeader>
          <CardTitle className="text-xl">Register an account</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-8">
            <RegisterForm />
          </div>
        </CardContent>
        <CardFooter>
          Already have an account?&nbsp;
          <Link href="/login" className="text-primary hover:underline">Login Now</Link>
        </CardFooter>
      </Card>
      <AuthCardText
        title="Ready to split the bill?"
        description="Register now and make splitting easy with WhoPays!"
      />
    </div>
  )
}