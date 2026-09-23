from dataclasses import dataclass

from domain_studio.shared.domain import AggregateRoot, DomainEvent, Entity


@dataclass(eq=False, kw_only=True)
class Coisa(Entity):
    nome: str


@dataclass(frozen=True, kw_only=True)
class CoisaCriada(DomainEvent):
    coisa_id: str


def test_entities_are_equal_by_identity_only() -> None:
    a = Coisa(id="1", nome="x")
    b = Coisa(id="1", nome="y")
    c = Coisa(id="2", nome="x")

    assert a == b
    assert a != c
    assert len({a, b, c}) == 2


def test_aggregate_root_collects_and_releases_events() -> None:
    root = AggregateRoot()
    root.record(CoisaCriada(coisa_id=root.id))

    events = root.pull_events()

    assert [type(e) for e in events] == [CoisaCriada]
    assert root.pull_events() == []
