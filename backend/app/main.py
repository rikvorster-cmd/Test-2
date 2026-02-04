from datetime import datetime
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import SessionLocal

app = FastAPI(title="MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


# Factories
@app.get("/factories", response_model=list[schemas.Factory])
def list_factories(db: Session = Depends(get_db)):
    return db.query(models.Factory).order_by(models.Factory.factory_id).all()


@app.post("/factories", response_model=schemas.Factory)
def create_factory(payload: schemas.FactoryCreate, db: Session = Depends(get_db)):
    factory = models.Factory(**payload.model_dump())
    db.add(factory)
    db.commit()
    db.refresh(factory)
    return factory


@app.get("/factories/{factory_id}", response_model=schemas.Factory)
def get_factory(factory_id: int, db: Session = Depends(get_db)):
    factory = db.get(models.Factory, factory_id)
    if not factory:
        raise HTTPException(status_code=404, detail="Factory not found")
    return factory


@app.put("/factories/{factory_id}", response_model=schemas.Factory)
def update_factory(factory_id: int, payload: schemas.FactoryUpdate, db: Session = Depends(get_db)):
    factory = db.get(models.Factory, factory_id)
    if not factory:
        raise HTTPException(status_code=404, detail="Factory not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(factory, key, value)
    db.commit()
    db.refresh(factory)
    return factory


@app.delete("/factories/{factory_id}")
def delete_factory(factory_id: int, db: Session = Depends(get_db)):
    factory = db.get(models.Factory, factory_id)
    if not factory:
        raise HTTPException(status_code=404, detail="Factory not found")
    db.delete(factory)
    db.commit()
    return {"status": "deleted"}


# Product nodes
@app.get("/product-nodes", response_model=list[schemas.ProductNode])
def list_product_nodes(db: Session = Depends(get_db)):
    return db.query(models.ProductNode).order_by(models.ProductNode.product_node_id).all()


@app.post("/product-nodes", response_model=schemas.ProductNode)
def create_product_node(payload: schemas.ProductNodeCreate, db: Session = Depends(get_db)):
    node = models.ProductNode(**payload.model_dump())
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


@app.get("/product-nodes/{product_node_id}", response_model=schemas.ProductNode)
def get_product_node(product_node_id: int, db: Session = Depends(get_db)):
    node = db.get(models.ProductNode, product_node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Product node not found")
    return node


@app.put("/product-nodes/{product_node_id}", response_model=schemas.ProductNode)
def update_product_node(product_node_id: int, payload: schemas.ProductNodeUpdate, db: Session = Depends(get_db)):
    node = db.get(models.ProductNode, product_node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Product node not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(node, key, value)
    db.commit()
    db.refresh(node)
    return node


@app.delete("/product-nodes/{product_node_id}")
def delete_product_node(product_node_id: int, db: Session = Depends(get_db)):
    node = db.get(models.ProductNode, product_node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Product node not found")
    db.delete(node)
    db.commit()
    return {"status": "deleted"}


# Params catalog
@app.get("/params", response_model=list[schemas.ParamCatalog])
def list_params(db: Session = Depends(get_db)):
    return db.query(models.ParamCatalog).order_by(models.ParamCatalog.param_id).all()


@app.post("/params", response_model=schemas.ParamCatalog)
def create_param(payload: schemas.ParamCatalogCreate, db: Session = Depends(get_db)):
    param = models.ParamCatalog(**payload.model_dump())
    db.add(param)
    db.commit()
    db.refresh(param)
    return param


@app.put("/params/{param_id}", response_model=schemas.ParamCatalog)
def update_param(param_id: int, payload: schemas.ParamCatalogUpdate, db: Session = Depends(get_db)):
    param = db.get(models.ParamCatalog, param_id)
    if not param:
        raise HTTPException(status_code=404, detail="Param not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(param, key, value)
    db.commit()
    db.refresh(param)
    return param


@app.delete("/params/{param_id}")
def delete_param(param_id: int, db: Session = Depends(get_db)):
    param = db.get(models.ParamCatalog, param_id)
    if not param:
        raise HTTPException(status_code=404, detail="Param not found")
    db.delete(param)
    db.commit()
    return {"status": "deleted"}


# Params product node
@app.get("/params-product-nodes", response_model=list[schemas.ParamProductNode])
def list_params_product_nodes(db: Session = Depends(get_db)):
    return db.query(models.ParamProductNode).order_by(models.ParamProductNode.id).all()


@app.post("/params-product-nodes", response_model=schemas.ParamProductNode)
def create_params_product_nodes(payload: schemas.ParamProductNodeCreate, db: Session = Depends(get_db)):
    row = models.ParamProductNode(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.put("/params-product-nodes/{row_id}", response_model=schemas.ParamProductNode)
def update_params_product_nodes(row_id: int, payload: schemas.ParamProductNodeUpdate, db: Session = Depends(get_db)):
    row = db.get(models.ParamProductNode, row_id)
    if not row:
        raise HTTPException(status_code=404, detail="Param-product node not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


@app.delete("/params-product-nodes/{row_id}")
def delete_params_product_nodes(row_id: int, db: Session = Depends(get_db)):
    row = db.get(models.ParamProductNode, row_id)
    if not row:
        raise HTTPException(status_code=404, detail="Param-product node not found")
    db.delete(row)
    db.commit()
    return {"status": "deleted"}


# Accessories
@app.get("/accessories", response_model=list[schemas.Accessory])
def list_accessories(db: Session = Depends(get_db)):
    return db.query(models.Accessory).order_by(models.Accessory.accessory_id).all()


@app.post("/accessories", response_model=schemas.Accessory)
def create_accessory(payload: schemas.AccessoryCreate, db: Session = Depends(get_db)):
    accessory = models.Accessory(**payload.model_dump())
    db.add(accessory)
    db.commit()
    db.refresh(accessory)
    return accessory


@app.put("/accessories/{accessory_id}", response_model=schemas.Accessory)
def update_accessory(accessory_id: int, payload: schemas.AccessoryUpdate, db: Session = Depends(get_db)):
    accessory = db.get(models.Accessory, accessory_id)
    if not accessory:
        raise HTTPException(status_code=404, detail="Accessory not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(accessory, key, value)
    db.commit()
    db.refresh(accessory)
    return accessory


@app.delete("/accessories/{accessory_id}")
def delete_accessory(accessory_id: int, db: Session = Depends(get_db)):
    accessory = db.get(models.Accessory, accessory_id)
    if not accessory:
        raise HTTPException(status_code=404, detail="Accessory not found")
    db.delete(accessory)
    db.commit()
    return {"status": "deleted"}


# Customer models (SKU)
@app.get("/customer-models", response_model=list[schemas.CustomerModel])
def list_customer_models(db: Session = Depends(get_db)):
    return db.query(models.CustomerModel).order_by(models.CustomerModel.customer_model_id).all()


@app.post("/customer-models", response_model=schemas.CustomerModel)
def create_customer_model(payload: schemas.CustomerModelCreate, db: Session = Depends(get_db)):
    model = models.CustomerModel(**payload.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@app.put("/customer-models/{customer_model_id}", response_model=schemas.CustomerModel)
def update_customer_model(customer_model_id: int, payload: schemas.CustomerModelUpdate, db: Session = Depends(get_db)):
    model = db.get(models.CustomerModel, customer_model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Customer model not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(model, key, value)
    db.commit()
    db.refresh(model)
    return model


@app.delete("/customer-models/{customer_model_id}")
def delete_customer_model(customer_model_id: int, db: Session = Depends(get_db)):
    model = db.get(models.CustomerModel, customer_model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Customer model not found")
    db.delete(model)
    db.commit()
    return {"status": "deleted"}


# Customer model accessories
@app.get("/customer-model-accessories", response_model=list[schemas.CustomerModelAccessory])
def list_customer_model_accessories(db: Session = Depends(get_db)):
    return db.query(models.CustomerModelAccessory).order_by(models.CustomerModelAccessory.customer_accessory_id).all()


@app.post("/customer-model-accessories", response_model=schemas.CustomerModelAccessory)
def create_customer_model_accessory(payload: schemas.CustomerModelAccessoryCreate, db: Session = Depends(get_db)):
    row = models.CustomerModelAccessory(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.put("/customer-model-accessories/{row_id}", response_model=schemas.CustomerModelAccessory)
def update_customer_model_accessory(row_id: int, payload: schemas.CustomerModelAccessoryUpdate, db: Session = Depends(get_db)):
    row = db.get(models.CustomerModelAccessory, row_id)
    if not row:
        raise HTTPException(status_code=404, detail="Customer model accessory not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


@app.delete("/customer-model-accessories/{row_id}")
def delete_customer_model_accessory(row_id: int, db: Session = Depends(get_db)):
    row = db.get(models.CustomerModelAccessory, row_id)
    if not row:
        raise HTTPException(status_code=404, detail="Customer model accessory not found")
    db.delete(row)
    db.commit()
    return {"status": "deleted"}


# Supplier models
@app.get("/supplier-models", response_model=list[schemas.SupplierModel])
def list_supplier_models(db: Session = Depends(get_db)):
    return db.query(models.SupplierModel).order_by(models.SupplierModel.supplier_model_id).all()


@app.post("/supplier-models", response_model=schemas.SupplierModel)
def create_supplier_model(payload: schemas.SupplierModelCreate, db: Session = Depends(get_db)):
    model = models.SupplierModel(**payload.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@app.put("/supplier-models/{supplier_model_id}", response_model=schemas.SupplierModel)
def update_supplier_model(supplier_model_id: int, payload: schemas.SupplierModelUpdate, db: Session = Depends(get_db)):
    model = db.get(models.SupplierModel, supplier_model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Supplier model not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(model, key, value)
    db.commit()
    db.refresh(model)
    return model


@app.delete("/supplier-models/{supplier_model_id}")
def delete_supplier_model(supplier_model_id: int, db: Session = Depends(get_db)):
    model = db.get(models.SupplierModel, supplier_model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Supplier model not found")
    db.delete(model)
    db.commit()
    return {"status": "deleted"}


# Measurements
@app.get("/measurements", response_model=list[schemas.Measurement])
def list_measurements(db: Session = Depends(get_db)):
    return db.query(models.Measurement).order_by(models.Measurement.measurement_id).all()


@app.post("/measurements", response_model=schemas.Measurement)
def create_measurement(payload: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    measurement = models.Measurement(**payload.model_dump())
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


@app.put("/measurements/{measurement_id}", response_model=schemas.Measurement)
def update_measurement(measurement_id: int, payload: schemas.MeasurementUpdate, db: Session = Depends(get_db)):
    measurement = db.get(models.Measurement, measurement_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(measurement, key, value)
    db.commit()
    db.refresh(measurement)
    return measurement


@app.delete("/measurements/{measurement_id}")
def delete_measurement(measurement_id: int, db: Session = Depends(get_db)):
    measurement = db.get(models.Measurement, measurement_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    db.delete(measurement)
    db.commit()
    return {"status": "deleted"}


# Links
@app.get("/links", response_model=list[schemas.Link])
def list_links(db: Session = Depends(get_db)):
    return db.query(models.Link).order_by(models.Link.link_id).all()


@app.post("/links", response_model=schemas.Link)
def create_link(payload: schemas.LinkCreate, db: Session = Depends(get_db)):
    link = models.Link(**payload.model_dump())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@app.put("/links/{link_id}", response_model=schemas.Link)
def update_link(link_id: int, payload: schemas.LinkUpdate, db: Session = Depends(get_db)):
    link = db.get(models.Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(link, key, value)
    db.commit()
    db.refresh(link)
    return link


@app.delete("/links/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db)):
    link = db.get(models.Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return {"status": "deleted"}


# Compare tables
@app.get("/compare-tables", response_model=list[schemas.CompareTable])
def list_compare_tables(db: Session = Depends(get_db)):
    return db.query(models.CompareTable).order_by(models.CompareTable.compare_table_id).all()


@app.post("/compare-tables", response_model=schemas.CompareTable)
def create_compare_table(payload: schemas.CompareTableCreate, db: Session = Depends(get_db)):
    table = models.CompareTable(**payload.model_dump())
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@app.put("/compare-tables/{compare_table_id}", response_model=schemas.CompareTable)
def update_compare_table(compare_table_id: int, payload: schemas.CompareTableUpdate, db: Session = Depends(get_db)):
    table = db.get(models.CompareTable, compare_table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Compare table not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(table, key, value)
    db.commit()
    db.refresh(table)
    return table


# Compare table lines
@app.get("/compare-table-lines", response_model=list[schemas.CompareTableLine])
def list_compare_table_lines(db: Session = Depends(get_db)):
    return db.query(models.CompareTableLine).order_by(models.CompareTableLine.compare_line_id).all()


@app.post("/compare-table-lines", response_model=schemas.CompareTableLine)
def create_compare_table_line(payload: schemas.CompareTableLineCreate, db: Session = Depends(get_db)):
    line = models.CompareTableLine(**payload.model_dump())
    db.add(line)
    db.commit()
    db.refresh(line)
    return line


@app.put("/compare-table-lines/{compare_line_id}", response_model=schemas.CompareTableLine)
def update_compare_table_line(compare_line_id: int, payload: schemas.CompareTableLineUpdate, db: Session = Depends(get_db)):
    line = db.get(models.CompareTableLine, compare_line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Compare line not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(line, key, value)
    db.commit()
    db.refresh(line)
    return line


# Contracts
@app.get("/contracts", response_model=list[schemas.Contract])
def list_contracts(db: Session = Depends(get_db)):
    return db.query(models.Contract).order_by(models.Contract.contract_id).all()


@app.post("/contracts", response_model=schemas.Contract)
def create_contract(payload: schemas.ContractCreate, db: Session = Depends(get_db)):
    contract = models.Contract(**payload.model_dump())
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


@app.put("/contracts/{contract_id}", response_model=schemas.Contract)
def update_contract(contract_id: int, payload: schemas.ContractUpdate, db: Session = Depends(get_db)):
    contract = db.get(models.Contract, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(contract, key, value)
    db.commit()
    db.refresh(contract)
    return contract


# Contract lines
@app.get("/contract-lines", response_model=list[schemas.ContractLine])
def list_contract_lines(db: Session = Depends(get_db)):
    return db.query(models.ContractLine).order_by(models.ContractLine.contract_line_id).all()


@app.post("/contract-lines", response_model=schemas.ContractLine)
def create_contract_line(payload: schemas.ContractLineCreate, db: Session = Depends(get_db)):
    line = models.ContractLine(**payload.model_dump())
    db.add(line)
    db.commit()
    db.refresh(line)
    return line


@app.put("/contract-lines/{contract_line_id}", response_model=schemas.ContractLine)
def update_contract_line(contract_line_id: int, payload: schemas.ContractLineUpdate, db: Session = Depends(get_db)):
    line = db.get(models.ContractLine, contract_line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Contract line not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(line, key, value)
    db.commit()
    db.refresh(line)
    return line


# Tolerances
@app.get("/tolerances", response_model=list[schemas.Tolerance])
def list_tolerances(db: Session = Depends(get_db)):
    return db.query(models.Tolerance).order_by(models.Tolerance.tolerance_id).all()


@app.post("/tolerances", response_model=schemas.Tolerance)
def create_tolerance(payload: schemas.ToleranceCreate, db: Session = Depends(get_db)):
    tolerance = models.Tolerance(**payload.model_dump())
    db.add(tolerance)
    db.commit()
    db.refresh(tolerance)
    return tolerance


@app.put("/tolerances/{tolerance_id}", response_model=schemas.Tolerance)
def update_tolerance(tolerance_id: int, payload: schemas.ToleranceUpdate, db: Session = Depends(get_db)):
    tolerance = db.get(models.Tolerance, tolerance_id)
    if not tolerance:
        raise HTTPException(status_code=404, detail="Tolerance not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tolerance, key, value)
    db.commit()
    db.refresh(tolerance)
    return tolerance


# Test methods
@app.get("/test-methods", response_model=list[schemas.TestMethod])
def list_test_methods(db: Session = Depends(get_db)):
    return db.query(models.TestMethod).order_by(models.TestMethod.method_id).all()


@app.post("/test-methods", response_model=schemas.TestMethod)
def create_test_method(payload: schemas.TestMethodCreate, db: Session = Depends(get_db)):
    method = models.TestMethod(**payload.model_dump())
    db.add(method)
    db.commit()
    db.refresh(method)
    return method


@app.put("/test-methods/{method_id}", response_model=schemas.TestMethod)
def update_test_method(method_id: int, payload: schemas.TestMethodUpdate, db: Session = Depends(get_db)):
    method = db.get(models.TestMethod, method_id)
    if not method:
        raise HTTPException(status_code=404, detail="Test method not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(method, key, value)
    db.commit()
    db.refresh(method)
    return method


# Tech tasks
@app.get("/tech-tasks", response_model=list[schemas.TechTask])
def list_tech_tasks(db: Session = Depends(get_db)):
    return db.query(models.TechTask).order_by(models.TechTask.tech_task_id).all()


# Effective params/methods
@app.get("/product-nodes/{product_node_id}/effective-params", response_model=list[schemas.EffectiveParam])
def get_effective_params(product_node_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text(
            """
            SELECT ep.product_node_id, ep.param_id, ep.is_required,
                   pc.param_code, pc.param_name, pc.uom_default
            FROM effective_params ep
            JOIN params_catalog pc ON pc.param_id = ep.param_id
            WHERE ep.product_node_id = :product_node_id
            ORDER BY pc.param_id
            """
        ),
        {"product_node_id": product_node_id},
    ).mappings()
    return [schemas.EffectiveParam(**row) for row in rows]


@app.get("/product-nodes/{product_node_id}/effective-methods", response_model=list[schemas.EffectiveMethod])
def get_effective_methods(product_node_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text(
            """
            SELECT product_node_id, method_id, method_title, method_text
            FROM effective_methods
            WHERE product_node_id = :product_node_id
            ORDER BY method_id
            """
        ),
        {"product_node_id": product_node_id},
    ).mappings()
    return [schemas.EffectiveMethod(**row) for row in rows]


@app.get("/compare-tables/{compare_table_id}/matrix", response_model=schemas.CompareMatrixResponse)
def get_compare_matrix(compare_table_id: int, db: Session = Depends(get_db)):
    table = db.get(models.CompareTable, compare_table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Compare table not found")

    customer_model = db.get(models.CustomerModel, table.customer_model_id)
    if not customer_model:
        raise HTTPException(status_code=404, detail="Customer model not found")

    params = get_effective_params(customer_model.product_node_id, db)

    rows_query = db.execute(
        text(
            """
            SELECT l.link_id, l.supplier_model_id, f.name AS factory_name,
                   l.status, l.last_price_fob, l.currency
            FROM compare_table_lines ctl
            JOIN links l ON l.link_id = ctl.link_id
            JOIN supplier_models sm ON sm.supplier_model_id = l.supplier_model_id
            JOIN factories f ON f.factory_id = sm.factory_id
            WHERE ctl.compare_table_id = :compare_table_id
            ORDER BY ctl.compare_line_id
            """
        ),
        {"compare_table_id": compare_table_id},
    ).mappings()

    rows = []
    for row in rows_query:
        values: dict[str, Any] = {}
        for param in params:
            measurement = db.execute(
                text(
                    """
                    SELECT value
                    FROM measurements
                    WHERE supplier_model_id = :supplier_model_id
                      AND param_id = :param_id
                    ORDER BY measured_at DESC
                    LIMIT 1
                    """
                ),
                {"supplier_model_id": row["supplier_model_id"], "param_id": param.param_id},
            ).scalar()
            values[str(param.param_id)] = measurement
        rows.append(
            schemas.CompareMatrixRow(
                link_id=row["link_id"],
                supplier_model_id=row["supplier_model_id"],
                factory_name=row["factory_name"],
                status=row["status"],
                last_price_fob=row["last_price_fob"],
                currency=row["currency"],
                values=values,
            )
        )
    return schemas.CompareMatrixResponse(params=params, rows=rows)


@app.post("/compare-tables/{compare_table_id}/send")
def send_compare_to_engineer(compare_table_id: int, db: Session = Depends(get_db)):
    table = db.get(models.CompareTable, compare_table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Compare table not found")
    table.status = "sent"
    table.sent_to_engineer_at = datetime.utcnow()
    db.commit()
    return {"status": "sent"}


@app.post("/contracts/{contract_id}/generate-tech-task", response_model=schemas.TechTaskResponse)
def generate_tech_task(contract_id: int, db: Session = Depends(get_db)):
    contract = db.get(models.Contract, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract_lines = db.query(models.ContractLine).filter_by(contract_id=contract_id).all()
    if not contract_lines:
        raise HTTPException(status_code=400, detail="Contract has no lines")

    latest_version = (
        db.query(models.TechTask)
        .filter_by(contract_id=contract_id)
        .order_by(models.TechTask.version.desc())
        .first()
    )
    next_version = 1 if not latest_version else latest_version.version + 1

    content_blocks = [
        f"# Tech Task: {contract.contract_code}",
        f"Factory ID: {contract.factory_id}",
        f"Generated at: {datetime.utcnow().isoformat()} | Version {next_version}",
        "",
    ]

    for line in contract_lines:
        link = db.get(models.Link, line.link_id)
        customer_model = db.get(models.CustomerModel, link.customer_model_id)
        supplier_model = db.get(models.SupplierModel, link.supplier_model_id)
        factory = db.get(models.Factory, supplier_model.factory_id)

        content_blocks.append(f"## Line {line.contract_line_id}")
        content_blocks.append(
            f"SKU: {customer_model.customer_sku} — {customer_model.name} | Qty: {line.qty} | Region: {line.region or '-'}"
        )
        content_blocks.append(f"Supplier model: {supplier_model.factory_model_name} (Factory: {factory.name})")
        content_blocks.append("")
        content_blocks.append("**BM Requirements**")
        content_blocks.append(customer_model.bm_requirements_text or "-")
        content_blocks.append("")

        accessories = (
            db.query(models.CustomerModelAccessory)
            .filter_by(customer_model_id=customer_model.customer_model_id)
            .all()
        )
        if accessories:
            content_blocks.append("**Accessories**")
            for accessory in accessories:
                accessory_item = db.get(models.Accessory, accessory.accessory_id)
                content_blocks.append(
                    f"- {accessory_item.accessory_name} (PN {accessory_item.part_number}) x{accessory.qty}"
                )
            content_blocks.append("")

        params = get_effective_params(customer_model.product_node_id, db)
        methods = get_effective_methods(customer_model.product_node_id, db)

        content_blocks.append("**Parameters**")
        content_blocks.append("| Parameter | Value | UOM | Tolerance | Condition |")
        content_blocks.append("| --- | --- | --- | --- | --- |")
        for param in params:
            measurement = db.execute(
                text(
                    """
                    SELECT value, uom, condition_tag
                    FROM measurements
                    WHERE supplier_model_id = :supplier_model_id
                      AND param_id = :param_id
                    ORDER BY measured_at DESC
                    LIMIT 1
                    """
                ),
                {"supplier_model_id": supplier_model.supplier_model_id, "param_id": param.param_id},
            ).mappings().first()

            tolerance = db.query(models.Tolerance).filter_by(param_id=param.param_id).first()
            tolerance_rule = tolerance.tolerance_rule if tolerance else default_tolerance(param.param_code)

            value = measurement["value"] if measurement else "-"
            uom = measurement["uom"] if measurement else (param.uom_default or "-")
            condition = measurement["condition_tag"] if measurement else "-"

            content_blocks.append(
                f"| {param.param_name} | {value} | {uom} | {tolerance_rule} | {condition} |"
            )
        content_blocks.append("")

        if methods:
            content_blocks.append("**Test Methods**")
            for method in methods:
                content_blocks.append(f"- {method.method_title}: {method.method_text}")
            content_blocks.append("")

    content = "\n".join(content_blocks)
    tech_task = models.TechTask(
        contract_id=contract_id,
        version=next_version,
        status="generated",
        content=content,
    )
    db.add(tech_task)
    db.commit()
    db.refresh(tech_task)

    return schemas.TechTaskResponse(
        tech_task_id=tech_task.tech_task_id,
        version=tech_task.version,
        content=tech_task.content,
    )


def default_tolerance(param_code: str) -> str:
    if param_code in {"VOLTAGE", "CURRENT"}:
        return "±5%"
    if param_code == "PF":
        return "±0.02"
    if param_code == "DUTY":
        return ">= measured - 5% abs"
    return "default"
