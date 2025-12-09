import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import RegisterForm from "./_components/register-form";
import AuthCardText from "../_components/auth-card-text";

export default function RegisterPage() {
  return (
    <Card className="w-4xl">
      <CardHeader>
        <CardTitle className="text-xl">Register an account</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex gap-8">
          <RegisterForm />
          <AuthCardText
            title="Ready to split the bill?"
            description="Register now and make splitting easy with WhoPays!"
          />
        </div>
      </CardContent>
    </Card>
  )
}