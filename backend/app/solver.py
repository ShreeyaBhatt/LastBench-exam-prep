"""Generates worked steps (CRC long division, Dijkstra, Bellman-Ford) for solutions.

Solutions embed placeholders such as {{crc:DIVIDEND:GEN}} or
{{dijkstra:SRC:A-B:2,B-C:3}}; expand() replaces them with markdown so the
steps shown to students are always computed from the actual numbers.
"""

import heapq
import re

INF = float("inf")


def crc_division(dividend: str, gen: str) -> str:
    bits = list(dividend)
    r = len(gen) - 1
    lines = ["  " + "".join(bits)]
    for i in range(len(bits) - r):
        if bits[i] != "1":
            continue
        lines.append("^ " + " " * i + gen)
        for j, g in enumerate(gen):
            bits[i + j] = str(int(bits[i + j]) ^ int(g))
        lines.append("  " + "-" * len(bits))
        lines.append("  " + "".join(bits))
    lines.append("  " + " " * (len(bits) - r) + "^" * r + "  remainder")
    return "```\n" + "\n".join(lines) + "\n```"


def parse_graph(spec: str) -> dict:
    g: dict = {}
    for edge in spec.split(","):
        uv, w = edge.rsplit(":", 1)
        u, v = uv.split("-")
        g.setdefault(u, {})[v] = int(w)
        g.setdefault(v, {})[u] = int(w)
    return g


def _key(n):
    return (0, int(n)) if n.isdigit() else (1, n)


def _fmt(d):
    return "inf" if d == INF else str(int(d))


def _path(prev, v):
    out = []
    while v is not None:
        out.append(v)
        v = prev[v]
    return " - ".join(reversed(out))


def dijkstra_table(src: str, spec: str) -> str:
    g = parse_graph(spec)
    nodes = sorted(g, key=_key)
    others = [n for n in nodes if n != src]
    dist = {n: INF for n in nodes}
    prev = {n: None for n in nodes}
    dist[src] = 0
    done: list = []
    rows = []
    pq = [(0, _key(src), src)]
    while pq:
        d, _, u = heapq.heappop(pq)
        if u in done:
            continue
        done.append(u)
        for v, w in g[u].items():
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], _key(v), v))
        cells = []
        for n in others:
            if n in done and n != u:
                cells.append("")
            elif dist[n] == INF:
                cells.append("inf")
            else:
                cells.append(f"{_fmt(dist[n])}, {prev[n]}")
        rows.append((len(done) - 1, ", ".join(done), cells))

    head = "| Step | N' | " + " | ".join(f"D({n}), p({n})" for n in others) + " |"
    sep = "|---|---|" + "---|" * len(others)
    body = "\n".join(f"| {s} | {np} | " + " | ".join(c) + " |" for s, np, c in rows)
    final = "\n".join(f"| {n} | {_fmt(dist[n])} | {_path(prev, n)} |" for n in others)
    return (
        f"{head}\n{sep}\n{body}\n\n"
        "A blank cell means that node is already in N' (its distance is final).\n\n"
        f"**Shortest paths from {src}**\n\n| Destination | Cost | Path |\n|---|---|---|\n{final}"
    )


def bellman_table(src: str, spec: str) -> str:
    g = parse_graph(spec)
    nodes = sorted(g, key=_key)
    others = [n for n in nodes if n != src]
    dist = {n: INF for n in nodes}
    prev = {n: None for n in nodes}
    dist[src] = 0
    rows = [[_fmt(dist[n]) for n in others]]
    for _ in range(len(nodes) - 1):
        new = dict(dist)
        newprev = dict(prev)
        for v in nodes:
            for u, w in g[v].items():
                if dist[u] + w < new[v]:
                    new[v] = dist[u] + w
                    newprev[v] = u
        if new == dist:
            break
        dist, prev = new, newprev
        rows.append([_fmt(dist[n]) for n in others])

    head = "| Iteration | " + " | ".join(others) + " |"
    sep = "|---|" + "---|" * len(others)
    body = "\n".join(f"| {i} | " + " | ".join(r) + " |" for i, r in enumerate(rows))
    final = "\n".join(
        f"| {n} | {_fmt(dist[n])} | {_path(prev, n).split(' - ')[1] if dist[n] not in (0, INF) else '-'} | {_path(prev, n)} |"
        for n in others
    )
    return (
        f"{head}\n{sep}\n{body}\n\n"
        f"Iteration k holds the best cost using at most k links. Values stop changing after iteration {len(rows) - 1}, so the tables have converged.\n\n"
        f"**Routing table at {src}**\n\n| Destination | Cost | Next hop | Path |\n|---|---|---|---|\n{final}"
    )


_PATTERN = re.compile(r"\{\{(crc|dijkstra|bellman):([^:}]+):([^}]+)\}\}")


def expand(text: str) -> str:
    def sub(m):
        kind, a, b = m.groups()
        if kind == "crc":
            return crc_division(a, b)
        if kind == "dijkstra":
            return dijkstra_table(a, b)
        return bellman_table(a, b)

    return _PATTERN.sub(sub, text)
