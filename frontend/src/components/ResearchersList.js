import React, { useState, useEffect } from "react";
import axios from "axios";

const ResearchersList = () => {
  const [researchers, setResearchers] = useState([]); // Liste des chercheurs
  const [search, setSearch] = useState(""); // Texte de recherche

  useEffect(() => {
    fetchResearchers();
  }, [search]); // Rafraîchit la liste lorsqu'on tape dans la barre de recherche

  const fetchResearchers = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/researchers/?search=${search}`
      );
      setResearchers(response.data);
    } catch (error) {
      console.error("Erreur lors de la récupération des chercheurs :", error);
    }
  };

  return (
    <div className="container mt-4">
      <h2>🔬 Liste des Chercheurs</h2>

      {/* Barre de recherche */}
      <input
        type="text"
        placeholder="Rechercher un chercheur..."
        className="form-control my-3"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {/* Affichage des chercheurs */}
      <ul className="list-group">
        {researchers.map((researcher) => (
          <li key={researcher.id} className="list-group-item">
            <strong>{researcher.expertise || "Expertise inconnue"}</strong> -{" "}
            {researcher.institution || "Institution inconnue"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ResearchersList;