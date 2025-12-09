import { ReactNode } from "react";

export default function AuthLayout({
  children
}: {
  children: Readonly<ReactNode>;
}) {
  return (
    <main className="min-h-screen flex justify-center items-center p-4">
      {children}
    </main>
  )
}