import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost, apiPut } from '../components/api';

export default function CompareTables() {
  const [tables, setTables] = useState([]);
  const [skus, setSkus] = useState([]);
  const [links, setLinks] = useState([]);
  const [lines, setLines] = useState([]);
  const [matrix, setMatrix] = useState(null);
  const [form, setForm] = useState({ customer_model_id: '' });
  const [selectedTable, setSelectedTable] = useState('');
  const [selectedLink, setSelectedLink] = useState('');

  const load = async () => {
    const [tablesData, skusData, linksData, linesData] = await Promise.all([
      apiGet('/compare-tables'),
      apiGet('/customer-models'),
      apiGet('/links'),
      apiGet('/compare-table-lines'),
    ]);
    setTables(tablesData);
    setSkus(skusData);
    setLinks(linksData);
    setLines(linesData);
  };

  const loadMatrix = async (tableId) => {
    const data = await apiGet(`/compare-tables/${tableId}/matrix`);
    setMatrix(data);
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    if (selectedTable) {
      loadMatrix(selectedTable);
    }
  }, [selectedTable]);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/compare-tables', {
      customer_model_id: Number(form.customer_model_id),
      status: 'draft',
    });
    setForm({ customer_model_id: '' });
    load();
  };

  const addLine = async (event) => {
    event.preventDefault();
    await apiPost('/compare-table-lines', {
      compare_table_id: Number(selectedTable),
      link_id: Number(selectedLink),
    });
    setSelectedLink('');
    load();
    loadMatrix(selectedTable);
  };

  const sendToEngineer = async () => {
    await apiPost(`/compare-tables/${selectedTable}/send`, {});
    load();
  };

  const updateLine = async (lineId, payload) => {
    await apiPut(`/compare-table-lines/${lineId}`, payload);
    load();
  };

  const tableLines = lines.filter((line) => line.compare_table_id === Number(selectedTable));
  const availableLinks = selectedTable
    ? links.filter((link) => {
        const table = tables.find((t) => t.compare_table_id === Number(selectedTable));
        return table && link.customer_model_id === table.customer_model_id;
      })
    : [];

  return (
    <Layout title="Compare Tables">
      <div className="card">
        <h3>Create compare table</h3>
        <form onSubmit={submit}>
          <select value={form.customer_model_id} onChange={(e) => setForm({ customer_model_id: e.target.value })}>
            <option value="">Select SKU</option>
            {skus.map((sku) => (
              <option key={sku.customer_model_id} value={sku.customer_model_id}>
                {sku.customer_sku}
              </option>
            ))}
          </select>
          <button type="submit">Create</button>
        </form>
      </div>

      <div className="card">
        <h3>Compare tables</h3>
        <select value={selectedTable} onChange={(e) => setSelectedTable(e.target.value)}>
          <option value="">Select table</option>
          {tables.map((table) => (
            <option key={table.compare_table_id} value={table.compare_table_id}>
              Table #{table.compare_table_id} (SKU {table.customer_model_id})
            </option>
          ))}
        </select>
        {selectedTable && (
          <div className="flex">
            <button onClick={sendToEngineer}>Send to Engineer</button>
          </div>
        )}
      </div>

      {selectedTable && (
        <>
          <div className="card">
            <h3>Add candidates (links)</h3>
            <form onSubmit={addLine}>
              <select value={selectedLink} onChange={(e) => setSelectedLink(e.target.value)}>
                <option value="">Select link</option>
                {availableLinks.map((link) => (
                  <option key={link.link_id} value={link.link_id}>
                    Link #{link.link_id}
                  </option>
                ))}
              </select>
              <button type="submit">Add line</button>
            </form>
          </div>

          <div className="card">
            <h3>Engineer review</h3>
            <table className="table">
              <thead>
                <tr>
                  <th>Line ID</th>
                  <th>Link ID</th>
                  <th>Priority</th>
                  <th>Comments</th>
                </tr>
              </thead>
              <tbody>
                {tableLines.map((line) => (
                  <tr key={line.compare_line_id}>
                    <td>{line.compare_line_id}</td>
                    <td>{line.link_id}</td>
                    <td>
                      <input
                        value={line.engineer_priority ?? ''}
                        onChange={(e) => updateLine(line.compare_line_id, { engineer_priority: Number(e.target.value) })}
                      />
                    </td>
                    <td>
                      <input
                        value={line.engineer_comments ?? ''}
                        onChange={(e) => updateLine(line.compare_line_id, { engineer_comments: e.target.value })}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="card">
            <h3>Comparison matrix</h3>
            {matrix && (
              <table className="table">
                <thead>
                  <tr>
                    <th>Link</th>
                    <th>Factory</th>
                    <th>Status</th>
                    <th>Price</th>
                    {matrix.params.map((param) => (
                      <th key={param.param_id}>{param.param_code}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {matrix.rows.map((row) => (
                    <tr key={row.link_id}>
                      <td>{row.link_id}</td>
                      <td>{row.factory_name}</td>
                      <td>{row.status || '-'}</td>
                      <td>{row.last_price_fob ? `${row.last_price_fob} ${row.currency || ''}` : '-'}</td>
                      {matrix.params.map((param) => (
                        <td key={param.param_id}>{row.values[String(param.param_id)] || '-'}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </Layout>
  );
}
