import { Breadcrumb, BreadcrumbItem, BreadcrumbLink } from "@chakra-ui/react";
import { Link, useLocation } from "react-router-dom";

import styles from "./main.module.scss";

function Navigation() {
  const location = useLocation();
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
      <BreadcrumbItem
        isCurrentPage={location.pathname === "/visited-locations"}
      >
        <BreadcrumbLink as={Link} to="/visited-locations">
          Точки локации, посещенные животным
        </BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbItem isCurrentPage={location.pathname === "/account"}>
        <BreadcrumbLink as={Link} to="/account">
          Аккаунт
        </BreadcrumbLink>
      </BreadcrumbItem>
    </Breadcrumb>
  );
}

export default Navigation;
