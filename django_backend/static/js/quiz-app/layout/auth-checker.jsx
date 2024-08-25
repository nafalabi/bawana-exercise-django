import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogFooter,
  DialogHeader,
} from "@/components/ui/dialog";

const checkLoggedIn = () => {
  return window.isLoggedIn
};

const AuthChecker = () => {
  const [showWarning, setShowWarning] = useState(false);

  useEffect(() => {
    const isLoggedIn = checkLoggedIn();
    setShowWarning(!isLoggedIn);
  }, []);

  return (
    <Dialog open={showWarning}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Attention</DialogTitle>
        </DialogHeader>
        <div>
          You are not logged in, please login first to visit this page
        </div>
        <DialogFooter>
          <Button onClick={() => {
            window.location = "/"
          }}>OK</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default AuthChecker;
