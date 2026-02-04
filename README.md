# MVP Schema & Seed Data

This repository contains the initial PostgreSQL schema and seed data for the MVP described in the specification.

## Files

- `schema.sql` — tables + views for effective parameters and methods inheritance.
- `seed.sql` — minimal seed data (factories, product nodes, 10 parameters, tolerances, test methods).

## Quick start

```bash
psql "$DATABASE_URL" -f schema.sql
psql "$DATABASE_URL" -f seed.sql
```

## Notes

- The `effective_params` view aggregates parameters for each product node by traversing parent nodes and OR-ing the `is_required` flag.
- The `effective_methods` view aggregates test methods with the same inheritance logic.
