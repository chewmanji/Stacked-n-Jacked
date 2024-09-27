import { Button } from "@/components/ui/button";
import Link from "next/link";
import { getToken } from "@/app/actions/auth";

export default async function Home() {
  const token = await getToken(); //doesnt work as should, after logging out the button is Dashboard is still visible
  //because of CACHE??? (Home is server component)
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <p className="font-bold text-xl">Stacked&Jacked</p>
        <div className="flex gap-4 items-center flex-col sm:flex-row">
          Start tracking your gains today!
          <div>
            <Link href="/auth/login">
              <Button>Sign in</Button>
            </Link>

            <Link href="/auth/register">
              <Button>Sign up</Button>
            </Link>
          </div>
          {token ? (
            <Link href="/dashboard">
              <Button>Dashboard</Button>
            </Link>
          ) : undefined}
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  );
}
