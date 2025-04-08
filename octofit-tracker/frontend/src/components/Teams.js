import React, { useEffect, useState } from 'react';
import { getToken } from '../utils/auth';

function Teams() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/teams/', {
      headers: {
        'Authorization': getToken(),
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => setTeams(data))
      .catch(error => console.error('Error fetching teams:', error));
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Teams</h1>
      <ul className="list-group">
        {teams.map(team => (
          <li key={team._id} className="list-group-item">{team.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Teams;
