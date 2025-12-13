import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ReceiptParticipant } from "@/types/data";

export default function ParticipantAvatar({ participant }: { participant: ReceiptParticipant }) {
  // If participant has a user object, use their photo and name
  const user = participant.user;
  const name = user?.name || "Friend";
  const photoUrl = user?.photo_url || undefined;

  // AvatarFallback can show initials or a default fallback
  function getInitials(name: string) {
    return name
      .split(" ")
      .map(part => part[0]?.toUpperCase())
      .slice(0, 2)
      .join("");
  }

  return (
    <Avatar>
      <AvatarImage src={photoUrl} alt={name} />
      <AvatarFallback>{getInitials(name)}</AvatarFallback>
    </Avatar>
  );
}