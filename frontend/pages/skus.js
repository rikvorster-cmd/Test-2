import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function Skus() {
  const [skus, setSkus] = useState([]);
  const [nodes, setNodes] = useState([]);
  const [accessories, setAccessories] = useState([]);
  const [form, setForm] = useState({ customer_sku: '', name: '', product_node_id: '', bm_requirements_text: '' });
  const [selectedSku, setSelectedSku] = useState('');
  const [skuAccessory, setSkuAccessory] = useState({ accessory_id: '', qty: 1, notes: '' });
  const [skuAccessories, setSkuAccessories] = useState([]);

  const load = async () => {
    const [skusData, nodesData, accessoriesData] = await Promise.all([
      apiGet('/customer-models'),
      apiGet('/product-nodes'),
      apiGet('/accessories'),
    ]);
    setSkus(skusData);
    setNodes(nodesData);
    setAccessories(accessoriesData);
  };

  const loadSkuAccessories = async (skuId) => {
    const rows = await apiGet('/customer-model-accessories');
    setSkuAccessories(rows.filter((row) => row.customer_model_id === Number(skuId)));
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    if (selectedSku) {
      loadSkuAccessories(selectedSku);
    }
  }, [selectedSku]);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/customer-models', {
      ...form,
      product_node_id: Number(form.product_node_id),
    });
    setForm({ customer_sku: '', name: '', product_node_id: '', bm_requirements_text: '' });
    load();
  };

  const addAccessory = async (event) => {
    event.preventDefault();
    await apiPost('/customer-model-accessories', {
      customer_model_id: Number(selectedSku),
      accessory_id: Number(skuAccessory.accessory_id),
      qty: Number(skuAccessory.qty),
      notes: skuAccessory.notes,
    });
    setSkuAccessory({ accessory_id: '', qty: 1, notes: '' });
    loadSkuAccessories(selectedSku);
  };

  return (
    <Layout title="SKU (Customer Models)">
      <div className="card">
        <h3>Create SKU</h3>
        <form onSubmit={submit}>
          <input
            placeholder="SKU code"
            value={form.customer_sku}
            onChange={(e) => setForm({ ...form, customer_sku: e.target.value })}
          />
          <input
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <select
            value={form.product_node_id}
            onChange={(e) => setForm({ ...form, product_node_id: e.target.value })}
          >
            <option value="">Select product node</option>
            {nodes.map((node) => (
              <option key={node.product_node_id} value={node.product_node_id}>
                {node.node_name}
              </option>
            ))}
          </select>
          <textarea
            placeholder="BM requirements"
            value={form.bm_requirements_text}
            onChange={(e) => setForm({ ...form, bm_requirements_text: e.target.value })}
          />
          <button type="submit">Create</button>
        </form>
      </div>

      <div className="card">
        <h3>SKU list</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>SKU</th>
              <th>Name</th>
              <th>Node</th>
            </tr>
          </thead>
          <tbody>
            {skus.map((sku) => (
              <tr key={sku.customer_model_id}>
                <td>{sku.customer_model_id}</td>
                <td>{sku.customer_sku}</td>
                <td>{sku.name}</td>
                <td>{sku.product_node_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>SKU Accessories</h3>
        <div className="flex">
          <select value={selectedSku} onChange={(e) => setSelectedSku(e.target.value)}>
            <option value="">Select SKU</option>
            {skus.map((sku) => (
              <option key={sku.customer_model_id} value={sku.customer_model_id}>
                {sku.customer_sku}
              </option>
            ))}
          </select>
        </div>
        {selectedSku && (
          <>
            <form onSubmit={addAccessory}>
              <select
                value={skuAccessory.accessory_id}
                onChange={(e) => setSkuAccessory({ ...skuAccessory, accessory_id: e.target.value })}
              >
                <option value="">Select accessory</option>
                {accessories.map((acc) => (
                  <option key={acc.accessory_id} value={acc.accessory_id}>
                    {acc.accessory_name}
                  </option>
                ))}
              </select>
              <input
                type="number"
                placeholder="Qty"
                value={skuAccessory.qty}
                onChange={(e) => setSkuAccessory({ ...skuAccessory, qty: e.target.value })}
              />
              <input
                placeholder="Notes"
                value={skuAccessory.notes}
                onChange={(e) => setSkuAccessory({ ...skuAccessory, notes: e.target.value })}
              />
              <button type="submit">Add accessory</button>
            </form>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Accessory</th>
                  <th>Qty</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                {skuAccessories.map((row) => (
                  <tr key={row.customer_accessory_id}>
                    <td>{row.customer_accessory_id}</td>
                    <td>{row.accessory_id}</td>
                    <td>{row.qty}</td>
                    <td>{row.notes || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </div>
    </Layout>
  );
}
