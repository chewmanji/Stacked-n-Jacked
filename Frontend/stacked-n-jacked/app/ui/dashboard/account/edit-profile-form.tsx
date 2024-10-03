"use client";

import { editProfile } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectItem,
  SelectContent,
} from "@/components/ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { EditProfileFormSchema, User } from "@/app/lib/definitions";
import { zodResolver } from "@hookform/resolvers/zod";
import { Gender } from "@/app/lib/definitions";
import { CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { ButtonLoading } from "@/app/ui/button-loading";

export function EditProfileForm({ user }: { user: User }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();
  const form = useForm<z.infer<typeof EditProfileFormSchema>>({
    resolver: zodResolver(EditProfileFormSchema),
    defaultValues: {
      email: user.email,
      birthDate: user.birthDate,
      gender: user.gender.toString(),
    },
  });

  async function onSubmit(values: z.infer<typeof EditProfileFormSchema>) {
    if (!isSubmitting) {
      setIsSubmitting(true);
      const genderData = z.coerce.number().parse(values.gender);
      const message = await editProfile({
        email: values.email,
        newPassword: values.newPassword,
        birthDate: values.birthDate,
        gender: genderData,
      });
      if (message) {
        toast({
          title: "Error",
          variant: "destructive",
          description: message.message,
        });
      } else {
        toast({
          title: "Success",
          description: "You have successfully registered!",
          duration: 2000,
        });
      }
    }

    setIsSubmitting(false);
  }
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="New email" {...field} />
              </FormControl>
              <FormDescription>Set new email</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        ></FormField>
        <FormField
          control={form.control}
          name="newPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input placeholder="New password" {...field} type="password" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        ></FormField>
        <FormField
          control={form.control}
          name="confirmPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Confirm password</FormLabel>

              <FormControl>
                <Input placeholder="New password" {...field} type="password" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        ></FormField>
        <FormField
          control={form.control}
          name="birthDate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Birth date</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant={"outline"}
                      className={cn(
                        "w-full pl-3 text-left font-normal",
                        !field.value && "text-muted-foreground"
                      )}
                    >
                      {field.value ? (
                        format(field.value, "PPP")
                      ) : (
                        <span>Pick a date</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-full" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    disabled={(date) =>
                      date > new Date() || date < new Date("1900-01-01")
                    }
                    captionLayout="dropdown-buttons"
                    fromYear={1900}
                    toYear={new Date().getFullYear()}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        ></FormField>
        <FormField
          control={form.control}
          name="gender"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Gender</FormLabel>
              <Select
                onValueChange={field.onChange}
                defaultValue={user.gender.toString()}
              >
                <FormControl>
                  <SelectTrigger className="col-span-4">
                    <SelectValue placeholder="Gender" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {Object.entries(Gender).map(([key, value]) => {
                    if (isNaN(Number(key))) {
                      return (
                        <SelectItem key={key} value={`${value}`}>
                          {key}
                        </SelectItem>
                      );
                    }
                  })}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        ></FormField>
        {isSubmitting ? (
          <ButtonLoading />
        ) : (
          <Button type="submit">Update profile</Button>
        )}
      </form>
    </Form>
  );
}