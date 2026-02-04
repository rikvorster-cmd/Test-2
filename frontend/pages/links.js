import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function Links() {
  const [links, setLinks] = useState([]);
  const [skus, setSkus] = useState([]);
  const [models, setModels] = useState([]);
  const [form, setForm] = useState({ customer_model_id: '', supplier_model_id: '', status: '', last_price_fob: '', currency: '' });

  const load = async () => {
    const [linksData, skusData, modelsData] = await Promise.all([
      apiGet('/links'),
      apiGet('/customer-models'),
      apiGet('/supplier-models'),
    ]);
    setLinks(linksData);
    setSkus(skusData);
    setModels(modelsData);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/links', {
      customer_model_id: Number(form.customer_model_id),
      supplier_model_id: Number(form.supplier_model_id),
      status: form.status,
      last_price_fob: form.last_price_fob ? Number(form.last_price_fob) : null,
      currency: form.currency,
    });
    setForm({ customer_model_id: '', supplier_model_id: '', status: '', last_price_fob: '', currency: '' });
    load();
  };

  return (
    <Layout title="Links (Candidates)">
      <div className="card">
        <h3>Create link</h3>
        <form onSubmit={submit}>
          <select value={form.customer_model_id} onChange={(e) => setForm({ ...form, customer_model_id: e.target.value })}>
            <option value="">Select SKU</option>
            {skus.map((sku) => (
              <option key={sku.customer_model_id} value={sku.customer_model_id}>
                {sku.customer_sku}
              </option>
            ))}
          </select>
          <select value={form.supplier_model_id} onChange={(e) => setForm({ ...form, supplier_model_id: e.target.value })}>
            <option value="">Select supplier model</option>
            {models.map((model) => (
              <option key={model.supplier_model_id} value={model.supplier_model_id}>
                {model.factory_model_name}
              </option>
            ))}
          </select>
          <input
            placeholder="Status"
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
          />
          <input
            placeholder="Price FOB"
            value={form.last_price_fob}
            onChange={(e) => setForm({ ...form, last_price_fob: e.target.value })}
          />
          <input
            placeholder="Currency"
            value={form.currency}
            onChange={(e) => setForm({ ...form, currency: e.target.value })}
          />
          <button type="submit">Create</button>
        </form>
      </div>
      <div className="card">
        <h3>Links</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>SKU</th>
              <th>Supplier model</th>
              <th>Status</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {links.map((link) => (
              <tr key={link.link_id}>
                <td>{link.link_id}</td>
                <td>{link.customer_model_id}</td>
                <td>{link.supplier_model_id}</td>
                <td>{link.status || '-'}</td>
                <td>{link.last_price_fob ? `${link.last_price_fob} ${link.currency || ''}` : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
