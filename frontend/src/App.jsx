import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import "./App.css";

const API = "http://localhost:8000/api";

const usd = (n) =>
  n.toLocaleString("es-PE", { style: "currency", currency: "USD", maximumFractionDigits: 2 });
const oz = (n) => n.toLocaleString("es-PE");

function App() {
  const [minas, setMinas] = useState([]);
  const [minaSeleccionada, setMinaSeleccionada] = useState("");
  const [resumen, setResumen] = useState([]);
  const [valorizacion, setValorizacion] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/minas`)
      .then((r) => r.json())
      .then(setMinas)
      .catch(() => setMinas([]));
  }, []);

  useEffect(() => {
    const query = minaSeleccionada ? `?mina_id=${minaSeleccionada}` : "";
    setCargando(true);
    setError(null);

    Promise.all([fetch(`${API}/resumen${query}`), fetch(`${API}/valorizacion${query}`)])
      .then(async ([r1, r2]) => {
        if (!r1.ok || !r2.ok) throw new Error("No se pudieron cargar los datos");
        return [await r1.json(), await r2.json()];
      })
      .then(([datosResumen, datosValorizacion]) => {
        setResumen(datosResumen);
        setValorizacion(datosValorizacion);
      })
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }, [minaSeleccionada]);

  return (
    <div>
      <h1>Producción minera 2025</h1>

      <div className="filtro">
        <label htmlFor="mina">Mina: </label>
        <select
          id="mina"
          value={minaSeleccionada}
          onChange={(e) => setMinaSeleccionada(e.target.value)}
        >
          <option value="">Todas las minas</option>
          {minas.map((m) => (
            <option key={m.id} value={m.id}>
              {m.nombre} ({m.region})
            </option>
          ))}
        </select>
      </div>

      {cargando && <p>Cargando...</p>}
      {error && <p>Error: {error}</p>}

      {!cargando && !error && valorizacion && (
        <>
          <p className="origen">
            {valorizacion.origen_precios === "api"
              ? "Precios en vivo de GoldAPI"
              : "Precios de respaldo (GoldAPI no disponible)"}
          </p>

          <div className="tarjetas">
            <div className="tarjeta">
              <h2>Valor total</h2>
              <p className="monto">{usd(valorizacion.total_usd)}</p>
            </div>
            <div className="tarjeta">
              <h2>Oro</h2>
              <p className="monto">{usd(valorizacion.oro.valor_usd)}</p>
              <p>{oz(valorizacion.oro.onzas)} oz a {usd(valorizacion.oro.precio_usd_oz)} por oz</p>
            </div>
            <div className="tarjeta">
              <h2>Plata</h2>
              <p className="monto">{usd(valorizacion.plata.valor_usd)}</p>
              <p>{oz(valorizacion.plata.onzas)} oz a {usd(valorizacion.plata.precio_usd_oz)} por oz</p>
            </div>
          </div>

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
        </>
      )}
    </div>
  );
}

export default App;
