CREATE TABLE factories (
  factory_id BIGSERIAL PRIMARY KEY,
  factory_code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  audit_score INT,
  risk_score INT
);

CREATE TABLE product_nodes (
  product_node_id BIGSERIAL PRIMARY KEY,
  parent_product_node_id BIGINT REFERENCES product_nodes(product_node_id),
  node_code TEXT UNIQUE NOT NULL,
  node_name TEXT NOT NULL
);

CREATE TABLE params_catalog (
  param_id BIGSERIAL PRIMARY KEY,
  param_code TEXT UNIQUE NOT NULL,
  param_name TEXT NOT NULL,
  value_type TEXT NOT NULL,
  uom_default TEXT
);

CREATE TABLE params_product_node (
  id BIGSERIAL PRIMARY KEY,
  product_node_id BIGINT NOT NULL REFERENCES product_nodes(product_node_id),
  param_id BIGINT NOT NULL REFERENCES params_catalog(param_id),
  is_required BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE (product_node_id, param_id)
);

CREATE TABLE accessories (
  accessory_id BIGSERIAL PRIMARY KEY,
  part_number TEXT NOT NULL,
  accessory_name TEXT NOT NULL,
  accessory_spec TEXT,
  factory_id BIGINT REFERENCES factories(factory_id),
  status TEXT
);

CREATE TABLE customer_models (
  customer_model_id BIGSERIAL PRIMARY KEY,
  customer_sku TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  product_node_id BIGINT NOT NULL REFERENCES product_nodes(product_node_id),
  bm_requirements_text TEXT,
  status TEXT
);

CREATE TABLE customer_model_accessories (
  customer_accessory_id BIGSERIAL PRIMARY KEY,
  customer_model_id BIGINT NOT NULL REFERENCES customer_models(customer_model_id),
  accessory_id BIGINT NOT NULL REFERENCES accessories(accessory_id),
  qty INT NOT NULL DEFAULT 1,
  notes TEXT,
  UNIQUE (customer_model_id, accessory_id)
);

CREATE TABLE supplier_models (
  supplier_model_id BIGSERIAL PRIMARY KEY,
  factory_id BIGINT NOT NULL REFERENCES factories(factory_id),
  factory_model_name TEXT NOT NULL,
  product_node_id BIGINT NOT NULL REFERENCES product_nodes(product_node_id),
  model_status TEXT,
  notes TEXT
);

CREATE TABLE measurements (
  measurement_id BIGSERIAL PRIMARY KEY,
  supplier_model_id BIGINT NOT NULL REFERENCES supplier_models(supplier_model_id),
  param_id BIGINT NOT NULL REFERENCES params_catalog(param_id),
  value TEXT NOT NULL,
  uom TEXT,
  condition_tag TEXT,
  measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE links (
  link_id BIGSERIAL PRIMARY KEY,
  customer_model_id BIGINT NOT NULL REFERENCES customer_models(customer_model_id),
  supplier_model_id BIGINT NOT NULL REFERENCES supplier_models(supplier_model_id),
  status TEXT,
  last_price_fob DECIMAL,
  currency TEXT,
  notes TEXT,
  UNIQUE (customer_model_id, supplier_model_id)
);

CREATE TABLE compare_tables (
  compare_table_id BIGSERIAL PRIMARY KEY,
  customer_model_id BIGINT NOT NULL REFERENCES customer_models(customer_model_id),
  status TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sent_to_engineer_at TIMESTAMPTZ
);

CREATE TABLE compare_table_lines (
  compare_line_id BIGSERIAL PRIMARY KEY,
  compare_table_id BIGINT NOT NULL REFERENCES compare_tables(compare_table_id),
  link_id BIGINT NOT NULL REFERENCES links(link_id),
  engineer_priority INT,
  engineer_comments TEXT,
  UNIQUE (compare_table_id, link_id)
);

CREATE TABLE contracts (
  contract_id BIGSERIAL PRIMARY KEY,
  contract_code TEXT UNIQUE NOT NULL,
  factory_id BIGINT NOT NULL REFERENCES factories(factory_id),
  status TEXT,
  payment_data TEXT,
  bank_data TEXT,
  signed_contract_file TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE contract_lines (
  contract_line_id BIGSERIAL PRIMARY KEY,
  contract_id BIGINT NOT NULL REFERENCES contracts(contract_id),
  link_id BIGINT NOT NULL REFERENCES links(link_id),
  qty INT NOT NULL,
  region TEXT,
  delivery_date DATE,
  price DECIMAL,
  currency TEXT
);

CREATE TABLE tolerances (
  tolerance_id BIGSERIAL PRIMARY KEY,
  param_id BIGINT NOT NULL REFERENCES params_catalog(param_id),
  tolerance_rule TEXT NOT NULL
);

CREATE TABLE test_methods (
  method_id BIGSERIAL PRIMARY KEY,
  product_node_id BIGINT NOT NULL REFERENCES product_nodes(product_node_id),
  method_title TEXT NOT NULL,
  method_text TEXT NOT NULL
);

CREATE TABLE tech_task (
  tech_task_id BIGSERIAL PRIMARY KEY,
  contract_id BIGINT NOT NULL REFERENCES contracts(contract_id),
  version INT NOT NULL,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  status TEXT,
  content TEXT NOT NULL
);

CREATE OR REPLACE VIEW effective_params AS
WITH RECURSIVE node_tree AS (
  SELECT
    pn.product_node_id,
    pn.parent_product_node_id,
    pn.product_node_id AS root_id
  FROM product_nodes pn
  UNION ALL
  SELECT
    parent.product_node_id,
    parent.parent_product_node_id,
    node_tree.root_id
  FROM product_nodes parent
  JOIN node_tree ON node_tree.parent_product_node_id = parent.product_node_id
)
SELECT
  node_tree.root_id AS product_node_id,
  ppn.param_id,
  BOOL_OR(ppn.is_required) AS is_required
FROM node_tree
JOIN params_product_node ppn ON ppn.product_node_id = node_tree.product_node_id
GROUP BY node_tree.root_id, ppn.param_id;

CREATE OR REPLACE VIEW effective_methods AS
WITH RECURSIVE node_tree AS (
  SELECT
    pn.product_node_id,
    pn.parent_product_node_id,
    pn.product_node_id AS root_id
  FROM product_nodes pn
  UNION ALL
  SELECT
    parent.product_node_id,
    parent.parent_product_node_id,
    node_tree.root_id
  FROM product_nodes parent
  JOIN node_tree ON node_tree.parent_product_node_id = parent.product_node_id
)
SELECT
  node_tree.root_id AS product_node_id,
  tm.method_id,
  tm.method_title,
  tm.method_text
FROM node_tree
JOIN test_methods tm ON tm.product_node_id = node_tree.product_node_id;
