import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function Accessories() {
  const [items, setItems] = useState([]);
  const [factories, setFactories] = useState([]);
  const [form, setForm] = useState({ part_number: '', accessory_name: '', accessory_spec: '', factory_id: '' });

  const load = async () => {
    const [list, factoriesData] = await Promise.all([apiGet('/accessories'), apiGet('/factories')]);
    setItems(list);
    setFactories(factoriesData);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/accessories', {
      ...form,
      factory_id: form.factory_id ? Number(form.factory_id) : null,
    });
    setForm({ part_number: '', accessory_name: '', accessory_spec: '', factory_id: '' });
    load();
  };

  return (
    <Layout title="Accessories">
      <div className="card">
        <h3>Create accessory</h3>
        <form onSubmit={submit}>
          <input
            placeholder="Part number"
            value={form.part_number}
            onChange={(e) => setForm({ ...form, part_number: e.target.value })}
          />
          <input
            placeholder="Name"
            value={form.accessory_name}
            onChange={(e) => setForm({ ...form, accessory_name: e.target.value })}
          />
          <input
            placeholder="Spec"
            value={form.accessory_spec}
            onChange={(e) => setForm({ ...form, accessory_spec: e.target.value })}
          />
          <select value={form.factory_id} onChange={(e) => setForm({ ...form, factory_id: e.target.value })}>
            <option value="">Factory (optional)</option>
            {factories.map((factory) => (
              <option key={factory.factory_id} value={factory.factory_id}>
                {factory.name}
              </option>
            ))}
          </select>
          <button type="submit">Create</button>
        </form>
      </div>
      <div className="card">
        <h3>Accessories</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Part #</th>
              <th>Name</th>
              <th>Factory</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.accessory_id}>
                <td>{item.accessory_id}</td>
                <td>{item.part_number}</td>
                <td>{item.accessory_name}</td>
                <td>{item.factory_id || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
