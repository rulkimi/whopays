"use client"

import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { Spinner } from "../ui/spinner"
import { Icons, type IconName } from "@/components/icons"

interface AppButtonProps
  extends React.ComponentPropsWithoutRef<typeof Button> {
  loading?: boolean
  icon?: IconName
  iconPosition?: "left" | "right"
}

export function AppButton({
  loading = false,
  icon,
  iconPosition = "left",
  children,
  className,
  disabled,
  variant,
  size,
  ...props
}: AppButtonProps) {
  const isDisabled = disabled || loading

  // Ensure icon shows if passed a valid key
  const IconComponent = icon ? Icons[icon] : undefined

  function renderIcon() {
    if (!IconComponent) return null
    // If IconComponent is a component (function or forwardRef), render it
    return (
      <span className="inline-flex items-center">
        <IconComponent className="h-4 w-4" aria-hidden="true" />
      </span>
    )
  }

  return (
    <Button
      variant={variant}
      size={size}
      disabled={isDisabled}
      className={cn(
        "relative inline-flex items-center justify-center gap-2",
        className
      )}
      {...props}
    >
      {/* Left icon or spinner */}
      {iconPosition === "left" && (
        loading ? <Spinner /> : icon ? renderIcon() : null
      )}

      {/* Button label */}
      <span className={cn(loading && "opacity-70")}>{children}</span>

      {/* Right icon */}
      {iconPosition === "right" && !loading && icon ? renderIcon() : null}
    </Button>
  )
}