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
          <button type="button" className="counter">
            Log In
          </button>
          or 
          <button
            type="button"
            className="counter"
          >
            Sign Up
          </button>
        </div>
      </section>
    </>
  );
}

export default App;
