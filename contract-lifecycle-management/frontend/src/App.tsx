import { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const ContractsList = lazy(() => import('./pages/ContractsList'));
const ContractDocuments = lazy(() => import('./pages/ContractDocuments'));
const DocumentViewer = lazy(() => import('./pages/DocumentViewer'));

function App(): JSX.Element {
  return (
    <Router>
      <div className="container">
        <div className="header">
          <h1>Contract Lifecycle Management</h1>
          <p>Initial Implementation - React + FastAPI + Oracle + Redis</p>
        </div>
        <Suspense fallback={<div className="loading">Loading...</div>}>
          <Routes>
            <Route path="/" element={<ContractsList />} />
            <Route path="/contracts/:contractId/documents" element={<ContractDocuments />} />
            <Route path="/contracts/:contractId/documents/:documentId" element={<DocumentViewer />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  );
}

export default App;
