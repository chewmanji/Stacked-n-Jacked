"use server";

import {
  FormState,
  SigninFormSchema,
  SignupFormSchema,
} from "../lib/definitions";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { z } from "zod";

export async function signin(state: FormState, formData: FormData) {
  const validatedFields = SigninFormSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  const { email, password } = validatedFields.data;
  console.log(JSON.stringify({ username: email, password }));

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username: email, password }),
    }
  );

  if (response.ok) {
    const { access_token } = await response.json();

    cookies().set("token", access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });

    return redirect("/dashboard");
  } else if (response.status === 401) {
    return {
      message: "Incorrect email or password!",
    };
  } else {
    const error = await response.json();
    return {
      message: error.detail,
    };
  }
}

export async function signup(state: FormState, formData: FormData) {
  const genderData = z.coerce.number().parse(formData.get("gender"));
  const validatedFields = SignupFormSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
    gender: genderData,
    birthDate: formData.get("birthDate"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  const { email, password, gender, birthDate } = validatedFields.data;
  console.log(
    JSON.stringify({ email, password, gender, birth_date: birthDate })
  );

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/users`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        gender,
        birth_date: birthDate,
      }),
    }
  );

  if (response.ok) {
    redirect("/auth/login");
  } else {
    const error = await response.json();
    return {
      message: error.detail,
    };
  }
}

export async function removeToken() {
  cookies().delete("token");
}

export async function getToken() {
  const token = cookies().get("token")?.value;
  return token;
}
