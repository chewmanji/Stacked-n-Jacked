"use client";

import { editProfile } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { ChangePasswordFormSchema } from "@/app/lib/definitions";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { ButtonLoading } from "@/app/ui/button-loading";
import { useRouter } from "next/navigation";

export function EditPasswordDialog() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [open, setOpen] = useState(false);
  const { toast } = useToast();
  const router = useRouter();
  const form = useForm<z.infer<typeof ChangePasswordFormSchema>>({
    resolver: zodResolver(ChangePasswordFormSchema),
    defaultValues: {},
  });

  async function onSubmit(values: z.infer<typeof ChangePasswordFormSchema>) {
    if (!isSubmitting) {
      setIsSubmitting(true);

      const message = await editProfile({
        newPassword: values.newPassword,
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
          description: "You have successfully changed your password!",
          duration: 2000,
        });
      }
    }

    setIsSubmitting(false);
    router.refresh();
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild className="my-3">
        <Button variant="outline">Change password</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] w-11/12">
        <DialogHeader>
          <DialogTitle>Change password</DialogTitle>
          <DialogDescription>
            Change your password here. Click save when you&apos;re done.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <FormField
              control={form.control}
              name="newPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="New password"
                      {...field}
                      type="password"
                    />
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
                    <Input
                      placeholder="New password"
                      {...field}
                      type="password"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            ></FormField>
            <DialogFooter>
              <div className="flex justify-between my-4">
                <DialogClose>
                  <Button variant="secondary">Close</Button>
                </DialogClose>
                {isSubmitting ? (
                  <ButtonLoading />
                ) : (
                  <Button type="submit">Save changes</Button>
                )}
              </div>
              <div className="text-xs mt-2">
                After saving changes you will have to log in again with new
                credentials.
              </div>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
