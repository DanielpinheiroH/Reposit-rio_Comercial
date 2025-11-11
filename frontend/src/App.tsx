import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Dashboard } from "./pages/Dashboard";
import { ConteudosEspeciais } from "./pages/ConteudosEspeciais";
import { PostsShorts } from "./pages/PostsShorts";
import { Colecoes } from "./pages/Colecoes";
import { Metricas } from "./pages/Metricas";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/conteudos-especiais" element={<ConteudosEspeciais />} />
          <Route path="/posts-shorts" element={<PostsShorts />} />
          <Route path="/colecoes" element={<Colecoes />} />
          <Route path="/metricas" element={<Metricas />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
