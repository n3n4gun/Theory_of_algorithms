def solve_consistency(n, edges):
    parent = list(range(2 * n))
    rank = [0] * (2 * n)

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    def union(v1, v2):
        r1, r2 = find(v1), find(v2)
        if r1 == r2:
            return
        if rank[r1] < rank[r2]:
            parent[r1] = r2
        elif rank[r1] > rank[r2]:
            parent[r2] = r1
        else:
            parent[r2] = r1
            rank[r1] += 1

    for i, j, t in edges:
        if t == 'same':
            union(i, j)
            union(i + n, j + n)
        else:  # 'diff'
            union(i, j + n)
            union(i + n, j)

    for i in range(n):
        if find(i) == find(i + n):
            return False
    return True


if __name__ == "__main__":
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, t = input().split()
        a, b = int(a) - 1, int(b) - 1  # нумерация с 0
        edges.append((a, b, t))

    if solve_consistency(n, edges):
        print("Совместимо")
    else:
        print("Несовместимо")