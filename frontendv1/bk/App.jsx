import { useEffect, useState, useMemo, useRef } from "react";
import { fetchToken, fetchDashboard } from "./api";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function App() {
  // -----------------------------
  // 1. STATE HOOKS
  // -----------------------------
  const [token, setToken] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [productQuery, setProductQuery] = useState("");
  const [userQuery, setUserQuery] = useState("");

  // -----------------------------
  // 2. DERIVED VALUES (useMemo)
  // -----------------------------
  const products = dashboard?.products || [];
  const users = dashboard?.users || [];

  const topBrands = useMemo(() => {
    const totals = {};
    products.forEach((p) => {
      if (!p.brand) return;
      totals[p.brand] = (totals[p.brand] || 0) + p.price;
    });
    return Object.entries(totals)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([brand, total]) => ({ brand, total }));
  }, [products]);

  const topRated = useMemo(() => {
    return [...products]
      .sort((a, b) => b.rating - a.rating)
      .slice(0, 10);
  }, [products]);

  const topCities = useMemo(() => {
    const counts = {};
    users.forEach((u) => {
      const city = u.address?.city || "Unknown";
      counts[city] = (counts[city] || 0) + 1;
    });
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([city, count]) => ({ city, count }));
  }, [users]);

  const priceChartData = useMemo(() => {
    return {
      labels: products.map((p) => p.title),
      datasets: [
        {
          label: "Product Price",
          data: products.map((p) => p.price),
          backgroundColor: "rgba(59, 130, 246, 0.7)",
        },
      ],
    };
  }, [products]);

  const priceChartOptions = {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: "#9ca3af" } },
      y: { ticks: { color: "#9ca3af" } },
    },
  };

  // -----------------------------
  // 3. FUNCTIONS
  // -----------------------------
  const loadDashboard = async (qProducts = "", qUsers = "") => {
    try {
      setLoading(true);

      const tokenData = await fetchToken();
      setToken(tokenData.accessToken);

      const dashData = await fetchDashboard(qProducts, qUsers);
      setDashboard(dashData);

      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load dashboard");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadDashboard(productQuery, userQuery);
  };

  // -----------------------------
  // 4. EFFECT (Strict Mode Safe)
  // -----------------------------
  const didRun = useRef(false);

  useEffect(() => {
    if (didRun.current) return; // prevents Strict Mode double-run
    didRun.current = true;

    loadDashboard();
  }, []);

  // -----------------------------
  // 5. RENDER
  // -----------------------------
  if (loading && !dashboard) return <div className="app">Loading dashboard…</div>;
  if (error) return <div className="app error">{error}</div>;

  return (
    <div className="app">
      <header className="header">
        <h1>DummyJSON Dashboard (Flask + React)</h1>
        <div className="token-box">
          <span>Backend Token: </span>
          <code>{token ? token.slice(0, 25) + "..." : "N/A"}</code>
        </div>
      </header>

      <form className="filters" onSubmit={handleSearch}>
        <div className="filter-field">
          <label>Product search</label>
          <input
            value={productQuery}
            onChange={(e) => setProductQuery(e.target.value)}
            placeholder="Search products..."
          />
        </div>

        <div className="filter-field">
          <label>User search</label>
          <input
            value={userQuery}
            onChange={(e) => setUserQuery(e.target.value)}
            placeholder="Search users..."
          />
        </div>

        <button type="submit">Apply</button>
      </form>

      <section className="summary">
        <div className="card">
          <h2>Products</h2>
          <p>{dashboard.summary.totalProducts}</p>
        </div>
        <div className="card">
          <h2>Users</h2>
          <p>{dashboard.summary.totalUsers}</p>
        </div>
      </section>

      <section className="stats-grid">
        <div className="panel">
          <h2>Top 5 Most Expensive Brands</h2>
          <ul>
            {topBrands.map((b, i) => (
              <li key={i}>
                <span>{b.brand}</span>
                <span>${b.total}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h2>Top 10 Highest Rated Products</h2>
          <ul>
            {topRated.map((p) => (
              <li key={p.id}>
                <span>{p.title}</span>
                <span>⭐ {p.rating}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h2>Top 5 Cities (Users)</h2>
          <ul>
            {topCities.map((c, i) => (
              <li key={i}>
                <span>{c.city}</span>
                <span>{c.count} users</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Product Price Distribution</h2>
          <Bar data={priceChartData} options={priceChartOptions} />
        </div>

        <div className="panel">
          <h2>Products</h2>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Brand</th>
                <th>Price</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id}>
                  <td>{p.title}</td>
                  <td>{p.brand}</td>
                  <td>${p.price}</td>
                  <td>{p.rating}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="panel">
          <h2>Users</h2>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Age</th>
                <th>City</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.firstName} {u.lastName}</td>
                  <td>{u.username}</td>
                  <td>{u.age}</td>
                  <td>{u.address?.city}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default App;
