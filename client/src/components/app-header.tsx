"use client"

import Link from "next/link";
import { IconName, Icons } from "./icons";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

interface NavMenu {
  url: string;
  label: string;
  icon: IconName
}

const NAV_MENUS: NavMenu[] = [
  {
    url: "/home",
    label: "Home",
    icon: "home",
  },
  {
    url: "/bills",
    label: "Bills",
    icon: "dollar-sign"
  },
  {
    url: "/friends",
    label: "Friends",
    icon: "users"
  },
  {
    url: "/stats",
    label: "Statistics",
    icon: "trending-up"
  }
];

export default function AppHeader() {
  const pathname = usePathname();

  return (
    <header
      className={cn(
        "shadow-sm border-t border-muted md:border md:border-border bg-background/30 backdrop-blur-md",
        "md:py-3 md:px-16 md:rounded-full",
        "fixed md:static bottom-0 left-0 w-full md:w-auto md:rounded-full z-30",
        "py-2 px-4",
        "rounded-none md:rounded-full"
      )}
    >
      <nav className="flex justify-between gap-2 md:gap-4">
        {NAV_MENUS.map(menu => {
          const Icon = Icons[menu.icon];
          const isActive = pathname === menu.url;
          return (
            <Link
              href={menu.url}
              key={menu.url}
              className={cn(
                "flex flex-1 flex-col items-center justify-center gap-0.5 py-1 text-xs",
                "md:flex-row md:gap-1.5 md:py-0 md:text-base",
                "hover:text-primary transition-colors duration-150",
                isActive && "text-primary"
              )}
            >
              <Icon className="size-5 md:size-4" />
              <span>{menu.label}</span>
            </Link>
          )
        })}
      </nav>
    </header>
  )
}