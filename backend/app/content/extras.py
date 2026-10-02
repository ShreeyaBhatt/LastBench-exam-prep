"""Syllabus topics the practice book does not cover, with notes and extra questions.

Ids 1000+ (1201 = unit 2, 1401 = unit 4, ...). Each question:
(id, kind, marks, text, options, answer_letter, answer_text, explanation)
"""

NOTES = {
    2: [{"h": "Data communication concepts (2.1)", "points": [
        "Data communication = exchange of data between two devices over a medium. Effectiveness depends on **delivery** (to the right destination), **accuracy**, **timeliness** (real-time data late is useless) and low **jitter** (uneven packet delay).",
        "Data representation: text (ASCII/Unicode bit patterns), numbers (binary), images (pixel bitmaps, RGB), audio and video (continuous or sampled signals).",
        "Line configuration: **point-to-point** (dedicated link) vs **multipoint** (shared link, spatially or temporally shared).",
    ]}],
    4: [{"h": "Channel allocation problem (4.1)", "points": [
        "How to allocate one broadcast channel among competing users.",
        "**Static allocation** (FDM/TDM): each of N users gets a fixed 1/N share. Wasteful for bursty traffic: idle shares cannot be used by others.",
        "Queueing delay on a channel: **T = 1 / (uC - lambda)**. Splitting into N static sub-channels makes delay **N times worse**: T_FDM = N x T.",
        "Dynamic allocation assumptions: independent traffic (station model), single shared channel, observable collisions, continuous or slotted time, carrier sense or no carrier sense.",
    ]}, {"h": "Collision-free protocols (4.2)", "points": [
        "**Bit-map (reservation)**: N contention slots per round; station j sets bit j if it has a frame, then stations send in numerical order. Efficiency: low load **d / (d + N)**, high load **d / (d + 1)**.",
        "**Token passing**: a token circulates (token ring / token bus); only the holder may send. No collisions; overhead = token time.",
        "**Binary countdown**: stations broadcast their address bit by bit (MSB first), bits are ORed on the channel; a station gives up when it sends 0 and hears 1. **Highest address wins.** Efficiency d / (d + log2 N).",
        "**Limited-contention** protocols (adaptive tree walk) mix contention at low load and collision-free at high load.",
    ]}],
    5: [{"h": "IPv6 (5.2)", "points": [
        "128-bit address, written as 8 groups of 4 hex digits: 2001:0DB8:0000:0000:0000:FF00:0042:8329.",
        "Abbreviation: drop leading zeros in each group; replace **one** run of all-zero groups with **::** (only once). Example: 2001:DB8::FF00:42:8329.",
        "Address types: **unicast**, **multicast**, **anycast** (nearest of a group). **No broadcast** in IPv6.",
        "**Base header fixed at 40 bytes**: Version (4) | Traffic class (8) | Flow label (20) | Payload length (16) | Next header (8) | Hop limit (8) | Source (128) | Destination (128).",
        "Removed vs IPv4: header checksum, fragmentation fields (moved to extension header; only the **source** fragments), options (now extension headers). TTL renamed **hop limit**.",
        "Transition IPv4 to IPv6: **dual stack** (both stacks), **tunneling** (IPv6 packet inside IPv4), **header translation** (NAT64, when one side speaks only IPv4).",
    ]}, {"h": "NAT (5.3)", "points": [
        "**Network Address Translation** lets many hosts with **private addresses** share one (or few) public IPs.",
        "Private ranges: **10.0.0.0/8**, **172.16.0.0/12** (172.16-172.31), **192.168.0.0/16**.",
        "Router rewrites the source IP (and port in **PAT/NAPT**) on the way out and keeps a **translation table** to map replies back.",
        "Types: static NAT (1-to-1), dynamic NAT (pool), PAT / overloading (many-to-1 using port numbers).",
        "Pros: saves IPv4 addresses, hides inside hosts. Cons: breaks end-to-end principle, problems for incoming connections and some protocols.",
    ]}],
    6: [{"h": "Flooding (6.1)", "points": [
        "Every incoming packet is sent out on **every line except the one it arrived on**.",
        "Generates huge numbers of duplicates. Controls: **hop counter** (decrement, discard at 0), **sequence numbers** to drop duplicates, **selective flooding** (only lines in roughly the right direction).",
        "Always finds the shortest path (it tries all paths in parallel) and is very robust, so used for broadcasting, link-state LSP distribution and military networks.",
    ]}],
    8: [{"h": "Congestion control (8.3)", "points": [
        "Congestion = too many packets for the network: queues overflow, delay and loss grow, throughput collapses.",
        "**Open loop** (prevent): retransmission, window, acknowledgement and discard policies, admission control. **Closed loop** (react): back pressure, choke packet, implicit and explicit signalling.",
        "**Leaky bucket**: output leaves at a constant rate; bursts are smoothed, excess dropped when the bucket is full.",
        "**Token bucket**: tokens added at rate rho up to capacity C; sending uses tokens, so bursts up to C are allowed. Max burst time **S = C / (M - rho)**, M = max output rate.",
        "TCP: **slow start** (cwnd doubles per RTT up to ssthresh), **congestion avoidance** (+1 MSS per RTT), **timeout**: ssthresh = cwnd/2, cwnd = 1 MSS; **3 duplicate ACKs** (Reno fast recovery): ssthresh = cwnd/2, cwnd = ssthresh. This is AIMD.",
    ]}],
    9: [{"h": "Principles of network applications (9.1)", "points": [
        "Application architectures: **client-server** (always-on server with fixed IP; data centres) and **P2P** (peers are both clients and servers; self-scalable, e.g. BitTorrent).",
        "Processes on different hosts communicate by sending **messages through sockets**; a process is addressed by **IP address + port**.",
        "Transport services an app may need: **reliable data transfer**, **throughput**, **timing**, **security**. Email/file transfer need reliability; telephony/games need timing.",
    ]}],
    10: [{"h": "Network design using Packet Tracer (10.1)", "points": [
        "Cisco Packet Tracer simulates routers, switches, PCs and cables. Drag devices, connect with the right cable, configure, then test with **ping** and **simulation mode**.",
        "Cables: **straight-through** for unlike devices (PC-switch, switch-router); **crossover** for like devices (PC-PC, switch-switch, PC-router). **Console** cable for CLI access.",
        "Router basics: `enable`, `configure terminal`, `interface g0/0`, `ip address 192.168.1.1 255.255.255.0`, `no shutdown`.",
        "Routing: static `ip route <net> <mask> <next-hop>`; RIP `router rip` + `network <net>`; OSPF `router ospf 1` + `network <net> <wildcard> area 0`.",
        "DHCP on a router: `ip dhcp excluded-address`, `ip dhcp pool`, `network`, `default-router`, `dns-server`.",
    ]}],
}

