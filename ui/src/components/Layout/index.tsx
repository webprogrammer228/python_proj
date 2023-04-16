import Navigation from "../Navigation";
import styles from "./main.module.scss";

interface ILayoutProps {
  children: React.ReactNode | React.ReactNode[];
}

function Layout({ children }: ILayoutProps) {
  return (
    <div className={styles.block}>
      <Navigation />
      {children}
    </div>
  );
}

export default Layout;
