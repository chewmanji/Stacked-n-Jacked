"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getToken, removeToken } from "@/app/actions/auth";

export function HomePageButtons() {
  const [hasToken, setHasToken] = useState(false);
  useEffect(() => {
    async function checkToken() {
      const token = await getToken();
      setHasToken(!!token);
    }
    checkToken();
  }, []);

  return hasToken ? (
    <>
      <Link href="/dashboard">
        <Button size="lg">Dashboard</Button>
      </Link>
      <Button
        variant="secondary"
        onClick={async () => {
          await removeToken();
          setHasToken(false);
        }}
      >
        Log out
      </Button>
    </>
  ) : (
    <>
      <Link href="/auth/login">
        <Button size="lg">Sign in</Button>
      </Link>
      <Link href="/auth/register">
        <Button>Sign up</Button>
      </Link>
    </>
  );
}