FORMULAS = {
    4: [["Queueing delay (one channel)", "T = 1 / (uC - lambda)"],
        ["Static FDM with N sub-channels", "T_FDM = N x T"],
        ["Bit-map efficiency", "low load d/(d+N), high load d/(d+1)"]],
    5: [["IPv6 base header", "40 bytes fixed"], ["IPv6 address", "128 bits = 8 groups of 16 bits (hex)"]],
    8: [["Token bucket burst length", "S = C / (M - rho)"], ["TCP timeout", "ssthresh = cwnd/2, cwnd = 1 MSS"]],
}

QUESTIONS = {
    2: [
        (1201, "mcq", 1, "The five components of a data communication system are:",
         ["Message, sender, receiver, transmission medium, protocol", "Sender, receiver, router, switch, cable",
          "Message, router, modem, medium, protocol", "Bits, bytes, frames, packets, segments"], "A",
         "Message, sender, receiver, transmission medium, protocol",
         "A data communication system has **message, sender, receiver, transmission medium and protocol**. Routers and switches are devices, not components of the model."),
        (1202, "theory", 3, "State the four fundamental characteristics that decide the effectiveness of a data communication system.",
         [], None, "Delivery, accuracy, timeliness, jitter",
         """1. **Delivery**: data must reach the correct destination and only the intended user.
2. **Accuracy**: data must arrive without alteration; corrupted data is unusable.
3. **Timeliness**: data must arrive in time. For real-time audio/video, late data is useless.
4. **Jitter**: variation in packet arrival time must stay low; uneven delay makes audio/video choppy."""),
    ],
    4: [
        (1401, "theory", 3, "What is the channel allocation problem? Compare static and dynamic channel allocation.",
         [], None, "Sharing one broadcast channel; static = fixed shares, dynamic = on demand",
         """The **channel allocation problem** is how to divide one shared broadcast channel among many competing users.

| Static allocation | Dynamic allocation |
|---|---|
| Channel split into fixed parts (FDM / TDM) | Channel given to whoever needs it, when needed |
| Each of N users gets 1/N of the bandwidth always | Users share the full bandwidth |
| Good for few users with steady traffic | Good for many users with bursty traffic |
| Idle shares are wasted; delay is N times worse | Needs a MAC protocol (ALOHA, CSMA, token) |

Assumptions for dynamic allocation: independent traffic, single channel, collisions observable, continuous or slotted time, carrier sense or not."""),
        (1402, "numerical", 3, "A 100 Mbps channel carries frames of mean length 10,000 bits arriving at 5000 frames/s. Find the mean delay T. If the channel is statically split into 10 equal FDM sub-channels, each with a tenth of the traffic, find the new delay.",
         [], None, "T = 200 us; with FDM, 2 ms",
         """**Single channel**
- Service rate uC = 100 x 10^6 / 10,000 = **10,000 frames/s**, lambda = 5000 frames/s
- T = 1 / (uC - lambda) = 1 / (10,000 - 5000) = **200 us**

**10 FDM sub-channels**
- Each: 10 Mbps -> uC = 1000 frames/s, lambda = 500 frames/s
- T_FDM = 1 / (1000 - 500) = **2 ms** = 10 x T

Static splitting makes the delay N times worse, which is why dynamic allocation is preferred for bursty traffic."""),
        (1403, "mcq", 1, "Which of these is NOT an assumption of dynamic channel allocation?",
         ["Independent traffic", "Single channel", "Observable collisions", "Every station has its own dedicated channel"], "D",
         "Every station has its own dedicated channel",
         "Dynamic allocation assumes a **single shared channel**. A dedicated channel per station is static allocation."),
        (1404, "theory", 4, "Explain collision-free protocols: bit-map, token passing and binary countdown.",
         [], None, "Reservation slots, circulating token, address bit arbitration",
         """**1. Bit-map (basic reservation)**
- Each round starts with N one-bit contention slots. Station j sets bit j if it has a frame.
- After the slots, stations with a 1 transmit in numerical order. No collisions.
- Efficiency: d/(d+N) at low load, d/(d+1) at high load.

**2. Token passing**
- A special frame (token) circulates around a logical ring. Only the station holding it may transmit, then it passes the token on.
- Used in Token Ring (802.5) and Token Bus (802.4). Fair, no collisions; the token must not be lost.

**3. Binary countdown**
- Stations broadcast their binary address MSB first; the channel ORs the bits.
- A station that sends 0 but hears 1 drops out. The **highest address wins**.
- Efficiency d/(d + log2 N); high-numbered stations get priority."""),
        (1405, "numerical", 3, "In binary countdown, stations 0010, 0100, 1001 and 1010 want the channel at the same time. Which station wins? Show each bit time.",
         [], None, "1010 wins",
         """| Bit time | 0010 | 0100 | 1001 | 1010 | Channel (OR) | Dropped |
|---|---|---|---|---|---|---|
| 1 (MSB) | 0 | 0 | 1 | 1 | 1 | 0010, 0100 (sent 0, heard 1) |
| 2 | - | - | 0 | 0 | 0 | none |
| 3 | - | - | 0 | 1 | 1 | 1001 |
| 4 | - | - | - | 0 | 0 | - |

Winner: **1010** (the highest address)."""),
        (1406, "numerical", 3, "A bit-map protocol has 32 stations and frames of 64 bits. Find the channel efficiency at low load and at high load.",
         [], None, "66.7% at low load, 98.5% at high load",
         """N = 32 contention bits per round, d = 64 data bits per frame.

- **Low load** (one frame per round): d / (d + N) = 64 / 96 = **66.7%**
- **High load** (all stations send): each frame carries 1 contention bit: d / (d + 1) = 64 / 65 = **98.5%**"""),
    ],
    5: [
        (1501, "mcq", 1, "What is the size of the IPv6 base header?",
         ["20 bytes", "32 bytes", "40 bytes", "60 bytes"], "C", "40 bytes",
         "The IPv6 base header is a **fixed 40 bytes**. Options are moved into extension headers, so the base size never changes (IPv4 is 20-60 bytes)."),
        (1502, "numerical", 2, "(a) Abbreviate 2001:0DB8:0000:0000:0000:FF00:0042:8329. (b) Expand 2001:db8::1 to full form.",
         [], None, "(a) 2001:DB8::FF00:42:8329 (b) 2001:0db8:0000:0000:0000:0000:0000:0001",
         """**(a)** Remove leading zeros in each group: 2001:DB8:0:0:0:FF00:42:8329. Replace the run of zero groups with `::` (once):
**2001:DB8::FF00:42:8329**

**(b)** The address has 3 written groups, so `::` stands for 8 - 3 = 5 zero groups. Pad each group to 4 digits:
**2001:0db8:0000:0000:0000:0000:0000:0001**"""),
        (1503, "theory", 4, "Draw the IPv6 base header and compare it with the IPv4 header.",
         [], None, "40-byte fixed header; no checksum, no fragmentation fields, flow label added",
         """```
| Ver (4) | Traffic class (8) |        Flow label (20)        |
|   Payload length (16)       | Next header (8) | Hop limit (8)|
|                Source address (128 bits)                     |
|             Destination address (128 bits)                   |
```

| IPv4 | IPv6 |
|---|---|
| 32-bit addresses | 128-bit addresses |
| Header 20-60 bytes (options) | Fixed 40-byte base header + extension headers |
| Header checksum | No checksum (left to link and transport layers) |
| Routers fragment (ID, flags, offset) | Only the source fragments (fragment extension header) |
| TTL | Hop limit |
| Type of service | Traffic class + **flow label** (for real-time flows) |
| Broadcast supported | No broadcast; multicast and anycast |
| Manual / DHCP config | Stateless auto-configuration too |"""),
        (1504, "theory", 3, "Explain the strategies for transition from IPv4 to IPv6.",
         [], None, "Dual stack, tunneling, header translation",
         """1. **Dual stack**: hosts and routers run IPv4 and IPv6 together; DNS tells which version the destination supports.
2. **Tunneling**: when two IPv6 hosts are separated by an IPv4-only region, the IPv6 packet is **encapsulated inside an IPv4 packet** (protocol 41) and decapsulated at the far end.
3. **Header translation**: when one end speaks only IPv4, a translator (e.g. NAT64) converts IPv6 headers to IPv4 and back."""),
        (1505, "mcq", 1, "Which IPv4 header field has no equivalent in the IPv6 base header?",
         ["Header checksum", "Source address", "Time to live", "Total length"], "A", "Header checksum",
         "IPv6 dropped the **header checksum** to speed up routing. TTL became hop limit, total length became payload length, and source address still exists."),
        (1506, "theory", 3, "What is NAT? Explain its types with an example.",
         [], None, "Translates private to public addresses; static, dynamic, PAT",
         """**Network Address Translation** maps private IP addresses inside a network to public addresses on the Internet, so many hosts can share few public IPs.

- Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.
- The NAT router rewrites the source address (and port) of outgoing packets and records the mapping in a **translation table**; replies are mapped back.

Types:
1. **Static NAT**: one private address always maps to one public address (servers).
2. **Dynamic NAT**: private addresses take a public address from a pool.
3. **PAT / NAPT (overloading)**: many private hosts share one public IP, told apart by port numbers. Used in home routers.

Example: 192.168.1.5:5000 -> 203.0.113.5:62001 on the way out."""),
        (1507, "numerical", 3, "Hosts 192.168.1.2 and 192.168.1.3 both use source port 3345 to reach 74.125.1.1:80 through a PAT router with public IP 203.0.113.5. The router assigns ports from 5001. Write the translation table and the destination of a reply arriving at 203.0.113.5:5002.",
         [], None, "Reply to 203.0.113.5:5002 goes to 192.168.1.3:3345",
         """| Inside (private) | Outside (public) | Destination |
|---|---|---|
| 192.168.1.2:3345 | 203.0.113.5:**5001** | 74.125.1.1:80 |
| 192.168.1.3:3345 | 203.0.113.5:**5002** | 74.125.1.1:80 |

Both hosts used port 3345, so PAT gives each a different public port. A reply to 203.0.113.5:5002 matches the second row and is forwarded to **192.168.1.3:3345**."""),
        (1508, "mcq", 1, "Which of these is a private IPv4 address?",
         ["172.32.1.1", "172.20.5.4", "192.169.1.1", "11.0.0.1"], "B", "172.20.5.4",
         "The private 172 range is **172.16.0.0 to 172.31.255.255** (172.16.0.0/12). 172.20.5.4 is inside it; 172.32.x.x is not. 192.169 is outside 192.168/16, and 11.x is public."),
    ],
    6: [
        (1601, "theory", 3, "Explain flooding. What are its problems and how are they controlled?",
         [], None, "Send on every line except the incoming one; control with hop count and sequence numbers",
         """**Flooding**: every incoming packet is sent out on every outgoing line except the one it arrived on.

Problems: an enormous number of duplicate packets; endless circulation if there are loops.

Controls:
- **Hop counter** in the header, decremented at each hop; packet discarded at 0 (initialise to the network diameter).
- **Sequence numbers**: each router remembers (source, sequence) pairs it has already flooded and drops duplicates.
- **Selective flooding**: send only on lines going roughly toward the destination.

Uses: broadcasting, distributing link-state packets, military/very robust networks; it always finds the shortest path."""),
        (1602, "numerical", 3, "Five routers are fully connected (each has 4 links). Router A floods a packet with hop count 2 and there is no duplicate suppression. How many transmissions take place?",
         [], None, "16 transmissions",
         """- **Hop 1**: A sends on all 4 links -> **4** transmissions. Hop count becomes 1.
- **Hop 2**: each of the 4 routers forwards on every line except the incoming one (3 lines) -> 4 x 3 = **12** transmissions. Hop count becomes 0, so the packets stop.

Total = 4 + 12 = **16 transmissions**."""),
    ],
    8: [
        (1801, "theory", 4, "Explain open-loop and closed-loop congestion control. Compare leaky bucket and token bucket.",
         [], None, "Prevention vs reaction; leaky bucket smooths, token bucket allows bursts",
         """**Open loop (prevention)**: retransmission policy, window policy, acknowledgement policy, discard policy, admission control.
**Closed loop (removal)**: back pressure, choke packets, implicit signalling (delay/loss), explicit signalling (ECN).

| Leaky bucket | Token bucket |
|---|---|
| Output at a **constant** rate | Output can **burst** up to bucket capacity |
| Bucket holds packets | Bucket holds tokens (permission to send) |
| Excess packets dropped when full | Excess **tokens** discarded; packets wait |
| Smooths traffic completely | Saves up tokens when idle for later bursts |"""),
        (1802, "numerical", 3, "A token bucket has capacity 250 KB, tokens arrive at 2 MB/s, and the maximum output rate is 25 MB/s. How long can the host send at full speed?",
         [], None, "About 10.9 ms",
         """Burst length S = C / (M - rho)

S = 250 KB / (25 - 2) MB/s = 250 / 23,000 s = **10.9 ms** (about 11 ms)"""),
        (1803, "numerical", 3, "TCP starts with cwnd = 1 MSS (1 KB) and ssthresh = 8 KB. Assuming no loss, give cwnd at the start of RTTs 1 to 8. If a timeout happens when cwnd = 12 KB, what are the new ssthresh and cwnd?",
         [], None, "1, 2, 4, 8, 9, 10, 11, 12 KB; then ssthresh 6 KB, cwnd 1 KB",
         """| RTT | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| cwnd (KB) | 1 | 2 | 4 | 8 | 9 | 10 | 11 | 12 |
| Phase | slow start | | | reaches ssthresh | congestion avoidance (+1 MSS/RTT) | | | |

On timeout at cwnd = 12 KB: **ssthresh = 12 / 2 = 6 KB**, **cwnd = 1 KB**, and slow start begins again."""),
        (1804, "mcq", 1, "In TCP Reno, after three duplicate ACKs the congestion window becomes:",
         ["1 MSS", "Half of the current window", "Unchanged", "Double the current window"], "B", "Half of the current window",
         "Three duplicate ACKs mean only one segment was lost, so Reno does **fast recovery**: ssthresh = cwnd/2 and cwnd = ssthresh (multiplicative decrease). A timeout drops cwnd to 1 MSS instead."),
    ],
    9: [
        (1901, "theory", 3, "Explain the principles of network applications: architectures, process communication and transport services.",
         [], None, "Client-server vs P2P; sockets; reliability, throughput, timing, security",
         """**Architectures**
- **Client-server**: an always-on server with a fixed address serves many clients (web, email).
- **Peer-to-peer**: peers act as both client and server; self-scalable (BitTorrent).

**Process communication**: processes on different hosts exchange **messages through sockets**; a process is identified by **IP address + port number**.

**Transport services an application needs**
| Need | Example |
|---|---|
| Reliable data transfer | File transfer, email, web |
| Throughput | Video streaming |
| Timing (low delay) | Internet telephony, games |
| Security | Banking (TLS) |"""),
        (1902, "mcq", 1, "Which transport service does Internet telephony need most?",
         ["Reliable data transfer", "Timing (low delay)", "Large storage", "Ordered byte stream"], "B", "Timing (low delay)",
         "Voice is **time-sensitive** and loss-tolerant: a late packet is useless, a lost one is barely noticed. That is why VoIP usually runs over UDP."),
    ],
    10: [
        (2001, "theory", 4, "Explain the steps to design and test a star topology LAN in Cisco Packet Tracer.",
         [], None, "Place devices, connect with straight-through cables, assign IPs, ping",
         """1. Place a **2960 switch** and 4 **PCs** from the device panel.
2. Connect each PC's FastEthernet port to a switch port with a **copper straight-through** cable (links turn green).
3. On each PC: Desktop -> IP Configuration -> set IP (192.168.1.1 - .4) and mask 255.255.255.0.
4. Test from Command Prompt: `ping 192.168.1.2`. Replies mean the LAN works.
5. Use **Simulation mode** to watch ARP and ICMP packets move hop by hop.
For a hub-based star, replace the switch with a hub and notice every PC receives every frame."""),
        (2002, "theory", 3, "Write the Cisco IOS commands to configure a router interface and a static route.",
         [], None, "interface + ip address + no shutdown; ip route",
         """```
Router> enable
Router# configure terminal
Router(config)# interface gigabitEthernet0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# ip route 192.168.2.0 255.255.255.0 10.0.0.2
Router(config)# end
Router# show ip route
```
`ip route <destination network> <mask> <next-hop IP>` adds the static route; `show ip route` marks it with **S**."""),
        (2003, "mcq", 1, "Which cable connects a PC to a switch in Packet Tracer?",
         ["Crossover", "Straight-through", "Console", "Serial DCE"], "B", "Straight-through",
         "Unlike devices (PC-switch, switch-router) use **straight-through**. Like devices (PC-PC, switch-switch, PC-router) use crossover. Console is for CLI access."),
        (2004, "theory", 3, "Write the commands to configure RIP and OSPF on a router.",
         [], None, "router rip + network; router ospf + network wildcard area",
         """**RIP (distance vector)**
```
Router(config)# router rip
Router(config-router)# version 2
Router(config-router)# network 192.168.1.0
Router(config-router)# network 10.0.0.0
```

**OSPF (link state)**
```
Router(config)# router ospf 1
Router(config-router)# network 192.168.1.0 0.0.0.255 area 0
Router(config-router)# network 10.0.0.0 0.0.0.3 area 0
```
OSPF uses a **wildcard mask** (inverse of subnet mask). Check with `show ip route` (R = RIP, O = OSPF)."""),
    ],
}
