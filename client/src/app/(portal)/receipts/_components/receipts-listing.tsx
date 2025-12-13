import { fetchReceiptsList } from "@/actions/receipts";
import PageLayout from "@/components/layout/page-layout";
import ReceiptCard from "./receipt-card";

export default async function ReceiptsListing() {
  const result = await fetchReceiptsList();

  if (!result.success) {
    // TODO: receipts error
    return null
  }

  const receipts = result.data;
  return (
    <PageLayout>
      {receipts.map(receipt => <ReceiptCard data={receipt} key={receipt.id} />)}
    </PageLayout>
  );
}
