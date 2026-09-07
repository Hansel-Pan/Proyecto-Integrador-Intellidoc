import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import Welcome from './pages/Welcome';
import Login from './pages/Login';
import Register from './pages/Register';
import Repositories from './pages/Repositories';
import RepositoryDetail from './pages/RepositoryDetail';
import DocumentDetail from './pages/DocumentDetail';
import Chat from './pages/Chat';
import Dashboard from './pages/Dashboard';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" replace />;
}

function PublicRoute({ children }) {
  const token = localStorage.getItem('access_token');
  return token ? <Navigate to="/repositories" replace /> : children;
}

function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
      <Route path="/" element={<Welcome />} />

      {/* Protected routes with layout */}
      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="repositories" element={<Repositories />} />
        <Route path="repositories/:id" element={<RepositoryDetail />} />
        <Route path="documents/:id" element={<DocumentDetail />} />
        <Route path="chat" element={<Chat />} />
        <Route path="dashboard" element={<Dashboard />} />
      </Route>

      {/* Redirect unknown routes */}
      <Route path="*" element={<Navigate to="/repositories" replace />} />
    </Routes>
  );
}

export default App;