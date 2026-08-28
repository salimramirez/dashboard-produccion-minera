import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

const API = "http://localhost:8000/api";

function App() {
  const [resumen, setResumen] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/resumen`)
      .then((r) => {
        if (!r.ok) throw new Error("No se pudo cargar la producción");
        return r.json();
      })
      .then(setResumen)
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Producción minera 2025</h1>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={resumen}>
          <XAxis dataKey="mes" />
          <YAxis yAxisId="oro" />
          <YAxis yAxisId="plata" orientation="right" />
          <Tooltip />
          <Legend />
          <Bar yAxisId="oro" dataKey="oro_oz" fill="#d4af37" name="Oro (oz)" />
          <Bar yAxisId="plata" dataKey="plata_oz" fill="#9ca3af" name="Plata (oz)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;
