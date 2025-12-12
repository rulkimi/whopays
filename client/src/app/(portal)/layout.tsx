import AppHeader from "@/components/app-header";
import { ReactNode } from "react";

export default function PortalLayout({
  children
}: {
  children: Readonly<ReactNode>;
}) {
  return (
    <div className="w-full max-w-3xl mx-auto px-4 py-8">
      <AppHeader />
      {children}
    </div>
  )
}