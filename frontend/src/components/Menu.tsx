import { useLocation, Link } from "react-router-dom";

const Menu = () => {
  const location = useLocation();

  return (
    <div className="fixed top-0 left-0 w-full bg-color-bg border-b border-color-2/25 z-[100]">
      <div className="container flex items-center justify-between h-full menu-footer-setup">
        <div className="flex flex-row gap-4 items-center">
          <Link to="/" className="flex items-center gap-4">
            <h1 className="text-title-1 text-color-1 hover:opacity-50 transition-opacity">
              LASTRO
            </h1>
          </Link>

          <div className="text-note-2 hidden md:flex flex-col uppercase gap-0.5">
            <span>A Música Portuguesa</span>
            <span>A Gostar Dela Própria</span>
          </div>
        </div>

        <nav className="flex flex-row items-end gap-2 text-body-2 uppercase">
          <Link
            to="/explorar"
            className={`p-2 transition-opacity ${
              location.pathname === "/explorar"
                ? "text-color-1"
                : "text-color-1/50 hover:text-color-1"
            }`}
          >
            Explorar
          </Link>

          <Link
            to="/sobre"
            className={`p-2 pr-0 transition-opacity ${
              location.pathname === "/sobre"
                ? "text-color-1"
                : "text-color-1/50 hover:text-color-1"
            }`}
          >
            Sobre
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default Menu;
