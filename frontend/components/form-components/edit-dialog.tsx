import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

interface EditDialogProps {
    title: string;
    description?: string;
    open: boolean;
    onOpenChange: (open: boolean) => void;
    formComponent: React.ReactNode; // <-- Accepts the whole JSX element
    maxWidth?: string;
  }

export const EditDialog = (props: EditDialogProps) => {
    return (
        <Dialog open={props.open} onOpenChange={props.onOpenChange}>
            <DialogContent className={`sm:max-w-[425px] ${props.maxWidth || ''}`}>
                <DialogHeader>
                    <DialogTitle>{props.title}</DialogTitle>
                    <DialogDescription>{props.description}</DialogDescription>
                </DialogHeader>
                {props.formComponent}
            </DialogContent>
        </Dialog>
    )
}