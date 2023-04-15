import { Outlet, Navigate } from "react-router-dom";
import auth from "../store/authStore";
import { observer } from "mobx-react";

const PrivateRoute = () => {
  return auth.logged ? <Outlet /> : <Navigate to="/" />;
};

export default observer(PrivateRoute);
