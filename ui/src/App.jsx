import React from "react";
import Hero from "./components/Hero";
import Predictor from "./components/Predictor";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Hero />
      <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Predictor />
      </main>
      <footer className="text-center py-6 text-sm text-slate-500">
        Credit Card Default Demo — Built with React, Tailwind & FastAPI
      </footer>
    </div>
  );
}
