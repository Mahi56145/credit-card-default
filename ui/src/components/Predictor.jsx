import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { RadialBarChart, RadialBar, Legend } from "recharts";

function ResultCard({ result }) {
  if (!result) return null;

  const value = Math.round((result.probability_of_default || 0) * 1000) / 10;
  const color = result.probability_of_default > 0.5 ? "#ef4444" : "#10b981";
  const display = `Probability: ${value}%\nLabel: ${result.predicted_label}`;

  const chartData = [{ name: "default", value: value }];

  return (
    <div className="mt-6 grid gap-4 sm:grid-cols-2 items-center">
      <div className="p-4 bg-white rounded-xl shadow">
        <div className="text-sm text-slate-500 mb-2">Prediction</div>
        <div className="text-lg font-semibold">{display}</div>
        <div className="mt-3 text-xs text-slate-500">Interpretation: {value > 50 ? "High risk" : "Low risk"}</div>
      </div>

      <div className="p-4 bg-white rounded-xl shadow flex items-center justify-center">
        <RadialBarChart width={220} height={150} cx="50%" cy="50%" innerRadius="20%" outerRadius="100%" barSize={18} data={chartData}>
          <RadialBar minAngle={15} background clockWise dataKey="value" cornerRadius={10} fill={color} />
          <Legend
            iconSize={0}
            layout="vertical"
            verticalAlign="bottom"
            wrapperStyle={{ top: 0, left: 0, lineHeight: "24px" }}
          />
        </RadialBarChart>
      </div>
    </div>
  );
}

export default function Predictor() {
  const [form, setForm] = useState({ Income: 50000, Age: 35, Loan: 4000, Loan_to_Income: 0.08 });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function submit() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const resp = await axios.post("/predict", {
        Income: Number(form.Income),
        Age: Number(form.Age),
        Loan: Number(form.Loan),
        Loan_to_Income: Number(form.Loan_to_Income)
      });
      setResult(resp.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <motion.div initial={{ y: 8, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
        <div className="bg-white p-6 rounded-2xl shadow">
          <div className="text-sm text-slate-500">Quick Inputs</div>

          <label className="block mt-4 text-sm font-medium text-slate-700">Income</label>
          <input
            className="mt-1 p-3 border rounded-lg w-full"
            type="number"
            value={form.Income}
            onChange={(e) => setForm({ ...form, Income: e.target.value })}
          />

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block mt-4 text-sm font-medium text-slate-700">Age</label>
              <input
                className="mt-1 p-3 border rounded-lg w-full"
                type="number"
                value={form.Age}
                onChange={(e) => setForm({ ...form, Age: e.target.value })}
              />
            </div>

            <div>
              <label className="block mt-4 text-sm font-medium text-slate-700">Loan</label>
              <input
                className="mt-1 p-3 border rounded-lg w-full"
                type="number"
                value={form.Loan}
                onChange={(e) => setForm({ ...form, Loan: e.target.value })}
              />
            </div>
          </div>

          <label className="block mt-4 text-sm font-medium text-slate-700">Loan to Income</label>
          <input
            className="mt-1 p-3 border rounded-lg w-full"
            type="number"
            step="0.0001"
            value={form.Loan_to_Income}
            onChange={(e) => setForm({ ...form, Loan_to_Income: e.target.value })}
          />

          <div className="flex items-center gap-3 mt-6">
            <button
              onClick={submit}
              className={`px-4 py-2 rounded-lg font-semibold ${loading ? "bg-slate-400" : "bg-brand-500 text-white"}`}
              disabled={loading}
            >
              {loading ? "Predicting…" : "Predict"}
            </button>

            <button
              onClick={() => {
                setForm({ Income: 50000, Age: 35, Loan: 4000, Loan_to_Income: 0.08 });
                setResult(null);
                setError("");
              }}
              className="px-4 py-2 rounded-lg border"
            >
              Reset
            </button>
          </div>

          {error && <div className="mt-4 text-sm text-red-600">{error}</div>}
        </div>
      </motion.div>

      <motion.div initial={{ y: 12, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
        <div className="bg-gradient-to-b from-white to-slate-50 p-6 rounded-2xl shadow">
          <div className="text-sm text-slate-500 mb-2">Results</div>
          {!result && <div className="text-sm text-slate-400">No prediction yet — enter values and hit predict.</div>}
          {result && <ResultCard result={result} />}
          <div className="text-xs text-slate-400 mt-4">
            Tip: try a large loan + low income to see higher risk.
          </div>
        </div>
      </motion.div>
    </div>
  );
}
