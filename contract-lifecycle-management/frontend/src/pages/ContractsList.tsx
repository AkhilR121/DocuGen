import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { contractsAPI } from '../services/api';
import { Contract } from '../types';

function ContractsList(): JSX.Element {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchContracts();
  }, []);

  const fetchContracts = async (): Promise<void> => {
    try {
      setLoading(true);
      const response = await contractsAPI.getAll();
      setContracts(response.data);
      setError(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError('Failed to load contracts: ' + errorMessage);
      console.error('Error fetching contracts:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading contracts...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="card">
      <h2>All Contracts</h2>
      {contracts.length === 0 ? (
        <p style={{ marginTop: '20px', color: '#7f8c8d' }}>
          No contracts found. Create one using the API or import existing data.
        </p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Contract ID</th>
              <th>Template ID</th>
              <th>Customer Name</th>
              <th>City, State</th>
              <th>Contract Period</th>
              <th>Price</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {contracts.map((contract) => (
              <tr key={contract.id}>
                <td>
                  <Link to={`/contracts/${contract.id}/documents`} className="link">
                    {contract.id}
                  </Link>
                </td>
                <td>{contract.template_id}</td>
                <td>{contract.customer_name}</td>
                <td>{contract.city}, {contract.state}</td>
                <td>{contract.start_date} - {contract.end_date}</td>
                <td>{contract.contract_price}</td>
                <td>{contract.created_at ? new Date(contract.created_at).toLocaleDateString() : 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ContractsList;
