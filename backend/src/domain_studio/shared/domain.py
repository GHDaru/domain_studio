"""Blocos de construção de base do DDD, sem dependência de framework."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


class DomainError(Exception):
    """Violação de uma regra ou invariante de domínio."""


def new_id() -> str:
    return uuid.uuid4().hex


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    """Fato ocorrido no domínio. Imutável."""

    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(eq=False, kw_only=True)
class Entity:
    """Objeto definido pela identidade: igualdade compara apenas `id`."""

    id: str = field(default_factory=new_id)

    def __eq__(self, other: object) -> bool:
        return type(other) is type(self) and other.id == self.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))


@dataclass(eq=False, kw_only=True)
class AggregateRoot(Entity):
    """Raiz de agregado: acumula eventos de domínio até serem publicados."""

    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events
