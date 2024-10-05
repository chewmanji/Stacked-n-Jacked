import { SignInForm } from "@/app/ui/auth/signin-form";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { buttonVariants } from "@/components/ui/button";
import Link from "next/link";
export default function Page() {
  return (
    <div className="flex justify-center py-4">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Log in to account</CardTitle>
        </CardHeader>
        <CardContent>
          <SignInForm></SignInForm>
        </CardContent>
        <CardFooter className="text-sm justify-center">
          Don&apos;t have an account?{" "}
          <Link
            href="/auth/register"
            className={`${buttonVariants({ variant: "link" })}`}
          >
            Register
          </Link>{" "}
          there
        </CardFooter>
      </Card>
    </div>
  );
}
