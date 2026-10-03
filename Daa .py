import sys
sys.setrecursionlimit(10000)


def find_bridges(n, edges):
    """Return the indices of bridge edges. O(N + M)."""
    graph = [[] for _ in range(n)]
    for idx, (u, v) in enumerate(edges):
        graph[u].append((v, idx))
        graph[v].append((u, idx))

    disc = [-1] * n
    low = [0] * n
    bridges = []
    timer = [0]

    def dfs(node, parent_edge):
        disc[node] = low[node] = timer[0]
        timer[0] += 1
        for nxt, idx in graph[node]:
            if idx == parent_edge:          # skip the link we arrived by
                continue
            if disc[nxt] == -1:             # tree edge
                dfs(nxt, idx)
                low[node] = min(low[node], low[nxt])
                if low[nxt] > disc[node]:   # no other route back
                    bridges.append(idx)
            else:                           # back edge (a loop)
                low[node] = min(low[node], disc[nxt])

    for s in range(n):
        if disc[s] == -1:
            dfs(s, -1)
    return sorted(bridges)


def components(n, edges, skip):
    """Union-Find: label each tower with its connected part."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, (u, v) in enumerate(edges):
        if i not in skip:
            parent[find(u)] = find(v)
    return [find(i) for i in range(n)]


def backup_links_needed(n, edges, bridges):
    """ceil(leaves / 2) of the bridge tree."""
    comp = components(n, edges, set(bridges))
    degree = {}
    for i in bridges:
        for c in (comp[edges[i][0]], comp[edges[i][1]]):
            degree[c] = degree.get(c, 0) + 1
    leaves = sum(1 for d in degree.values() if d == 1)
    return (leaves + 1) // 2


def report(n, edges):
    b = find_bridges(n, edges)
    score = round(100 * (1 - len(b) / len(edges))) if edges else 100
    return [edges[i] for i in b], score, backup_links_needed(n, edges, b)


if __name__ == "__main__":
    n = 8
    edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4),
             (4, 5), (5, 3), (5, 6), (6, 7)]
    bridges, score, backups = report(n, edges)
    print("Critical links:", bridges)
    print("Resilience score:", score)
    print("Backup links needed:", backups)