"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getToken } from "@/app/actions/auth";

export function DashboardButton() {
  const [hasToken, setHasToken] = useState(false);

  useEffect(() => {
    async function checkToken() {
      const token = await getToken();
      setHasToken(!!token);
    }
    checkToken();
  }, []);

  return (
    <>
      {hasToken && (
        <Link href="/dashboard">
          <Button>Dashboard</Button>
        </Link>
      )}
    </>
  );
}
