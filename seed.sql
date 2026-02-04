INSERT INTO factories (factory_code, name, audit_score, risk_score)
VALUES
  ('FAC-ALPHA', 'Alpha Manufacturing', 85, 3),
  ('FAC-BETA', 'Beta Industrial', 78, 4);

INSERT INTO product_nodes (parent_product_node_id, node_code, node_name)
VALUES
  (NULL, 'WELDING', 'Welding equipment'),
  (1, 'WELDING-MIG', 'MIG welders'),
  (1, 'WELDING-TIG', 'TIG welders');

INSERT INTO params_catalog (param_code, param_name, value_type, uom_default)
VALUES
  ('VOLTAGE', 'Input voltage', 'number', 'V'),
  ('CURRENT', 'Output current', 'number', 'A'),
  ('PF', 'Power factor', 'number', ''),
  ('DUTY', 'Duty cycle', 'number', '%'),
  ('WEIGHT', 'Net weight', 'number', 'kg'),
  ('DIM-L', 'Length', 'number', 'mm'),
  ('DIM-W', 'Width', 'number', 'mm'),
  ('DIM-H', 'Height', 'number', 'mm'),
  ('GAS', 'Shielding gas', 'text', ''),
  ('WIRE', 'Wire diameter', 'number', 'mm');

INSERT INTO params_product_node (product_node_id, param_id, is_required)
VALUES
  (1, 1, true),
  (1, 2, true),
  (1, 3, false),
  (1, 4, true),
  (1, 5, false),
  (1, 6, false),
  (1, 7, false),
  (1, 8, false),
  (2, 9, false),
  (2, 10, false);

INSERT INTO test_methods (product_node_id, method_title, method_text)
VALUES
  (1, 'Visual inspection', 'Check casing, labeling, and safety marks.'),
  (2, 'MIG arc stability', 'Run a 10-minute arc stability test at 200A.');

INSERT INTO tolerances (param_id, tolerance_rule)
VALUES
  (1, '±5%'),
  (2, '±5%'),
  (3, '±0.02'),
  (4, '>= measured - 5% abs');
