"use client";

import { signup } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { useEffect } from "react";
import { useFormState, useFormStatus } from "react-dom";

export function SignUpForm() {
  const [state, action] = useFormState(signup, undefined);
  useEffect(() => {
    if (state?.message) alert(state.message);
  }, [state]);
  return (
    <form action={action} id="signup-form">
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
      {state?.errors?.password && (
        <div>
          <p>Password must:</p>
          <ul>
            {state.errors.password.map((error) => (
              <li key={error}>- {error}</li>
            ))}
          </ul>
        </div>
      )}
      <div>
        <Label htmlFor="birthDate">Birth date</Label>
        <Input id="birthDate" name="birthDate" type="date" />
      </div>

      <div>
        <Label htmlFor="gender">Gender</Label>
        <select id="gender" name="gender">
          <option value="2">---</option>
          <option value="0">Male</option>
          <option value="1">Female</option>
        </select>
      </div>
      <div className="flex justify-between w-full my-4">
        <Link href="/">
          <Button variant="outline">Go home</Button>
        </Link>
        {/*tried to use useRouter hook to router.back() but it didnt work - always returned to home page*/}

        <SubmitButton></SubmitButton>
      </div>
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <Button disabled={pending} type="submit">
      Register
    </Button>
  );
}
