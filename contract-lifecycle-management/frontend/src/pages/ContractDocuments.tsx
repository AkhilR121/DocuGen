import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { contractsAPI } from '../services/api';
import { Document } from '../types';

function ContractDocuments(): JSX.Element {
  const { contractId } = useParams<{ contractId: string }>();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDocuments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contractId]);

  const fetchDocuments = async (): Promise<void> => {
    if (!contractId) return;

    try {
      setLoading(true);
      const response = await contractsAPI.getDocuments(contractId);
      setDocuments(response.data);
      setError(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError('Failed to load documents: ' + errorMessage);
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading documents...</div>;
  }

  if (error) {
    return (
      <div>
        <div className="breadcrumb">
          <Link to="/" className="link">← Back to Contracts</Link>
        </div>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div>
      <div className="breadcrumb">
        <Link to="/" className="link">← Back to Contracts</Link>
      </div>

      <div className="card">
        <h2>Contract Documents - Contract ID: {contractId}</h2>
        {documents.length === 0 ? (
          <p style={{ marginTop: '20px', color: '#7f8c8d' }}>
            No documents found for this contract. Create one using the API.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Document ID</th>
                <th>Customer Name</th>
                <th>Sites Count</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Files</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((document) => (
                <tr key={document.document_id}>
                  <td>
                    <Link
                      to={`/contracts/${contractId}/documents/${document.document_id}`}
                      className="link"
                    >
                      {document.document_id}
                    </Link>
                  </td>
                  <td>{document.customer_name}</td>
                  <td>{document.sites_count}</td>
                  <td>
                    <span style={{
                      color: document.is_active ? '#27ae60' : '#e74c3c',
                      fontWeight: '500'
                    }}>
                      {document.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>{document.created_at ? new Date(document.created_at).toLocaleString() : 'N/A'}</td>
                  <td>
                    {document.files && document.files.length > 0 ? (
                      <span>{document.files.length} files</span>
                    ) : (
                      <span style={{ color: '#95a5a6' }}>No files</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default ContractDocuments;
