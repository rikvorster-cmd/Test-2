from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Factory(Base):
    __tablename__ = "factories"

    factory_id = Column(BigInteger, primary_key=True)
    factory_code = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    audit_score = Column(Integer)
    risk_score = Column(Integer)


class ProductNode(Base):
    __tablename__ = "product_nodes"

    product_node_id = Column(BigInteger, primary_key=True)
    parent_product_node_id = Column(BigInteger, ForeignKey("product_nodes.product_node_id"))
    node_code = Column(Text, unique=True, nullable=False)
    node_name = Column(Text, nullable=False)

    parent = relationship("ProductNode", remote_side=[product_node_id])


class ParamCatalog(Base):
    __tablename__ = "params_catalog"

    param_id = Column(BigInteger, primary_key=True)
    param_code = Column(Text, unique=True, nullable=False)
    param_name = Column(Text, nullable=False)
    value_type = Column(Text, nullable=False)
    uom_default = Column(Text)


class ParamProductNode(Base):
    __tablename__ = "params_product_node"

    id = Column(BigInteger, primary_key=True)
    product_node_id = Column(BigInteger, ForeignKey("product_nodes.product_node_id"), nullable=False)
    param_id = Column(BigInteger, ForeignKey("params_catalog.param_id"), nullable=False)
    is_required = Column(Boolean, nullable=False, default=False)


class Accessory(Base):
    __tablename__ = "accessories"

    accessory_id = Column(BigInteger, primary_key=True)
    part_number = Column(Text, nullable=False)
    accessory_name = Column(Text, nullable=False)
    accessory_spec = Column(Text)
    factory_id = Column(BigInteger, ForeignKey("factories.factory_id"))
    status = Column(Text)


class CustomerModel(Base):
    __tablename__ = "customer_models"

    customer_model_id = Column(BigInteger, primary_key=True)
    customer_sku = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    product_node_id = Column(BigInteger, ForeignKey("product_nodes.product_node_id"), nullable=False)
    bm_requirements_text = Column(Text)
    status = Column(Text)


class CustomerModelAccessory(Base):
    __tablename__ = "customer_model_accessories"

    customer_accessory_id = Column(BigInteger, primary_key=True)
    customer_model_id = Column(BigInteger, ForeignKey("customer_models.customer_model_id"), nullable=False)
    accessory_id = Column(BigInteger, ForeignKey("accessories.accessory_id"), nullable=False)
    qty = Column(Integer, nullable=False, default=1)
    notes = Column(Text)


class SupplierModel(Base):
    __tablename__ = "supplier_models"

    supplier_model_id = Column(BigInteger, primary_key=True)
    factory_id = Column(BigInteger, ForeignKey("factories.factory_id"), nullable=False)
    factory_model_name = Column(Text, nullable=False)
    product_node_id = Column(BigInteger, ForeignKey("product_nodes.product_node_id"), nullable=False)
    model_status = Column(Text)
    notes = Column(Text)


class Measurement(Base):
    __tablename__ = "measurements"

    measurement_id = Column(BigInteger, primary_key=True)
    supplier_model_id = Column(BigInteger, ForeignKey("supplier_models.supplier_model_id"), nullable=False)
    param_id = Column(BigInteger, ForeignKey("params_catalog.param_id"), nullable=False)
    value = Column(Text, nullable=False)
    uom = Column(Text)
    condition_tag = Column(Text)
    measured_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Link(Base):
    __tablename__ = "links"

    link_id = Column(BigInteger, primary_key=True)
    customer_model_id = Column(BigInteger, ForeignKey("customer_models.customer_model_id"), nullable=False)
    supplier_model_id = Column(BigInteger, ForeignKey("supplier_models.supplier_model_id"), nullable=False)
    status = Column(Text)
    last_price_fob = Column(Numeric)
    currency = Column(Text)
    notes = Column(Text)


class CompareTable(Base):
    __tablename__ = "compare_tables"

    compare_table_id = Column(BigInteger, primary_key=True)
    customer_model_id = Column(BigInteger, ForeignKey("customer_models.customer_model_id"), nullable=False)
    status = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    sent_to_engineer_at = Column(DateTime(timezone=True))


class CompareTableLine(Base):
    __tablename__ = "compare_table_lines"

    compare_line_id = Column(BigInteger, primary_key=True)
    compare_table_id = Column(BigInteger, ForeignKey("compare_tables.compare_table_id"), nullable=False)
    link_id = Column(BigInteger, ForeignKey("links.link_id"), nullable=False)
    engineer_priority = Column(Integer)
    engineer_comments = Column(Text)


class Contract(Base):
    __tablename__ = "contracts"

    contract_id = Column(BigInteger, primary_key=True)
    contract_code = Column(Text, unique=True, nullable=False)
    factory_id = Column(BigInteger, ForeignKey("factories.factory_id"), nullable=False)
    status = Column(Text)
    payment_data = Column(Text)
    bank_data = Column(Text)
    signed_contract_file = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class ContractLine(Base):
    __tablename__ = "contract_lines"

    contract_line_id = Column(BigInteger, primary_key=True)
    contract_id = Column(BigInteger, ForeignKey("contracts.contract_id"), nullable=False)
    link_id = Column(BigInteger, ForeignKey("links.link_id"), nullable=False)
    qty = Column(Integer, nullable=False)
    region = Column(Text)
    delivery_date = Column(Date)
    price = Column(Numeric)
    currency = Column(Text)


class Tolerance(Base):
    __tablename__ = "tolerances"

    tolerance_id = Column(BigInteger, primary_key=True)
    param_id = Column(BigInteger, ForeignKey("params_catalog.param_id"), nullable=False)
    tolerance_rule = Column(Text, nullable=False)


class TestMethod(Base):
    __tablename__ = "test_methods"

    method_id = Column(BigInteger, primary_key=True)
    product_node_id = Column(BigInteger, ForeignKey("product_nodes.product_node_id"), nullable=False)
    method_title = Column(Text, nullable=False)
    method_text = Column(Text, nullable=False)


class TechTask(Base):
    __tablename__ = "tech_task"

    tech_task_id = Column(BigInteger, primary_key=True)
    contract_id = Column(BigInteger, ForeignKey("contracts.contract_id"), nullable=False)
    version = Column(Integer, nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    status = Column(Text)
    content = Column(Text, nullable=False)
