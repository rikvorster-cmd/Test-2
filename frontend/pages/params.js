import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function Params() {
  const [params, setParams] = useState([]);
  const [form, setForm] = useState({ param_code: '', param_name: '', value_type: '', uom_default: '' });

  const load = async () => {
    setParams(await apiGet('/params'));
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/params', form);
    setForm({ param_code: '', param_name: '', value_type: '', uom_default: '' });
    load();
  };

  return (
    <Layout title="Parameters Catalog">
      <div className="card">
        <h3>Create parameter</h3>
        <form onSubmit={submit}>
          <input
            placeholder="Code"
            value={form.param_code}
            onChange={(e) => setForm({ ...form, param_code: e.target.value })}
          />
          <input
            placeholder="Name"
            value={form.param_name}
            onChange={(e) => setForm({ ...form, param_name: e.target.value })}
          />
          <input
            placeholder="Value type"
            value={form.value_type}
            onChange={(e) => setForm({ ...form, value_type: e.target.value })}
          />
          <input
            placeholder="UOM"
            value={form.uom_default}
            onChange={(e) => setForm({ ...form, uom_default: e.target.value })}
          />
          <button type="submit">Create</button>
        </form>
      </div>
      <div className="card">
        <h3>Parameters</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Code</th>
              <th>Name</th>
              <th>Type</th>
              <th>UOM</th>
            </tr>
          </thead>
          <tbody>
            {params.map((param) => (
              <tr key={param.param_id}>
                <td>{param.param_id}</td>
                <td>{param.param_code}</td>
                <td>{param.param_name}</td>
                <td>{param.value_type}</td>
                <td>{param.uom_default || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
