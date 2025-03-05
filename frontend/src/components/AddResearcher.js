import React, { useState } from "react";
import axios from "axios";

const AddResearcher = ({ onResearcherAdded }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [expertise, setExpertise] = useState("");
  const [institution, setInstitution] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const userData = {
      username,
      password,
      researcher: { expertise, institution },  // Envoie aussi expertise et institution ici
    };
  
    // Vérifier les données avant d'envoyer
    console.log("📤 Données envoyées à l'API :", userData);
  
    try {
      const userResponse = await axios.post("http://127.0.0.1:8000/api/users/", userData);
  
      setMessage("✅ Chercheur ajouté avec succès !");
      setUsername("");
      setPassword("");
      setExpertise("");
      setInstitution("");
  
      if (onResearcherAdded) {
        onResearcherAdded(); // Mise à jour de la liste
      }
    } catch (error) {
      setMessage("❌ Erreur lors de l'ajout du chercheur.");
      console.error(error);
    }
  };

  return (
    <div>
      <h2>➕ Ajouter un Chercheur</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nom d'utilisateur"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Domaine d'expertise"
          value={expertise}
          onChange={(e) => setExpertise(e.target.value)}
        />
        <input
          type="text"
          placeholder="Institution"
          value={institution}
          onChange={(e) => setInstitution(e.target.value)}
        />
        <button type="submit">Créer Chercheur</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddResearcher;