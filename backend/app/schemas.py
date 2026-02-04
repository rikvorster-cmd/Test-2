from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class FactoryBase(BaseModel):
    factory_code: str
    name: str
    audit_score: Optional[int] = None
    risk_score: Optional[int] = None


class FactoryCreate(FactoryBase):
    pass


class FactoryUpdate(BaseModel):
    factory_code: Optional[str] = None
    name: Optional[str] = None
    audit_score: Optional[int] = None
    risk_score: Optional[int] = None


class Factory(FactoryBase):
    factory_id: int

    class Config:
        from_attributes = True


class ProductNodeBase(BaseModel):
    parent_product_node_id: Optional[int] = None
    node_code: str
    node_name: str


class ProductNodeCreate(ProductNodeBase):
    pass


class ProductNodeUpdate(BaseModel):
    parent_product_node_id: Optional[int] = None
    node_code: Optional[str] = None
    node_name: Optional[str] = None


class ProductNode(ProductNodeBase):
    product_node_id: int

    class Config:
        from_attributes = True


class ParamCatalogBase(BaseModel):
    param_code: str
    param_name: str
    value_type: str
    uom_default: Optional[str] = None


class ParamCatalogCreate(ParamCatalogBase):
    pass


class ParamCatalogUpdate(BaseModel):
    param_code: Optional[str] = None
    param_name: Optional[str] = None
    value_type: Optional[str] = None
    uom_default: Optional[str] = None


class ParamCatalog(ParamCatalogBase):
    param_id: int

    class Config:
        from_attributes = True


class ParamProductNodeBase(BaseModel):
    product_node_id: int
    param_id: int
    is_required: bool = False


class ParamProductNodeCreate(ParamProductNodeBase):
    pass


class ParamProductNodeUpdate(BaseModel):
    is_required: Optional[bool] = None


class ParamProductNode(ParamProductNodeBase):
    id: int

    class Config:
        from_attributes = True


class AccessoryBase(BaseModel):
    part_number: str
    accessory_name: str
    accessory_spec: Optional[str] = None
    factory_id: Optional[int] = None
    status: Optional[str] = None


class AccessoryCreate(AccessoryBase):
    pass


class AccessoryUpdate(BaseModel):
    part_number: Optional[str] = None
    accessory_name: Optional[str] = None
    accessory_spec: Optional[str] = None
    factory_id: Optional[int] = None
    status: Optional[str] = None


class Accessory(AccessoryBase):
    accessory_id: int

    class Config:
        from_attributes = True


class CustomerModelBase(BaseModel):
    customer_sku: str
    name: str
    product_node_id: int
    bm_requirements_text: Optional[str] = None
    status: Optional[str] = None


class CustomerModelCreate(CustomerModelBase):
    pass


class CustomerModelUpdate(BaseModel):
    customer_sku: Optional[str] = None
    name: Optional[str] = None
    product_node_id: Optional[int] = None
    bm_requirements_text: Optional[str] = None
    status: Optional[str] = None


class CustomerModel(CustomerModelBase):
    customer_model_id: int

    class Config:
        from_attributes = True


class CustomerModelAccessoryBase(BaseModel):
    customer_model_id: int
    accessory_id: int
    qty: int = 1
    notes: Optional[str] = None


class CustomerModelAccessoryCreate(CustomerModelAccessoryBase):
    pass


class CustomerModelAccessoryUpdate(BaseModel):
    qty: Optional[int] = None
    notes: Optional[str] = None


class CustomerModelAccessory(CustomerModelAccessoryBase):
    customer_accessory_id: int

    class Config:
        from_attributes = True


class SupplierModelBase(BaseModel):
    factory_id: int
    factory_model_name: str
    product_node_id: int
    model_status: Optional[str] = None
    notes: Optional[str] = None


class SupplierModelCreate(SupplierModelBase):
    pass


class SupplierModelUpdate(BaseModel):
    factory_id: Optional[int] = None
    factory_model_name: Optional[str] = None
    product_node_id: Optional[int] = None
    model_status: Optional[str] = None
    notes: Optional[str] = None


class SupplierModel(SupplierModelBase):
    supplier_model_id: int

    class Config:
        from_attributes = True


class MeasurementBase(BaseModel):
    supplier_model_id: int
    param_id: int
    value: str
    uom: Optional[str] = None
    condition_tag: Optional[str] = None
    measured_at: Optional[datetime] = None


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementUpdate(BaseModel):
    value: Optional[str] = None
    uom: Optional[str] = None
    condition_tag: Optional[str] = None
    measured_at: Optional[datetime] = None


class Measurement(MeasurementBase):
    measurement_id: int

    class Config:
        from_attributes = True


class LinkBase(BaseModel):
    customer_model_id: int
    supplier_model_id: int
    status: Optional[str] = None
    last_price_fob: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    status: Optional[str] = None
    last_price_fob: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None


class Link(LinkBase):
    link_id: int

    class Config:
        from_attributes = True


class CompareTableBase(BaseModel):
    customer_model_id: int
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    sent_to_engineer_at: Optional[datetime] = None


class CompareTableCreate(CompareTableBase):
    pass


class CompareTableUpdate(BaseModel):
    status: Optional[str] = None
    sent_to_engineer_at: Optional[datetime] = None


class CompareTable(CompareTableBase):
    compare_table_id: int

    class Config:
        from_attributes = True


class CompareTableLineBase(BaseModel):
    compare_table_id: int
    link_id: int
    engineer_priority: Optional[int] = None
    engineer_comments: Optional[str] = None


class CompareTableLineCreate(CompareTableLineBase):
    pass


class CompareTableLineUpdate(BaseModel):
    engineer_priority: Optional[int] = None
    engineer_comments: Optional[str] = None


class CompareTableLine(CompareTableLineBase):
    compare_line_id: int

    class Config:
        from_attributes = True


class ContractBase(BaseModel):
    contract_code: str
    factory_id: int
    status: Optional[str] = None
    payment_data: Optional[str] = None
    bank_data: Optional[str] = None
    signed_contract_file: Optional[str] = None
    created_at: Optional[datetime] = None


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    contract_code: Optional[str] = None
    factory_id: Optional[int] = None
    status: Optional[str] = None
    payment_data: Optional[str] = None
    bank_data: Optional[str] = None
    signed_contract_file: Optional[str] = None


class Contract(ContractBase):
    contract_id: int

    class Config:
        from_attributes = True


class ContractLineBase(BaseModel):
    contract_id: int
    link_id: int
    qty: int
    region: Optional[str] = None
    delivery_date: Optional[date] = None
    price: Optional[float] = None
    currency: Optional[str] = None


class ContractLineCreate(ContractLineBase):
    pass


class ContractLineUpdate(BaseModel):
    qty: Optional[int] = None
    region: Optional[str] = None
    delivery_date: Optional[date] = None
    price: Optional[float] = None
    currency: Optional[str] = None


class ContractLine(ContractLineBase):
    contract_line_id: int

    class Config:
        from_attributes = True


class ToleranceBase(BaseModel):
    param_id: int
    tolerance_rule: str


class ToleranceCreate(ToleranceBase):
    pass


class ToleranceUpdate(BaseModel):
    param_id: Optional[int] = None
    tolerance_rule: Optional[str] = None


class Tolerance(ToleranceBase):
    tolerance_id: int

    class Config:
        from_attributes = True


class TestMethodBase(BaseModel):
    product_node_id: int
    method_title: str
    method_text: str


class TestMethodCreate(TestMethodBase):
    pass


class TestMethodUpdate(BaseModel):
    product_node_id: Optional[int] = None
    method_title: Optional[str] = None
    method_text: Optional[str] = None


class TestMethod(TestMethodBase):
    method_id: int

    class Config:
        from_attributes = True


class TechTaskBase(BaseModel):
    contract_id: int
    version: int
    generated_at: Optional[datetime] = None
    status: Optional[str] = None
    content: str


class TechTaskCreate(TechTaskBase):
    pass


class TechTask(TechTaskBase):
    tech_task_id: int

    class Config:
        from_attributes = True


class EffectiveParam(BaseModel):
    product_node_id: int
    param_id: int
    is_required: bool
    param_code: str
    param_name: str
    uom_default: Optional[str] = None


class EffectiveMethod(BaseModel):
    product_node_id: int
    method_id: int
    method_title: str
    method_text: str


class CompareMatrixRow(BaseModel):
    link_id: int
    supplier_model_id: int
    factory_name: Optional[str]
    status: Optional[str]
    last_price_fob: Optional[float]
    currency: Optional[str]
    values: dict


class CompareMatrixResponse(BaseModel):
    params: list[EffectiveParam]
    rows: list[CompareMatrixRow]


class TechTaskResponse(BaseModel):
    tech_task_id: int
    version: int
    content: str
