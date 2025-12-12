export default function AuthCardText({
  title,
  description
}: {
  title: string;
  description: string
}) {
  return (
    <div className="hidden md:flex flex-col justify-center items-center w-full bg-primary rounded-r-xl text-primary-foreground p-8">
      <h2 className="text-2xl font-bold">{title}</h2>
      <p className="mt-2 text-primary-foreground/90 text-center">
        {description}
      </p>
    </div>
  )
}