import React from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

const GenericDialog = ({ buttonText, title, content }) => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button size="sm">{buttonText}</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {/* <DialogDescription> */}
          {/*   This action cannot be undone. This will permanently delete your */}
          {/*   account and remove your data from our servers. */}
          {/* </DialogDescription> */}
        </DialogHeader>
        {content}
      </DialogContent>
    </Dialog>
  );
};

export default GenericDialog;
