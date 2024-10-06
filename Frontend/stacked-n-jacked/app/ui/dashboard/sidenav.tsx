import Link from "next/link";
import NavLinks from "@/app/ui/dashboard/navlinks";

export default function SideNav() {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="bg-primary mb-2 flex h-20 items-end justify-start rounded-md p-4 md:h-40"
        href="/"
      >
        <div className="w-32 md:w-40 font-serif italic text-primary-foreground">
          Stacked&Jacked
        </div>
      </Link>
      <NavLinks />
    </div>
  );
}
