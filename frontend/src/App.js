import React, { useState } from "react";
import ResearchersList from "./components/ResearchersList";
import AddResearcher from "./components/AddResearcher";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [refresh, setRefresh] = useState(false);

  return (
    <div>
      <h1>🧑‍🔬 Réseau des Chercheurs</h1>
      <AddResearcher onResearcherAdded={() => setRefresh(!refresh)} />
      <ResearchersList key={refresh} />
    </div>
  );
}

export default App;