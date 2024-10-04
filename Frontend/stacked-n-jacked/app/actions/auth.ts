"use server";

import { Gender } from "../lib/definitions";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import moment from "moment";

export async function signIn(formData: { email: string; password: string }) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        username: formData.email,
        password: formData.password,
      }),
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

export async function signUp(formData: {
  email: string;
  password: string;
  birthDate: Date;
  gender: Gender;
}): Promise<{ message: string } | void> {
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

export async function editProfile(formData: {
  email?: string;
  newPassword?: string;
  birthDate?: Date;
  gender?: Gender;
}): Promise<{ message: string } | void> {
  const token = await getToken();
  const body = JSON.stringify({
    email: formData.email,
    password: formData.newPassword,
    gender: formData.gender,
    birth_date: moment(formData.birthDate).format("YYYY-MM-DD"),
  });
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/users`,
    {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: body,
    }
  );

  if (response.ok) {
    if (formData.newPassword || formData.email) {
      redirect("/auth/login");
    }
    return;
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
