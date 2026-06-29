import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  return (
    <div className="min-h-screen bg-brand-bg text-white">
      <Navbar />
      <Home />
    </div>
  );
}

export default App;