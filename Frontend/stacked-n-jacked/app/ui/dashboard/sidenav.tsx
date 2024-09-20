import Link from "next/link";
import NavLinks from "@/app/ui/dashboard/navlinks";
import { CircleUserRound, LogOut } from "lucide-react";

export default function SideNav() {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="mb-2 flex h-20 items-end justify-start rounded-md bg-gray-800 p-4 md:h-40"
        href="/"
      >
        <div className="w-32 text-white md:w-40">HOME PAGE</div>
      </Link>
      <NavLinks />
    </div>
  );
}
