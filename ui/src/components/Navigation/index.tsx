import { Breadcrumb, BreadcrumbItem, BreadcrumbLink } from "@chakra-ui/react";
import { Link, useLocation } from "react-router-dom";
import Cookies from "js-cookie";
import styles from "./main.module.scss";

function Navigation() {
  const location = useLocation();
  const logoutHandler = () => {
    Cookies.remove("id");
    Cookies.remove("logged");
  };
  return (
    <Breadcrumb className={styles.navigation}>
      <BreadcrumbItem isCurrentPage={location.pathname === "/locations"}>
        <BreadcrumbLink as={Link} to="/locations">
          Точка локации животных
        </BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbItem isCurrentPage={location.pathname === "/animal-types"}>
        <BreadcrumbLink as={Link} to="/animal-types">
          Типы животных
        </BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbItem isCurrentPage={location.pathname === "/animal"}>
        <BreadcrumbLink as={Link} to="/animal">
          Животное
        </BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbItem isCurrentPage={location.pathname === "/account"}>
        <BreadcrumbLink as={Link} to="/account">
          Аккаунт
        </BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbItem>
        <BreadcrumbLink as={Link} to="/" onClick={logoutHandler}>
          Выход
        </BreadcrumbLink>
      </BreadcrumbItem>
    </Breadcrumb>
  );
}

export default Navigation;
