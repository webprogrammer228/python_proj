import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from "./pages/login";
import Registration from "./pages/registration";
import PrivateRoute from "./utils/PrivateRoute";
import Main from "./pages/main";
import Account from "./pages/account";
import Locations from "./pages/locations";
import AnimalTypes from "./pages/animalTypes";
import Animal from "./pages/animal";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route element={<PrivateRoute />}>
            <Route element={<Main />} path="/main" />
            <Route element={<Account />} path="/account" />
            <Route element={<Locations />} path="/locations" />
            <Route element={<AnimalTypes />} path="/animal-types" />
            <Route element={<Animal />} path="/animal" />
          </Route>
          <Route path="/" element={<Login />} />
          <Route path="/registration" element={<Registration />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
