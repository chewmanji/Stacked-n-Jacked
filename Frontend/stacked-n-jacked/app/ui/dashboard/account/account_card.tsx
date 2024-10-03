import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { EditProfileForm } from "./edit-profile-form";
import { User } from "@/app/lib/definitions";
import { fetchCurrentUser } from "@/app/lib/data";

export default async function AccountCard() {
  const user: User = await fetchCurrentUser();
  return (
    <Card>
      <CardHeader>
        <CardTitle>Your account</CardTitle>
        <CardDescription>Edit your profile here</CardDescription>
      </CardHeader>
      <CardContent>
        <EditProfileForm user={user} />
      </CardContent>
      <CardFooter className="flex justify-between"></CardFooter>
    </Card>
  );
}
