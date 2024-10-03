"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import {
  House,
  BadgeCheck,
  Dumbbell,
  Award,
  CircleUserRound,
  LogOut,
} from "lucide-react";
import { removeToken } from "@/app/actions/auth";

const links = [
  { name: "Home", href: "/dashboard", icon: House },
  {
    name: "Exercises",
    href: "/dashboard/exercises",
    icon: Dumbbell,
  },
  { name: "Workouts", href: "/dashboard/workouts", icon: BadgeCheck },
  { name: "Your exercises", href: "/dashboard/user_exercises", icon: Award },
];

export default function NavLinks() {
  const pathname = usePathname();

  return (
    <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2 bg-secondary">
      {links.map((link) => {
        const LinkIcon = link.icon;
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              "flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-primary text-primary-foreground p-3 text-sm font-medium hover:bg-sky-100 hover:text-black md:flex-none md:justify-start md:p-2 md:px-3",
              {
                "bg-secondary text-secondary-foreground":
                  pathname === link.href,
              }
            )}
          >
            <LinkIcon className="w-6" />
            <p className="hidden md:block">{link.name}</p>
          </Link>
        );
      })}
      <div className="hidden h-auto w-full grow rounded-md md:block"></div>
      <Link
        href="/dashboard/account"
        className={clsx(
          "flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-primary text-primary-foreground p-3 text-sm font-medium hover:bg-sky-100 hover:text-black md:flex-none md:justify-start md:p-2 md:px-3"
        )}
      >
        <CircleUserRound />
        <p className="hidden md:block">Account</p>
      </Link>

      <Link
        onClick={async () => {
          await removeToken();
        }}
        href="/"
        className={clsx(
          "flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-primary text-primary-foreground p-3 text-sm font-medium hover:bg-sky-100 hover:text-black md:flex-none md:justify-start md:p-2 md:px-3"
        )}
      >
        <LogOut />
        <div className="hidden md:block">Sign Out</div>
      </Link>
    </div>
  );
}
