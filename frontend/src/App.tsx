import { Link} from "react-router";
import "./App.css";

function App() {
  return (
    <>
      <section id="center">
        <div>
          <h1>HabiTrack</h1>
          <p>A tidy place to track your habits.</p>
        </div>
        <div>
          <Link to="/login" className="counter">
            Log In
          </Link>
          or 
          <Link
            to="/sign-up"
            className="counter"
          >
            Sign Up
          </Link>
        </div>
      </section>
    </>
  );
}

export default App;
