import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { apiGet, apiPost } from '../components/api';

export default function SupplierModels() {
  const [models, setModels] = useState([]);
  const [factories, setFactories] = useState([]);
  const [nodes, setNodes] = useState([]);
  const [form, setForm] = useState({ factory_id: '', factory_model_name: '', product_node_id: '' });
  const [newFactory, setNewFactory] = useState({ factory_code: '', name: '' });
  const [selectedModel, setSelectedModel] = useState('');
  const [effectiveParams, setEffectiveParams] = useState([]);
  const [measurementForm, setMeasurementForm] = useState({});
  const [measurements, setMeasurements] = useState([]);

  const load = async () => {
    const [modelsData, factoriesData, nodesData] = await Promise.all([
      apiGet('/supplier-models'),
      apiGet('/factories'),
      apiGet('/product-nodes'),
    ]);
    setModels(modelsData);
    setFactories(factoriesData);
    setNodes(nodesData);
  };

  const loadMeasurements = async (modelId) => {
    const list = await apiGet('/measurements');
    setMeasurements(list.filter((row) => row.supplier_model_id === Number(modelId)));
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    const current = models.find((m) => m.supplier_model_id === Number(selectedModel));
    if (current) {
      apiGet(`/product-nodes/${current.product_node_id}/effective-params`).then(setEffectiveParams);
      loadMeasurements(selectedModel);
    }
  }, [selectedModel, models]);

  const createFactoryInline = async () => {
    if (!newFactory.factory_code || !newFactory.name) return;
    const created = await apiPost('/factories', newFactory);
    setFactories((prev) => [...prev, created]);
    setForm({ ...form, factory_id: String(created.factory_id) });
    setNewFactory({ factory_code: '', name: '' });
  };

  const submit = async (event) => {
    event.preventDefault();
    await apiPost('/supplier-models', {
      factory_id: Number(form.factory_id),
      factory_model_name: form.factory_model_name,
      product_node_id: Number(form.product_node_id),
    });
    setForm({ factory_id: '', factory_model_name: '', product_node_id: '' });
    load();
  };

  const submitMeasurements = async (event) => {
    event.preventDefault();
    const entries = Object.entries(measurementForm);
    for (const [paramId, value] of entries) {
      if (!value) continue;
      const param = effectiveParams.find((p) => String(p.param_id) === paramId);
      await apiPost('/measurements', {
        supplier_model_id: Number(selectedModel),
        param_id: Number(paramId),
        value,
        uom: param?.uom_default || null,
        condition_tag: '',
      });
    }
    setMeasurementForm({});
    loadMeasurements(selectedModel);
  };

  return (
    <Layout title="Supplier Models">
      <div className="card">
        <h3>Create supplier model</h3>
        <form onSubmit={submit}>
          <select value={form.factory_id} onChange={(e) => setForm({ ...form, factory_id: e.target.value })}>
            <option value="">Select factory</option>
            {factories.map((factory) => (
              <option key={factory.factory_id} value={factory.factory_id}>
                {factory.name}
              </option>
            ))}
          </select>
          <div className="flex">
            <input
              placeholder="New factory code"
              value={newFactory.factory_code}
              onChange={(e) => setNewFactory({ ...newFactory, factory_code: e.target.value })}
            />
            <input
              placeholder="New factory name"
              value={newFactory.name}
              onChange={(e) => setNewFactory({ ...newFactory, name: e.target.value })}
            />
            <button type="button" className="secondary" onClick={createFactoryInline}>
              Inline create factory
            </button>
          </div>
          <input
            placeholder="Factory model name"
            value={form.factory_model_name}
            onChange={(e) => setForm({ ...form, factory_model_name: e.target.value })}
          />
          <select value={form.product_node_id} onChange={(e) => setForm({ ...form, product_node_id: e.target.value })}>
            <option value="">Select product node</option>
            {nodes.map((node) => (
              <option key={node.product_node_id} value={node.product_node_id}>
                {node.node_name}
              </option>
            ))}
          </select>
          <button type="submit">Create supplier model</button>
        </form>
      </div>

      <div className="card">
        <h3>Supplier models</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Factory</th>
              <th>Name</th>
              <th>Node</th>
            </tr>
          </thead>
          <tbody>
            {models.map((model) => (
              <tr key={model.supplier_model_id}>
                <td>{model.supplier_model_id}</td>
                <td>{model.factory_id}</td>
                <td>{model.factory_model_name}</td>
                <td>{model.product_node_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Measurements (what to measure)</h3>
        <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
          <option value="">Select supplier model</option>
          {models.map((model) => (
            <option key={model.supplier_model_id} value={model.supplier_model_id}>
              {model.factory_model_name}
            </option>
          ))}
        </select>

        {selectedModel && (
          <>
            <form onSubmit={submitMeasurements}>
              {effectiveParams.map((param) => (
                <input
                  key={param.param_id}
                  placeholder={`${param.param_name} (${param.uom_default || '-'})`}
                  value={measurementForm[param.param_id] || ''}
                  onChange={(e) =>
                    setMeasurementForm({
                      ...measurementForm,
                      [param.param_id]: e.target.value,
                    })
                  }
                />
              ))}
              <button type="submit">Save measurements</button>
            </form>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Param</th>
                  <th>Value</th>
                  <th>UOM</th>
                </tr>
              </thead>
              <tbody>
                {measurements.map((m) => (
                  <tr key={m.measurement_id}>
                    <td>{m.measurement_id}</td>
                    <td>{m.param_id}</td>
                    <td>{m.value}</td>
                    <td>{m.uom || '-'}</td>
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
