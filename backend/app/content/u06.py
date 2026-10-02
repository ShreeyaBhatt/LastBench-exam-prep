"""Unit 6 - Routing in the Network Layer (PB Q262-Q295).

{{dijkstra:SRC:EDGES}} and {{bellman:SRC:EDGES}} placeholders are expanded by
app.solver into step tables, so the steps always match the graph.
"""

TITLE = "Routing Algorithms"
SOURCE = "Practice book Unit 6 (not covered in T1 notes; standard Forouzan / Kurose content)"

NOTES = {
    "summary": "How routers build forwarding tables: Dijkstra (link state), Bellman-Ford (distance vector), their protocols, and the problems each one has.",
    "sections": [
        {"h": "Forwarding", "points": [
            "Routing table = **routes to use for forwarding data** to each destination (prefix -> next hop / interface).",
            "**Host-specific** forwarding stores full host addresses; **network-specific** stores network prefixes; **next-hop** stores only the next router; **default** route catches the rest.",
            "**Longest prefix match**: if several entries match, use the one with the longest mask.",
            "**Address aggregation** (supernetting) keeps tables small in **classless (CIDR)** addressing. /24 in 223.1.1.0/24 is **CIDR notation** (prefix length).",
            "The routing processor performs **network-layer** functions. `route` command edits the routing table; `traceroute` counts hops.",
        ]},
        {"h": "Link state routing (Dijkstra)", "points": [
            "Each router floods **LSPs** describing **its neighbourhood** (its links and costs) to all routers, so everyone gets the **whole map**.",
            "Each router runs **Dijkstra** to build a shortest-path tree. Protocol: **OSPF** (intradomain).",
            "Dijkstra: set D(source)=0, others infinity. Repeatedly pick the unvisited node with the smallest D, add it to N', relax its neighbours: D(v) = min(D(v), D(w) + c(w,v)).",
            "Updates sent when something changes (plus periodic refresh). Converges fast; no count-to-infinity.",
        ]},
        {"h": "Distance vector routing (Bellman-Ford)", "points": [
            "Each router knows only costs to its **neighbours** and shares its whole **distance vector** with them **periodically**.",
            "Bellman-Ford equation: **Dx(y) = min over neighbours v { c(x,v) + Dv(y) }**.",
            "Protocol: **RIP** (hop count, max 15). Simple but slow to converge.",
            "**Count-to-infinity**: after a link fails, two routers keep bouncing stale routes, increasing the cost slowly. Fixes: split horizon, poison reverse, hold-down.",
        ]},
        {"h": "Multicast", "points": [
            "**Flooding** broadcasts packets but creates loops (fixed by RPF / spanning trees).",
            "Each router builds a **shortest-path tree** per group (source-based tree) or uses a shared group tree.",
            "Interdomain routing uses **BGP** (path vector).",
        ]},
    ],
    "formulas": [
        ["Dijkstra relaxation", "D(v) = min( D(v), D(w) + c(w,v) )"],
        ["Bellman-Ford", "Dx(y) = min_v { c(x,v) + Dv(y) }"],
        ["Natural masks", "A /8 255.0.0.0, B /16 255.255.0.0, C /24 255.255.255.0"],
    ],
    "traps": [
        "Link state: router sends info about its neighbours, but to everyone. Distance vector: sends info about everyone, but to neighbours only.",
        "Distance vector updates are periodic; OSPF (link state) is the one triggered by change.",
        "In Dijkstra tables, once a node enters N' its distance is final.",
        "A link is 'unused' only if it is on no shortest path between any pair of routers.",
    ],
}

NUMERICAL = set(range(277, 296))

