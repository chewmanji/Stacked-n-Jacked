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
import { ChangeEmailFormSchema } from "@/app/lib/definitions";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { ButtonLoading } from "@/app/ui/button-loading";
import { useRouter } from "next/navigation";

export function EditEmailDialog() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [open, setOpen] = useState(false);
  const { toast } = useToast();
  const router = useRouter();
  const form = useForm<z.infer<typeof ChangeEmailFormSchema>>({
    resolver: zodResolver(ChangeEmailFormSchema),
    defaultValues: {},
  });

  async function onSubmit(values: z.infer<typeof ChangeEmailFormSchema>) {
    if (!isSubmitting) {
      setIsSubmitting(true);

      const message = await editProfile({
        email: values.email,
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
          description: "You have successfully changed your email!",
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
        <Button variant="outline">Change email</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] w-11/12">
        <DialogHeader>
          <DialogTitle>Change email</DialogTitle>
          <DialogDescription>
            Change your email here. Click save when you&apos;re done. After
            saving changes you will have to log in again with new credentials.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>New email</FormLabel>

                  <FormControl>
                    <Input placeholder="New email" {...field} type="email" />
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
