import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function ParamsProductNodes() {
  const [rows, setRows] = useState([]);
  const [nodes, setNodes] = useState([]);
  const [params, setParams] = useState([]);
  const [form, setForm] = useState({ product_node_id: '', param_id: '', is_required: false });

  const load = async () => {
    const [rowsData, nodesData, paramsData] = await Promise.all([
      apiGet('/params-product-nodes'),
      apiGet('/product-nodes'),
      apiGet('/params'),
    ]);
    setRows(rowsData);
    setNodes(nodesData);
    setParams(paramsData);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/params-product-nodes', {
      product_node_id: Number(form.product_node_id),
      param_id: Number(form.param_id),
      is_required: form.is_required,
    });
    setForm({ product_node_id: '', param_id: '', is_required: false });
    load();
  };

  return (
    <Layout title="Params per Product Node">
      <div className="card">
        <h3>Attach param to node</h3>
        <form onSubmit={submit}>
          <select value={form.product_node_id} onChange={(e) => setForm({ ...form, product_node_id: e.target.value })}>
            <option value="">Select node</option>
            {nodes.map((node) => (
              <option key={node.product_node_id} value={node.product_node_id}>
                {node.node_name}
              </option>
            ))}
          </select>
          <select value={form.param_id} onChange={(e) => setForm({ ...form, param_id: e.target.value })}>
            <option value="">Select param</option>
            {params.map((param) => (
              <option key={param.param_id} value={param.param_id}>
                {param.param_name}
              </option>
            ))}
          </select>
          <label className="flex">
            <input
              type="checkbox"
              checked={form.is_required}
              onChange={(e) => setForm({ ...form, is_required: e.target.checked })}
            />
            Required
          </label>
          <button type="submit">Attach</button>
        </form>
      </div>
      <div className="card">
        <h3>Assignments</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Node</th>
              <th>Param</th>
              <th>Required</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td>{row.id}</td>
                <td>{row.product_node_id}</td>
                <td>{row.param_id}</td>
                <td>{row.is_required ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
