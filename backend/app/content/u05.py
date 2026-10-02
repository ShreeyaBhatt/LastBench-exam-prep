"""Unit 5 - Introduction to the Network Layer (PB Q214-Q261)."""

TITLE = "Network Layer & IPv4"
SOURCE = "Practice book Unit 5 (not covered in T1 notes; standard Forouzan / Kurose content)"

NOTES = {
    "summary": "IPv4 addressing (classful and CIDR), subnetting, the IPv4 header, fragmentation, and circuit vs packet switching.",
    "sections": [
        {"h": "Network layer basics", "points": [
            "Unit of data = **packet / datagram**. Job: host-to-host delivery, logical addressing, routing, forwarding, fragmentation. **Error control is not** its function.",
            "IP is **connectionless and unreliable** (best effort). Each datagram is routed independently, so packets may take different routes.",
            "**Circuit switching** (telephone): reserved path, constant rate. **Packet switching**: datagram (connectionless) or **virtual circuit** (connection-oriented; packets carry a short **VC number**).",
            "A host can have several IP addresses (one per interface).",
        ]},
        {"h": "IPv4 addressing", "points": [
            "32 bits = **network ID + host ID**. Dotted decimal: each octet 0-255.",
            "Classes by first octet: **A 0-127** (/8), **B 128-191** (/16), **C 192-223** (/24), D 224-239 (multicast), **E 240-255** (reserved). By first bits: A 0, B 10, C 110, D 1110, E 1111.",
            "Network address = IP **AND** mask. Broadcast = network address with all host bits = 1. Usable hosts = **2^h - 2**.",
            "**CIDR** /n = n network bits. Block size in the interesting octet = 256 - mask octet.",
            "Subnetting: borrow s bits -> **2^s subnets**. 12 subnets -> 4 bits (16) -> Class C mask 255.255.255.240.",
            "**VLSM**: allocate the **largest** subnet first, each block a power of 2 aligned on its size.",
        ]},
        {"h": "IPv4 header (20-60 bytes)", "points": [
            "VER (4) | **HLEN** (4, x4 bytes, min 5 = 20 B) | Service type | **Total length** (16) | **Identification** | **Flags** (D, M) | **Fragment offset** (13, x8 bytes) | **TTL** | Protocol | Checksum | Source IP | Destination IP | Options.",
            "**TTL** decrements at each router; packet discarded at 0, which **prevents looping**.",
            "Routers change TTL, checksum, and (when fragmenting) length/flags/offset. They **never change source address**.",
            "Options length = HLEN x 4 - 20.",
        ]},
        {"h": "Fragmentation", "points": [
            "Needed when datagram > next link's **MTU**. Fields: **Identification** (same for all fragments), **MF** flag (1 = more follow, 0 = last), **DF** (don't fragment), **Offset** (in units of 8 bytes).",
            "Data per fragment = largest **multiple of 8** <= MTU - header.",
            "Offset of a fragment = bytes of data before it / 8. First data byte = offset x 8; last byte = first + payload - 1.",
            "Reassembly happens **only at the destination**.",
        ]},
    ],
    "formulas": [
        ["Network ID", "IP AND subnet mask"],
        ["Usable hosts", "2^(32 - n) - 2"],
        ["Subnets from s borrowed bits", "2^s"],
        ["Bits to borrow for N subnets", "smallest s with 2^s >= N"],
        ["Data per fragment", "floor((MTU - IP header) / 8) x 8"],
        ["Fragment offset", "(data bytes before this fragment) / 8"],
        ["Number of fragments", "ceil(total data / data per fragment)"],
        ["Header length", "HLEN x 4 bytes"],
    ],
    "traps": [
        "HLEN is in 4-byte words; fragment offset is in 8-byte units.",
        "Total length includes the header.",
        "When a fragment is fragmented again, MF of every piece stays 1 unless it is the true last piece.",
        "Fragment the transport payload (TCP/UDP header + data), not just the user data.",
        "A first octet of 125 is Class A, even if the question calls it Class B.",
    ],
}

