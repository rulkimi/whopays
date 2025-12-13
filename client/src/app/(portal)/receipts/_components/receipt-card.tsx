import ParticipantAvatar from "@/components/participant-avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDate } from "@/lib/date";
import { formatPrice } from "@/lib/number";
import { Receipt } from "@/types/data";
import { Users, User, Calendar } from "lucide-react";

export default function ReceiptCard({
  data
}: {
  data: Receipt
}) {
  return (
    <Card className="gap-0">
      <CardHeader>
        <div className="flex flex-col sm:flex-row justify-between gap-2">
          <CardTitle>{data.restaurant_name}</CardTitle>
          <div className="flex justify-between gap-2">
            <span>{formatPrice(data.total_amount)}</span>
            <div className="flex sm:hidden items-center gap-2 text-muted-foreground">
              <User className="w-4 h-4" />
              <span>{data.participants.length}</span>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex justify-between gap-2">
        <div className="hidden sm:flex items-center gap-2 text-muted-foreground">
          <Calendar className="w-4 h-4" />
          <span>{formatDate(data.created_at)}</span>
        </div>
        <Participants participants={data.participants} />
      </CardContent>
    </Card>
  )
}

function Participants({ participants }: { participants: Receipt["participants"] }) {
  if (!participants || participants.length === 0) {
    return (
      <div className="hidden sm:flex items-center gap-2 text-muted-foreground">
        <User className="w-4 h-4" />
        <span>No participants</span>
      </div>
    );
  }

  return (
    <div className="hidden sm:flex items-center gap-2">
      <Users className="w-4 h-4" />
      <span className="font-medium">{participants.length}</span>
      <div className="flex flex-row gap-1">
        {participants.map(participant => (
          <ParticipantAvatar participant={participant} key={participant.id} />
        ))}
      </div>
    </div>
  );
}