import type { ReactNode } from "react";
import type {
	Control,
	ControllerRenderProps,
	FieldPath,
	FieldValues} from "react-hook-form";
import {
	useFormContext,
	useFormState,
} from "react-hook-form";
import {
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
import RequiredAsterisk from "./required-asterisk";
import { AnimatePresence, motion } from "motion/react";
import { InputGroup, InputGroupButton, InputGroupInput } from "../ui/input-group";

/* ----------------------------- Motion Variants ---------------------------- */

const layoutTransition = {
	type: "spring" as const,
	stiffness: 400,
	damping: 30,
};

const errorMessageVariants = {
	initial: { opacity: 0, y: 8 },
	animate: { opacity: 1, y: 0 },
	exit: { opacity: 0, y: 8 },
};

const emptyMessageVariants = {
	initial: { opacity: 0, height: 0 },
	animate: { opacity: 0, height: 0 },
	exit: { opacity: 0, height: 0 },
};

/* --------------------------- Animated Error Block -------------------------- */

const AnimatedFormMessage = ({ hasError }: { hasError: boolean }) => (
	<AnimatePresence mode="wait" initial={false}>
		{hasError ? (
			<motion.div
				key="form-message"
				variants={errorMessageVariants}
				initial="initial"
				animate="animate"
				exit="exit"
				transition={{ duration: 0.2 }}
			>
				<FormMessage />
			</motion.div>
		) : (
			<motion.div
				key="form-message-empty"
				variants={emptyMessageVariants}
				initial="initial"
				animate="animate"
				exit="exit"
				style={{ overflow: "hidden" }}
			/>
		)}
	</AnimatePresence>
);

/* ------------------------------- Base Field ------------------------------- */

interface BaseFormFieldProps<T extends FieldValues> {
	control: Control<T>;
	name: FieldPath<T>;
	label?: string;
	description?: string;
	required?: boolean;
}

export function CommonFormField<T extends FieldValues>({
	control,
	name,
	label,
	description,
	required,
	render,
}: BaseFormFieldProps<T> & {
	render: (field: ControllerRenderProps<T, FieldPath<T>>) => ReactNode;
}) {
	const { getFieldState } = useFormContext();
	const formState = useFormState({ name });
	const { error } = getFieldState(name, formState);

	return (
		<FormField
			control={control}
			name={name}
			render={({ field }) => (
				<motion.div layout transition={layoutTransition} className="w-full">
					<FormItem>
						{label && (
							<FormLabel htmlFor={name}>
								{label}
								{required && <RequiredAsterisk />}
							</FormLabel>
						)}
						<FormControl>{render(field)}</FormControl>
						{description && <FormDescription>{description}</FormDescription>}
						<AnimatedFormMessage hasError={!!error} />
					</FormItem>
				</motion.div>
			)}
		/>
	);
}

/* ----------------------------- Input Variants ----------------------------- */

export function InputFormField<T extends FieldValues>(
  props: BaseFormFieldProps<T> & { placeholder?: string; disabled?: boolean; append?: ReactNode }
) {
  const { placeholder, disabled, append, name } = props;

  return (
    <CommonFormField
      {...props}
      render={(field) => {
        if (append) {
          return (
            <InputGroup>
              <InputGroupInput
                {...field}
                id={name}
                placeholder={placeholder}
                disabled={disabled}
              />
              <InputGroupButton>
                {append}
              </InputGroupButton>
            </InputGroup>
          );
        } else {
          return (
            <Input
              {...field}
              id={name}
              placeholder={placeholder}
              disabled={disabled}
            />
          );
        }
      }}
    />
  );
}

export function NumberFormField<T extends FieldValues>(
  props: BaseFormFieldProps<T> & { placeholder?: string; disabled?: boolean; min?: number; max?: number; step?: number }
) {
  return (
    <CommonFormField
      {...props}
      render={(field) => (
        <Input
          {...field}
          id={props.name}
          type="number"
          placeholder={props.placeholder}
          disabled={props.disabled}
          min={props.min}
          max={props.max}
          step={props.step}
          // onChange needed to ensure number value parsing
          onChange={e => {
            const value = e.target.value === "" ? "" : Number(e.target.value);
            field.onChange(value);
          }}
        />
      )}
    />
  );
}


export function TextareaFormField<T extends FieldValues>(
	props: BaseFormFieldProps<T> & { placeholder?: string; rows?: number }
) {
	return (
		<CommonFormField
			{...props}
			render={(field) => (
				<Textarea
					{...field}
          id={props.name}
					placeholder={props.placeholder}
					rows={props.rows}
				/>
			)}
		/>
	);
}
