import { SignUpForm } from "@/app/ui/auth/signup-form";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
export default function Page() {
  return (
    <div className="flex justify-center py-4">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Register an account</CardTitle>
        </CardHeader>
        <CardContent>
          <SignUpForm></SignUpForm>
        </CardContent>
      </Card>
    </div>
  );
}
