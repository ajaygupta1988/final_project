import React from "react";
import { createStandaloneToast } from "@chakra-ui/react";

const { toast } = createStandaloneToast();

export const loader = (loading) => {
  React.useEffect(() => {
    if (loading) {
      toast({
        position: "top",
        variant: "subtle",
        title: "Loading data",
        id: "loading",
        status: "loading",
        isClosable: false,
        duration: null,
      });
    } else {
      toast.close("loading");
    }
    return () => toast.close("loading");
  }, [loading]);
};
