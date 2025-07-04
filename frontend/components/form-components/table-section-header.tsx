import React from 'react'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface TableSectionHeaderProps {
    title:string;
    action_title:string;
    open:boolean;
    onOpenChange: (open: boolean) => void;
    onSuccess: () => void;
    formComponent: React.ReactNode;
    formTitle:string;
    formDescription:string;

}

const TableSectionHeader = (props: TableSectionHeaderProps) => {
  return (



    <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold tracking-tight">{props.title}</h2>
            <Dialog open={props.open} onOpenChange={props.onOpenChange}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="h-2 w-2 md:h-4 md:w-4" />
                  <span className="hidden md:block">{props.action_title}</span>
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>{props.formTitle}</DialogTitle>
                  <DialogDescription>
                    {props.formDescription}
                  </DialogDescription>
                </DialogHeader>
                {props.formComponent}
              </DialogContent>
            </Dialog>
          </div>  
      )
}




export default TableSectionHeader