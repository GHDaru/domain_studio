"""Ponto de entrada da API. Cada contexto delimitado registra seu router aqui."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="DomainStudio",
        version="0.1.0",
        description="Decompõe especificações de domínio em modelos DDD, diagramas e código.",
    )

    @app.get("/health", tags=["infra"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
