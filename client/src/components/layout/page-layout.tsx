import { ReactNode } from "react"

export default function PageLayout ({
  children
}: {
  children: Readonly<ReactNode>;
}) {
  return (
    <main className="max-w-3xl mx-auto px-4 py-8">
      {children}
    </main>
  )
}