import { useState, useEffect } from "react";
import { getToken } from "../actions/auth";

export const useTokenCheck = () => {
  const [hasToken, setHasToken] = useState(false);

  useEffect(() => {
    const checkToken = async () => {
      const token = await getToken();
      setHasToken(!!token);
    };
    checkToken();
  }, []);

  return hasToken;
};
