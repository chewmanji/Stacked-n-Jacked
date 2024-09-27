"use client";

import { signin } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { useEffect } from "react";
import { useFormState, useFormStatus } from "react-dom";

export function SignInForm() {
  const [state, action] = useFormState(signin, undefined);
  useEffect(() => {
    if (state?.message) alert(state.message);
  }, [state]);
  return (
    <form action={action}>
      <div>
        <Label htmlFor="email">Email</Label>
        <Input id="email" name="email" placeholder="Email" />
      </div>
      {state?.errors?.email && <p>{state.errors.email}</p>}
      <div>
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          name="password"
          type="password"
          placeholder="Password"
        />
      </div>
      <div className="flex justify-between w-full my-4">
        <Link href="/">
          <Button variant="outline">Go home</Button>
        </Link>
        <SubmitButton></SubmitButton>
      </div>
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <Button disabled={pending} type="submit">
      Login
    </Button>
  );
}
