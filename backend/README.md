# DomainStudio — Backend (FastAPI)

Estrutura e marcos em [`../docs/plano-de-implementacao.md`](../docs/plano-de-implementacao.md).

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

uvicorn domain_studio.main:app --reload   # http://localhost:8000/docs
pytest
ruff check . && ruff format --check .
```
