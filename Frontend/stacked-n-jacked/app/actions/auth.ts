"use server";

import { FormState, SignInFormSchema, UserFormData } from "../lib/definitions";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import moment from "moment";

export async function signIn(state: FormState, formData: FormData) {
  const validatedFields = SignInFormSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  const { email, password } = validatedFields.data;

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
      maxAge: 30 * 24 * 60 * 60, //30 days
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

export async function signUp(formData: UserFormData) {
  const body = JSON.stringify({
    email: formData.email,
    password: formData.password,
    gender: formData.gender,
    birth_date: moment(formData.birthDate).format("YYYY-MM-DD"),
  });
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/users`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body,
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
