import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function Contracts() {
  const [contracts, setContracts] = useState([]);
  const [lines, setLines] = useState([]);
  const [techTasks, setTechTasks] = useState([]);
  const [factories, setFactories] = useState([]);
  const [links, setLinks] = useState([]);
  const [form, setForm] = useState({ contract_code: '', factory_id: '', status: '' });
  const [selectedContract, setSelectedContract] = useState('');
  const [lineForm, setLineForm] = useState({ link_id: '', qty: '', region: '', delivery_date: '', price: '', currency: '' });
  const [generatedTask, setGeneratedTask] = useState(null);

  const load = async () => {
    const [contractsData, linesData, techTasksData, factoriesData, linksData] = await Promise.all([
      apiGet('/contracts'),
      apiGet('/contract-lines'),
      apiGet('/tech-tasks'),
      apiGet('/factories'),
      apiGet('/links'),
    ]);
    setContracts(contractsData);
    setLines(linesData);
    setTechTasks(techTasksData);
    setFactories(factoriesData);
    setLinks(linksData);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/contracts', {
      contract_code: form.contract_code,
      factory_id: Number(form.factory_id),
      status: form.status,
      payment_data: '',
      bank_data: '',
    });
    setForm({ contract_code: '', factory_id: '', status: '' });
    load();
  };

  const addLine = async (event) => {
    event.preventDefault();
    await apiPost('/contract-lines', {
      contract_id: Number(selectedContract),
      link_id: Number(lineForm.link_id),
      qty: Number(lineForm.qty),
      region: lineForm.region,
      delivery_date: lineForm.delivery_date || null,
      price: lineForm.price ? Number(lineForm.price) : null,
      currency: lineForm.currency,
    });
    setLineForm({ link_id: '', qty: '', region: '', delivery_date: '', price: '', currency: '' });
    load();
  };

  const generateTechTask = async () => {
    const data = await apiPost(`/contracts/${selectedContract}/generate-tech-task`, {});
    setGeneratedTask(data);
    load();
  };

  const contractLines = lines.filter((line) => line.contract_id === Number(selectedContract));
  const contractTasks = techTasks.filter((task) => task.contract_id === Number(selectedContract));

  return (
    <Layout title="Contracts & Tech Tasks">
      <div className="card">
        <h3>Create contract</h3>
        <form onSubmit={submit}>
          <input
            placeholder="Contract code"
            value={form.contract_code}
            onChange={(e) => setForm({ ...form, contract_code: e.target.value })}
          />
          <select value={form.factory_id} onChange={(e) => setForm({ ...form, factory_id: e.target.value })}>
            <option value="">Select factory</option>
            {factories.map((factory) => (
              <option key={factory.factory_id} value={factory.factory_id}>
                {factory.name}
              </option>
            ))}
          </select>
          <input
            placeholder="Status"
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
          />
          <button type="submit">Create</button>
        </form>
      </div>

      <div className="card">
        <h3>Select contract</h3>
        <select value={selectedContract} onChange={(e) => setSelectedContract(e.target.value)}>
          <option value="">Select contract</option>
          {contracts.map((contract) => (
            <option key={contract.contract_id} value={contract.contract_id}>
              {contract.contract_code}
            </option>
          ))}
        </select>
      </div>

      {selectedContract && (
        <>
          <div className="card">
            <h3>Add contract line</h3>
            <form onSubmit={addLine}>
              <select value={lineForm.link_id} onChange={(e) => setLineForm({ ...lineForm, link_id: e.target.value })}>
                <option value="">Select link</option>
                {links.map((link) => (
                  <option key={link.link_id} value={link.link_id}>
                    Link #{link.link_id}
                  </option>
                ))}
              </select>
              <input
                placeholder="Qty"
                value={lineForm.qty}
                onChange={(e) => setLineForm({ ...lineForm, qty: e.target.value })}
              />
              <input
                placeholder="Region"
                value={lineForm.region}
                onChange={(e) => setLineForm({ ...lineForm, region: e.target.value })}
              />
              <input
                placeholder="Delivery date (YYYY-MM-DD)"
                value={lineForm.delivery_date}
                onChange={(e) => setLineForm({ ...lineForm, delivery_date: e.target.value })}
              />
              <input
                placeholder="Price"
                value={lineForm.price}
                onChange={(e) => setLineForm({ ...lineForm, price: e.target.value })}
              />
              <input
                placeholder="Currency"
                value={lineForm.currency}
                onChange={(e) => setLineForm({ ...lineForm, currency: e.target.value })}
              />
              <button type="submit">Add line</button>
            </form>
          </div>

          <div className="card">
            <h3>Contract lines</h3>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Link</th>
                  <th>Qty</th>
                  <th>Region</th>
                </tr>
              </thead>
              <tbody>
                {contractLines.map((line) => (
                  <tr key={line.contract_line_id}>
                    <td>{line.contract_line_id}</td>
                    <td>{line.link_id}</td>
                    <td>{line.qty}</td>
                    <td>{line.region || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="card">
            <h3>Generate Tech Task</h3>
            <button onClick={generateTechTask}>Generate Tech Task</button>
          </div>

          <div className="card">
            <h3>Tech Tasks</h3>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Version</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {contractTasks.map((task) => (
                  <tr key={task.tech_task_id}>
                    <td>{task.tech_task_id}</td>
                    <td>{task.version}</td>
                    <td>{task.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {generatedTask && (
            <div className="card">
              <h3>Generated Tech Task (Markdown)</h3>
              <pre>{generatedTask.content}</pre>
            </div>
          )}
        </>
      )}
    </Layout>
  );
}