G = {
    277: "0-1:2 0-2:6 1-3:5 2-3:8 3-5:15 3-4:10 5-4:6 5-6:6 4-6:2",
    278: "E-D:2 D-B:2 C-B:5 E-F:1 D-F:2 E-A:4 D-A:3 A-B:3",
    279: "U-T:4 T-P:1 T-R:5 U-Q:3 Q-P:1 P-S:2 Q-S:3 R-S:2",
    280: "P-Q:1 P-O:2 P-M:4 Q-L:3 M-L:1 M-N:3 O-N:2 N-L:5 N-R:1",
    281: "x-z:8 z-y:12 x-y:6 y-t:7 y-v:8 x-v:3 x-w:6 v-t:4 v-w:4 v-u:3 t-u:2 w-u:3",
    282: "u-v:1 u-y:2 v-x:3 y-x:3 v-z:6 x-z:2",
    283: "A-B:2 A-C:5 A-D:1 B-C:3 B-D:2 D-C:3 C-E:1 D-E:1 C-F:5 E-F:2",
    284: "A-C:3 A-D:8 B-E:2 C-E:1 D-E:2 C-F:6",
    286: "R1-R2:6 R1-R3:3 R2-R3:2 R2-R4:7 R3-R5:9 R4-R5:1 R4-R6:8 R5-R6:4",
    287: "A-B:5 A-C:10 B-C:3 B-D:11 C-D:2",
    288: "A-B:1 A-C:1 A-E:1 A-F:1 B-C:1 C-D:1 D-G:1 F-G:1",
    289: "A-C:2 A-D:10 C-D:1 C-F:18 D-F:6 B-D:2 B-E:1 D-E:11 E-F:2",
    290: "1-3:2 1-4:5 1-2:3 2-4:1 3-4:2 3-6:1 4-5:3 2-5:4 5-6:2",
    291: "A-C:3 A-D:8 B-E:2 C-E:1 D-E:2 C-F:6",
    292: "A-B:4 A-C:8 B-D:8 B-C:11 C-E:7 C-F:1 D-E:2 E-F:6 D-G:7 D-H:4 F-H:2 G-I:9 G-H:14 H-I:10",
    293: "A-B:2 A-D:3 B-C:5 B-E:4 D-E:5 E-F:2 C-F:4 C-G:3 F-G:1",
    294: "D-C:11 D-A:1 D-B:7 A-B:2 C-B:3",
    295: "A-B:4 A-D:6 B-F:12 B-G:22 B-C:4 D-C:3 C-G:16 C-E:14 F-E:8 F-G:12 E-G:6",
}


def dj(src, q):
    return "{{dijkstra:%s:%s}}" % (src, G[q].replace(" ", ","))


def bf(src, q):
    return "{{bellman:%s:%s}}" % (src, G[q].replace(" ", ","))


