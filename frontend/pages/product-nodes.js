import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function ProductNodes() {
  const [nodes, setNodes] = useState([]);
  const [form, setForm] = useState({ node_code: '', node_name: '', parent_product_node_id: '' });

  const load = async () => {
    setNodes(await apiGet('/product-nodes'));
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/product-nodes', {
      node_code: form.node_code,
      node_name: form.node_name,
      parent_product_node_id: form.parent_product_node_id ? Number(form.parent_product_node_id) : null,
    });
    setForm({ node_code: '', node_name: '', parent_product_node_id: '' });
    load();
  };

  return (
    <Layout title="Product Nodes">
      <div className="card">
        <h3>Create node</h3>
        <form onSubmit={submit}>
          <input
            placeholder="Code"
            value={form.node_code}
            onChange={(e) => setForm({ ...form, node_code: e.target.value })}
          />
          <input
            placeholder="Name"
            value={form.node_name}
            onChange={(e) => setForm({ ...form, node_name: e.target.value })}
          />
          <input
            placeholder="Parent node ID (optional)"
            value={form.parent_product_node_id}
            onChange={(e) => setForm({ ...form, parent_product_node_id: e.target.value })}
          />
          <button type="submit">Create</button>
        </form>
      </div>
      <div className="card">
        <h3>Nodes</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Code</th>
              <th>Name</th>
              <th>Parent</th>
            </tr>
          </thead>
          <tbody>
            {nodes.map((node) => (
              <tr key={node.product_node_id}>
                <td>{node.product_node_id}</td>
                <td>{node.node_code}</td>
                <td>{node.node_name}</td>
                <td>{node.parent_product_node_id ?? '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
