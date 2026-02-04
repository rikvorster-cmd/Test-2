import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function Factories() {
  const [factories, setFactories] = useState([]);
  const [form, setForm] = useState({ factory_code: '', name: '', audit_score: '', risk_score: '' });

  const load = async () => {
    const data = await apiGet('/factories');
    setFactories(data);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/factories', {
      ...form,
      audit_score: form.audit_score ? Number(form.audit_score) : null,
      risk_score: form.risk_score ? Number(form.risk_score) : null,
    });
    setForm({ factory_code: '', name: '', audit_score: '', risk_score: '' });
    load();
  };

  return (
    <Layout title="Factories">
      <div className="card">
        <h3>Create Factory</h3>
        <form onSubmit={submit}>
          <input
            placeholder="Code"
            value={form.factory_code}
            onChange={(e) => setForm({ ...form, factory_code: e.target.value })}
          />
          <input
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <input
            placeholder="Audit score"
            value={form.audit_score}
            onChange={(e) => setForm({ ...form, audit_score: e.target.value })}
          />
          <input
            placeholder="Risk score"
            value={form.risk_score}
            onChange={(e) => setForm({ ...form, risk_score: e.target.value })}
          />
          <button type="submit">Create</button>
        </form>
      </div>
      <div className="card">
        <h3>Factories list</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Code</th>
              <th>Name</th>
              <th>Audit</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {factories.map((factory) => (
              <tr key={factory.factory_id}>
                <td>{factory.factory_id}</td>
                <td>{factory.factory_code}</td>
                <td>{factory.name}</td>
                <td>{factory.audit_score ?? '-'}</td>
                <td>{factory.risk_score ?? '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