SOL = {
    262: "Count-to-infinity occurs in **distance vector routing**: routers only know neighbours' distances, so after a failure they keep advertising stale routes to each other.",
    263: "Dijkstra's algorithm, distance vector routing and link state routing can **all** be used in network-layer design.",
    264: "A routing table keeps the **routes to use for forwarding data to its destination** (destination -> next hop / interface).",
    265: "The **route** command displays and manipulates the TCP/IP routing table (route add / delete / print).",
    266: "In **host-specific** forwarding the table holds the full IP address of each destination host.",
    267: "Address aggregation (route summarization) was designed for **classless addressing (CIDR)**, where many small blocks would otherwise each need an entry.",
    268: "The routing processor runs routing protocols and builds tables: **network layer** functions.",
    269: "/24 is **CIDR** (prefix-length) notation: 24 network bits.",
    270: "**Flooding** sends a copy out of every interface; it reaches everyone but creates loops and duplicates.",
    271: "Natural (default) Class C mask = **255.255.255.0**.",
    272: "In multicast routing each router builds a **shortest** path tree for each group.",
    273: "OSPF is based on **link state** routing (each router runs Dijkstra on the full map).",
    274: "In distance vector routing (e.g. RIP every 30 s), updates are sent **periodically**.",
    275: "Link state routers use the **Dijkstra algorithm** to compute shortest paths. OSPF is the protocol, not the algorithm.",
    276: "In link state routing an LSP carries the router's knowledge of **its neighbourhood** (its links and their costs), flooded to every router.",
    277: ("0-1 2, 0-2 6, 0-1-3 7, 0-1-3-4 17, 0-1-3-4-6 19, 0-1-3-5 22", "Dijkstra from node **0**:\n\n" + dj("0", 277)),
    278: ("B 3, C 8, D 3, E 4, F 5", "Edges are drawn without arrows, so they are treated as two-way. Dijkstra from **A**:\n\n" + dj("A", 278)),
    279: ("P 1, T 2, S 3, U 3, R 5", "Distance vector / Bellman-Ford from **Q**. Each round, every node's estimate is improved using its neighbours' estimates from the previous round:\n\n" + bf("Q", 279)),
    280: ("R 1, O 2, M 3, L 4, P 4, Q 5", "Bellman-Ford from **N** (iteration k = best paths using at most k links):\n\n" + bf("N", 280)),
    281: ("v 3, u 6, w 6, y 6, t 7, z 8", "Dijkstra from **x** (Kurose textbook network):\n\n" + dj("x", 281)),
    282: ("Dz: u 6, v 5, x 2, y 5", """Node z has neighbours **v (cost 6)** and **x (cost 2)**.

**Initially** z knows only its links: Dz = (u inf, v 6, x 2, y inf, z 0).

**After receiving neighbours' vectors** (Dv = (u 1, v 0, x 3, y 3); Dx = (u 4, v 3, x 0, y 3)), z applies Dz(y) = min(c(z,v) + Dv(y), c(z,x) + Dx(y)):

| Dest | via v (6 + Dv) | via x (2 + Dx) | **Dz** | Next hop |
|---|---|---|---|---|
| u | 6 + 1 = 7 | 2 + 4 = 6 | **6** | x |
| v | 6 + 0 = 6 | 2 + 3 = 5 | **5** | x |
| x | 6 + 3 = 9 | 2 + 0 = 2 | **2** | x |
| y | 6 + 3 = 9 | 2 + 3 = 5 | **5** | x |

Check with Bellman-Ford from z:

""" + bf("z", 282)),
    283: ("B 2, D 1, E 2, C 3, F 4", "Link state routing = each router floods its links, then runs Dijkstra on the full map. From **A**:\n\n" + dj("A", 283)),
    284: ("C 3, E 4, B 6, D 6, F 9", "No source is named; take **A**. Dijkstra:\n\n" + dj("A", 284)),
    285: ("N3 = (3, 2, 0, 2, 5)", """After the change, N2 and N3 set their direct entry to 2:
- N2 = (1, 0, **2**, 7, 3)
- N4 = (8, 7, 2, 0, 4) (unchanged)

N3's neighbours are N2 (cost 2) and N4 (cost 2). N3 recomputes each entry:

| Dest | via N2: 2 + D_N2 | via N4: 2 + D_N4 | **New D_N3** |
|---|---|---|---|
| N1 | 2 + 1 = 3 | 2 + 8 = 10 | **3** |
| N2 | 2 + 0 = 2 | 2 + 7 = 9 | **2** |
| N3 | - | - | **0** |
| N4 | 2 + 7 = 9 | 2 + 0 = 2 | **2** |
| N5 | 2 + 3 = 5 | 2 + 4 = 6 | **5** |

New distance vector at N3 = **(3, 2, 0, 2, 5)**"""),
    286: ("2 links (R1-R2 and R4-R6)", """Find every router pair's shortest path and mark the links they use. Example from R1:

""" + dj("R1", 286) + """

Doing this for every source:
- **R1-R2 (6)** is never used: R1-R3-R2 costs 3 + 2 = 5 < 6.
- **R4-R6 (8)** is never used: R4-R5-R6 costs 1 + 4 = 5 < 8.
- All other links lie on some shortest path.

Links never used = **2**"""),
    287: ("A-B-C-D, cost 10", "Dijkstra from **A**:\n\n" + dj("A", 287) + "\n\nShortest path A to D = **A - B - C - D**, cost 5 + 3 + 2 = **10** (direct A-C-D costs 12, A-B-D costs 16)."),
    288: ("From A: B 1, C 1, E 1, F 1, D 2 (via C), G 2 (via F)", "Distance vector from **A** (all link costs 1):\n\n" + bf("A", 288) + "\n\nEach other router builds its own table the same way by exchanging vectors with its neighbours."),
    289: ("From A: C 2, D 3, B 5, E 6, F 8", "Distance vector from **A**:\n\n" + bf("A", 289) + "\n\nNotice how the direct A-D link (10) and C-F (18) lose to multi-hop paths after a few exchanges."),
    290: ("From 1: 3 2, 2 3, 6 3, 4 4, 5 5", "Distance vector from node **1**:\n\n" + bf("1", 290)),
    291: ("Before: A to E = 4 via C. After failure: A to E = 10 via D", """**Before failure** (Dijkstra from A):

""" + dj("A", 291) + """

**When C-E fails**
- C sets its entry for E to **infinity** (it was the direct link); E sets its entry for C to infinity.
- C sends its new vector to its neighbours **A and F**; E sends its new vector to **B and D**.
- C's routes to B and D (which went through E) also become invalid and are recomputed from neighbours.

**A's table after C and E have reported** (A now reaches E through D):

{{bellman:A:A-C:3,A-D:8,B-E:2,D-E:2,C-F:6}}

| Dest | Cost | Next hop |
|---|---|---|
| B | 12 | D |
| C | 3 | C |
| D | 8 | D |
| E | 10 | D |
| F | 9 | C |"""),
    292: ("From A: B 4, C 8, F 9, H 11, D 12, E 14, G 19, I 21", "Taking **A** as the source, distance vector (Bellman-Ford) gives:\n\n" + bf("A", 292)),
    293: ("From A: B 2, D 3, E 6, C 7, F 8, G 9", "Link state = Dijkstra on the full map. From **A**:\n\n" + dj("A", 293)),
    294: ("From C: B 3, A 5, D 6", "Distance vector from **C**:\n\n" + bf("C", 294) + "\n\nC reaches D more cheaply through B and A (3 + 2 + 1 = 6) than through the direct link (11)."),
    295: ("B 4, D 6, C 8, F 16, E 22, G 24", "Dijkstra from **A**:\n\n" + dj("A", 295)),
}