NUMERICAL = set(range(230, 262)) - {231}

TEXT_FIX = {
    236: "The forwarding table of a router is shown below. A packet addressed to a destination address 200.150.68.118 arrives at the router. It will be forwarded to the interface with ID ____. (The table is not printed in the practice book.)",
}

SOL = {
    214: "The network layer handles **packets** (datagrams). Bits = physical, frames = data link.",
    215: "Routing, inter-networking and congestion control are network-layer jobs. Hop-by-hop **error control** is a data link (and transport) function.",
    216: "A 32-bit IP address has a **network address part and a host address part**.",
    217: "IP is **unreliable** (best-effort, connectionless): no ACKs, no retransmission, no ordering.",
    218: "The traditional telephone network is **circuit switched**: a dedicated path is reserved for the whole call.",
    219: "Statement D is false: with the **source routing option** the sender *can* set the route. A, B, C are true (multiple IPs per host, different routes, TTL discards packets).",
    220: "Networks providing only connection service = **virtual-circuit (connection-oriented)** networks; only connectionless = **datagram (connectionless)** networks.",
    221: "TTL is decremented at each router and the packet is discarded at 0, so a packet caught in a routing loop does not circulate forever: it **prevents packet looping**.",
    222: "Routers change TTL (decrement), checksum (recomputed) and length (when fragmenting). The **source address** is not modified.",
    223: "01000010: VER = 0100 = 4 (valid), HLEN = 0010 = 2, header = 2 x 4 = **8 bytes**. The minimum header is 20 bytes (HLEN 5), so **the receiver rejects the packet**.",
    224: "HLEN = 1000 = 8, header = 8 x 4 = 32 bytes. Options = 32 - 20 = **12 bytes**.",
    225: """- M = 0 and offset is not 0 -> **last fragment**
- Header = 10 x 4 = 40 bytes, payload = 400 - 40 = 360 bytes
- First byte = offset x 8 = 300 x 8 = **2400**
- Last byte = 2400 + 360 - 1 = **2759**

Answer: **Last fragment, 2400 and 2759**""",
    226: "Identification, Flags and Fragment offset all serve fragmentation. **Type of service** is about priority / QoS.",
    227: """- C1: 203.197.2.53 AND 255.255.128.0 = 203.197.0.0. C2's IP with C1's mask: 203.197.75.201 AND 255.255.128.0 = 203.197.0.0. Same, so **C1 thinks C2 is on its network**.
- C2: 203.197.75.201 AND 255.255.192.0 = 203.197.64.0. C1's IP with C2's mask: 203.197.2.53 AND 255.255.192.0 = 203.197.0.0. Different, so **C2 thinks C1 is on a different network**.

Answer **A**.""",
    228: "If each sees the other as off-network it must send through the default gateway, and to put the frame on the LAN it must **find the MAC address that corresponds to the gateway's IP address** (ARP).",
    229: "In a virtual-circuit network the path is set up first, so each packet carries only a **short VC number** instead of full addresses.",
    230: "223 = 11011111, 1 = 00000001, 3 = 00000011, 27 = 00011011, so **11011111.00000001.00000011.00011011** (option A).",
    231: "Class B default mask is 255.255.0.0, so the broadcast of network 172.16.0.0 sets the last 16 bits to 1: **172.16.255.255**.",
    232: """- First octet 172 is in 128-191: **Class B**
- Mask .128 -> block size 128 in the last octet. 7 lies in block 0-127.
- Subnet = **172.16.13.0**, broadcast = **172.16.13.127**""",
    233: "12 subnets need s bits with 2^s >= 12, so **s = 4** (16 subnets). Class C mask /24 + 4 = /28 = **255.255.255.240**.",
    234: "10 subnets: 2^3 = 8 is too few, 2^4 = 16 is enough, so borrow 4 bits: **255.255.255.240**.",
    235: """Mask 255.255.240.0: third-octet block size = 256 - 240 = 16. 30 lies in block 16-31.

Network = 160.168.16.0, broadcast = **160.168.31.255**""",
    236: ("Interface 3 (per key)", """The forwarding table for this question is **missing from the practice book**, so it cannot be re-derived here. The key gives **interface 3**.

How to solve it when the table is given: **longest prefix match**.
1. Write the destination 200.150.68.118 in binary (at least the octets the prefixes cover: 68 = 01000100).
2. For each entry, check whether the first n bits of the destination equal the prefix.
3. Of all matching entries, choose the one with the **longest** prefix (largest /n). If none match, use the default route."""),
    237: ("2740 datagrams", """Each datagram carries 1500 - 20 (IP) - 20 (TCP) = **1460 bytes** of data.

Datagrams = ceil(4,000,000 / 1460) = ceil(2739.7) = **2740**"""),
    238: ("3 packets: 516, 516, 48 bytes", """The IP payload is the whole TCP segment = 1000 data + 20 TCP header = **1020 bytes**.

Each IP packet can carry 500 bytes, but fragment data must be a multiple of 8, so **496 bytes** per fragment.

| Fragment | Data | Total size (with 20 B IP header) |
|---|---|---|
| 1 | 496 | **516** |
| 2 | 496 | **516** |
| 3 | 28 | **48** |

(If you ignore the 8-byte rule and treat the 20-byte TCP header separately, the simple answer is 2 packets of 520 bytes; mention the assumption.)"""),
    239: ("13 fragments", """Data = 1000 - 20 = 980 bytes. Per fragment: MTU 100 - 20 = 80 bytes (multiple of 8).

Fragments = ceil(980 / 80) = ceil(12.25) = **13** (12 of 80 B and the last of 20 B)."""),
    240: ("4 fragments", """Data = 2400 - 20 = 2380 bytes. Per fragment = 700 - 20 = **680 bytes** (680 / 8 = 85).

| # | Total length | Data | ID | MF | Offset |
|---|---|---|---|---|---|
| 1 | 700 | 680 | 422 | 1 | 0 |
| 2 | 700 | 680 | 422 | 1 | 85 |
| 3 | 700 | 680 | 422 | 1 | 170 |
| 4 | 360 | 340 | 422 | 0 | 255 |"""),
    241: ("3 fragments; last: MF=0, offset 44, HLEN 5", """Data = 520 - 20 = 500. Per fragment = floor(180 / 8) x 8 = **176 bytes**.

| # | Total length | Data | MF | Offset | HLEN |
|---|---|---|---|---|---|
| 1 | 196 | 176 | 1 | 0 | 5 |
| 2 | 196 | 176 | 1 | 22 | 5 |
| 3 | 168 | 148 | 0 | 44 | 5 |

Last fragment: **MF = 0, offset = 44, HLEN = 5** (20 bytes)."""),
    242: ("144", """IP payload = 4500 - 20 = 4480 bytes (TCP header is part of it). Per fragment = 600 - 20 = **576 bytes** (576 / 8 = 72).

Offsets: fragment 1 = 0, fragment 2 = 72, fragment 3 = **144**."""),
    243: ("4 fragments", """Data = 3200 - 20 = 3180. Per fragment = 900 - 20 = **880 bytes** (880 / 8 = 110).

| # | Total length | Data | ID | MF | Offset |
|---|---|---|---|---|---|
| 1 | 900 | 880 | 512 | 1 | 0 |
| 2 | 900 | 880 | 512 | 1 | 110 |
| 3 | 900 | 880 | 512 | 1 | 220 |
| 4 | 560 | 540 | 512 | 0 | 330 |"""),
    244: ("Total length 356, DF 0, MF 0, offset 83", """IP datagram at A = 1000 (TCP segment) + 20 = **1020 bytes**.

- Link A-R1: MTU = 1500 - 15 = 1485 >= 1020, so no fragmentation.
- Link R1-R2: MTU = 700 - 10 = 690. Data per fragment = floor(670 / 8) x 8 = **664**.
  - Fragment 1: 664 data -> total 684, MF = 1, offset 0
  - Fragment 2: 1000 - 664 = 336 data -> **total 356, MF = 0, offset 664 / 8 = 83**

Last packet over R1-R2: **Total length = 356, DF = 0, MF = 0, offset = 83**"""),
    245: ("7 fragments, last offset 1110", """IP payload = 8880 + 8 (UDP header) = **8888 bytes**. Per fragment = 1500 - 20 = 1480 (multiple of 8).

Fragments = ceil(8888 / 1480) = **7** (six of 1480 B, last of 8 B).

Last fragment offset = 6 x 1480 / 8 = **1110**."""),
    246: ("(a) 20 users (b) 0.1", """**(a)** Circuit switching reserves 150 kbps per user: 3 Mbps / 150 kbps = **20 users**.

**(b)** Each user transmits 10% of the time, so P(a given user is transmitting) = **0.1**."""),
    247: ("76.8 Mbps", """One token every 5 us = 200,000 tokens/s; each token = 48 bytes = 384 bits.

Rate = 384 / 5 x 10^-6 = **76.8 Mbps**"""),
    248: ("223.1.17.0/25, 223.1.17.128/26, 223.1.17.192/28", """Allocate the largest first (block sizes powers of 2, including network and broadcast):

| Subnet | Needs | Block | Address |
|---|---|---|---|
| Subnet 2 | 90 | 128 (/25) | **223.1.17.0/25** |
| Subnet 1 | 60 | 64 (/26) | **223.1.17.128/26** |
| Subnet 3 | 12 | 16 (/28) | **223.1.17.192/28** |"""),
    249: ("A /20, B /21, C /20, D /19", """Round each request to a power of 2 and align the block on its size:

| Org | Need | Block | First | Last | Mask |
|---|---|---|---|---|---|
| A | 4000 | 4096 | 198.16.0.0 | 198.16.15.255 | /20 |
| B | 2000 | 2048 | 198.16.16.0 | 198.16.23.255 | /21 |
| C | 4000 | 4096 | 198.16.32.0 | 198.16.47.255 | /20 |
| D | 8000 | 8192 | 198.16.64.0 | 198.16.95.255 | /19 |

C cannot start at 198.16.24.0 because a 4096 block must start on a multiple of 16 in the third octet; D needs a multiple of 32."""),
    250: ("About 10^13 years", """Total addresses = 2^128 = 3.4 x 10^38.

Rate = 10^6 per 10^-12 s = 10^18 addresses/s.

Time = 3.4 x 10^38 / 10^18 = 3.4 x 10^20 s = 3.4 x 10^20 / 3.15 x 10^7 = **about 1.08 x 10^13 years**"""),
    251: ("a: A, b: C, c: A, d: E", """- **a.** First bit 0 -> **Class A**
- **b.** First bits 110 -> **Class C**
- **c.** 14 is in 0-127 -> **Class A**
- **d.** 252 is in 240-255 -> **Class E**"""),
    252: ("See table", """Mask 255.255.255.128 (/25) splits 193.1.2.0/24 into 2 subnets of 128.

**a)** Subnet-1 ID = **193.1.2.0**
**b)** Direct broadcast of Subnet-1 = **193.1.2.127**
**c)** Each subnet has 2^7 - 2 = **126 usable hosts** (network and broadcast addresses are reserved); Subnet-2 = 193.1.2.128-255, also 126.
**d)** Split Subnet-2 (193.1.2.128/25) with one more bit: mask **255.255.255.192 (/26)**

| New subnet | Subnet ID | Broadcast | Hosts |
|---|---|---|---|
| 2a | 193.1.2.128 | 193.1.2.191 | 62 |
| 2b | 193.1.2.192 | 193.1.2.255 | 62 |"""),
    253: ("24,576 addresses left", """| Group | Customers x size | Prefix | Range |
|---|---|---|---|
| 1 | 64 x 256 = 16,384 | /24 | 190.100.0.0 - 190.100.63.255 |
| 2 | 128 x 128 = 16,384 | /25 | 190.100.64.0 - 190.100.127.255 |
| 3 | 128 x 64 = 8,192 | /26 | 190.100.128.0 - 190.100.159.255 |

Group 1 customer i gets 190.100.(i-1).0/24. Group 2 customers get 190.100.64.0/25, 190.100.64.128/25, ... Group 3 get 190.100.128.0/26, 190.100.128.64/26, ...

Used = 40,960. Available = 65,536 - 40,960 = **24,576** (190.100.160.0 to 190.100.255.255)."""),
    254: ("Yes, /22 gives 1022 hosts", """/22 leaves 10 host bits: 2^10 - 2 = **1022 usable hosts** >= 100, so it is **sufficient** (in fact oversized).

The smallest subnet for 100 hosts: 2^7 - 2 = 126 >= 100, so **/25 (255.255.255.128)** fits with less waste."""),
    255: ("C /20, B /21, A /24", """11.12.13.14/8 belongs to network **11.0.0.0/8**. Allocate largest first (VLSM):

| Subnet | Hosts | Block | Network | Broadcast | Mask | Wasted |
|---|---|---|---|---|---|---|
| C | 3998 | 4096 | 11.0.0.0 | 11.0.15.255 | /20 | 4094 - 3998 = **96** |
| B | 1589 | 2048 | 11.0.16.0 | 11.0.23.255 | /21 | 2046 - 1589 = **457** |
| A | 189 | 256 | 11.0.24.0 | 11.0.24.255 | /24 | 254 - 189 = **65** |"""),
    256: ("255.240.0.0 (/12)", "16 subnets need 4 bits (2^4 = 16). /8 + 4 = **/12** = **255.240.0.0**."),
    257: ("190.76.255.193 to 190.76.255.254", """/16 + 10 bits = **/26** (64 addresses per subnet). The last subnet is 190.76.255.192/26 (broadcast 190.76.255.255).

First host = **190.76.255.193**, last host = **190.76.255.254**"""),
    258: ("28", """201 -> Class C (/24).
- Directed broadcast = 201.24.58.255. 1s: 201 (11001001) = 4, 24 (00011000) = 2, 58 (00111010) = 4, 255 = 8 -> **a = 18**
- Network ID = 201.24.58.0 -> 4 + 2 + 4 + 0 = **b = 10**

a + b = **28**"""),
    259: ("20066", """/20: third-octet block = 16. 67 is in 64-79.

Network 143.128.64.0, broadcast 143.128.79.255, last host = 143.128.79.254.

x = 79, y = 254, x x y = **20066**"""),
    260: ("125.134.96.0", """Mask 255.255.224.0: third-octet block = 256 - 224 = 32. 112 lies in 96-127.

Network (first) address = **125.134.96.0** (note: 125 is really Class A; the mask is what matters)."""),
    261: ("4 fragments at the destination", """**Ethernet (MTU 1500)**: data = 1780; per fragment 1480.

| | Total length | MF | Offset |
|---|---|---|---|
| E1 | 1500 | 1 | 0 |
| E2 | 320 | 0 | 185 |

**WAN (MTU 576)**: per fragment = floor(556/8) x 8 = 552. E1 (1480 data) splits again; E2 (320) fits.

| Fragment | Total length | MF | Offset |
|---|---|---|---|
| 1 | 572 | 1 | 0 |
| 2 | 572 | 1 | 69 |
| 3 | 396 | 1 | 138 |
| 4 | 320 | 0 | 185 |

Fragment 3 keeps MF = 1 because more data (E2) follows it."""),
}
