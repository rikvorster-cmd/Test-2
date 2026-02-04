# MVP App (BM → PM → Engineer → Compare → Contract → Tech Task)

This repository contains a working MVP application with PostgreSQL, FastAPI, and Next.js.

## Stack

- **DB**: Postgres (preloaded schema + seed).
- **Backend**: FastAPI + SQLAlchemy + Alembic.
- **Frontend**: Next.js (minimal UI).

## Quick start

```bash
docker compose up --build
```

Services:

- Frontend: http://localhost:3000
- Backend Swagger: http://localhost:8000/docs

## Files

- `schema.sql` — tables + views for effective parameters and methods inheritance.
- `seed.sql` — minimal seed data (factories, product nodes, 10 parameters, tolerances, test methods).
- `docker-compose.yml` — runs db + backend + frontend.
- `backend/` — FastAPI app + Alembic baseline.
- `frontend/` — Next.js UI.

## End-to-end scenario (acceptance test)

1. **BM**: Open **SKU (Customer Models)** and create a SKU (select a product node, add BM requirements).
2. **BM**: In the same page, select the SKU and add accessories.
3. **PM**: Open **Supplier Models** and create a supplier model. Use **Inline create factory** if needed.
4. **Engineer**: In **Supplier Models**, select the supplier model and enter measurements for the effective params list.
5. **BM/PM**: Open **Links (Candidates)** and create a link between SKU and supplier model.
6. **BM**: Open **Compare Tables**, create a table for the SKU, add link rows, then **Send to Engineer**.
7. **Engineer**: In **Compare Tables**, enter priority/comments in the engineer review table.
8. **PM**: Open **Contracts & Tech Tasks**, create a contract, add contract lines (link + qty).
9. **PM**: Click **Generate Tech Task** and confirm a new Tech Task appears with markdown content.

## Notes

- The `effective_params` view aggregates parameters for each product node by traversing parent nodes and OR-ing the `is_required` flag.
- The `effective_methods` view aggregates test methods with the same inheritance logic.
