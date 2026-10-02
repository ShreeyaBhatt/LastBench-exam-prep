"""Unit 1 - Introduction to Computer Networks (PB Q1-Q66)."""

TITLE = "Introduction to Networks"
SOURCE = "T1: Computer Network T1 Notes - Unit-1, Unit-1 Networking Devices"

NOTES = {
    "summary": "What a network is, how it is classified, the OSI and TCP/IP layer stacks, network devices, and the four delays that make up latency.",
    "sections": [
        {"h": "Basics", "points": [
            "**Network** = nodes (computers, printers, routers) + links (wired or wireless) that share resources.",
            "**5 components**: Message, Sender, Receiver, Transmission medium, Protocol.",
            "**Protocol** = set of rules both sides agree on. Without it devices are connected but cannot communicate.",
            "**ARPANET** (1969, DARPA) was the first network and the first to use packet switching. TCP/IP came from Cerf & Kahn (1978).",
            "Connection types: **point-to-point** (dedicated link for 2 devices) and **multipoint** (3+ devices share one link).",
            "Data flow: **Simplex** (one way: keyboard), **Half duplex** (both ways, one at a time: walkie-talkie), **Full duplex** (both at once: telephone).",
        ]},
        {"h": "Network types", "points": [
            "By size: **PAN** (Bluetooth, ~10 m) < **LAN** (building/campus) < **MAN** (city, cable TV) < **WAN** (country/world, Internet).",
            "By role: **Peer-to-peer** (no central server, cheap, low security) vs **Client-server** (central server, scalable, single point of failure).",
            "Size, ownership and physical architecture all decide the category of a network.",
        ]},
        {"h": "OSI model (7 layers, top to bottom)", "points": [
            "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing = Application, Presentation, Session, Transport, Network, Data link, Physical.",
            "**Physical**: raw bits to signals, cables, voltages, bit rate, topology, transmission mode.",
            "**Data link**: framing, MAC (physical) addressing, error control, flow control, access control. Node-to-node (hop-to-hop) delivery.",
            "**Network**: logical (IP) addressing, routing, packet forwarding, fragmentation. Source-to-destination (host-to-host) delivery.",
            "**Transport**: port addressing, segmentation and reassembly, end-to-end (process-to-process) flow and error control. TCP / UDP.",
            "**Session**: dialog control and synchronization (checkpoints).",
            "**Presentation**: translation (ASCII/EBCDIC), encryption, compression.",
            "**Application**: services for the user: HTTP, FTP, SMTP, DNS.",
        ]},
        {"h": "TCP/IP model (4 layers)", "points": [
            "Network interface (= OSI Physical + Data link), Internet (= Network), Transport, Application (= Session + Presentation + Application).",
            "TCP/IP has **no separate Session or Presentation layer**.",
            "IPv4 address = **32 bits** (4 bytes). IPv6 = **128 bits** (16 bytes). MAC = **48 bits**, burned into the NIC.",
        ]},
        {"h": "Devices and the layer they work at", "points": [
            "**Repeater** (L1): regenerates a weak signal to extend range. **Hub** (L1): multiport repeater, broadcasts to all ports.",
            "**Bridge** (L2): connects two LAN segments, filters by MAC. **Switch** (L2): multiport bridge, forwards by MAC table.",
            "**Router** (L3): connects different networks (LANs), forwards by IP and routing table.",
            "**Gateway**: protocol converter; can work at **any** of the 7 layers. **Modem**: modulates digital to analog and back.",
        ]},
    ],
    "formulas": [
        ["Propagation delay", "Tp = distance / propagation speed"],
        ["Transmission delay", "Tt = packet size (bits) / bandwidth (bps)"],
        ["Latency (total delay)", "Tp + Tt + queuing + processing"],
        ["Throughput of a path", "min(R1, R2, ..., Rn)  (bottleneck link)"],
        ["File transfer time", "file size (bits) / throughput"],
        ["Store-and-forward, h links, N packets", "(N + h - 1) x Tt + h x Tp"],
        ["Bandwidth-delay product", "bandwidth x delay = bits 'in flight' on the link"],
    ],
    "traps": [
        "Convert bytes to bits (x8) before dividing by bandwidth.",
        "km to m (x1000) before dividing by m/s. Answer comes out in seconds.",
        "1 Mbps = 10^6 bps (decimal) even when file sizes use KB/MB.",
        "Throughput is decided by the slowest link, not the sum or average.",
        "Jitter = variation in packet delay; it hurts audio/video.",
    ],
}

NUMERICAL = {27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
             45, 46, 47, 48, 49, 50, 51, 52, 53, 54}

TEXT_FIX = {
    27: "What is the propagation time if the distance between the two points is 12000 km? Assume the propagation speed to be 2.4 x 10^8 m/s in cable.",
    44: "A packet travels through three network links, each 5000 km long, with a propagation speed of 2.5 x 10^8 m/s. Each link has a transmission rate of 50 Mbps, and the packet size is 10 MB. Additionally, each network node introduces a processing delay of 20 ms and a queuing delay of 5 ms. Calculate the total end-to-end delay in seconds, considering transmission, propagation, processing, and queuing delays.",
}

SOL = {
    1: "**ARPANET** (Advanced Research Projects Agency Network) was built by DARPA in 1969. It linked 4 university computers (UCLA, Stanford, UCSB, Utah) and was the first network to use packet switching.",
    2: "When three or more devices share a single link, the connection is **multipoint** (multidrop). A dedicated link between exactly two devices is point-to-point.",
    3: "Two devices are *in a network* when a **process in one device can exchange information with a process in another device**. Merely running processes or matching PIDs does not make a network.",
    4: "A network can be categorized by its **size** (LAN/MAN/WAN), its **ownership** (private/public) and its **physical architecture** (topology). So **all of the above**.",
    5: "LAN = **Local** Area Network: a network within a room, building or campus.",
    6: "This is the postal-letter analogy for layering. At the receiver the order is reversed: the **lowest layer** is the carrier delivering the letter **to the post office**, the middle layer moves it from post office to mailbox, and the top layer opens and reads it.",
    7: "TCP/IP has only Application, Transport, Internet and Network-interface layers. The **Presentation** (and Session) layer exists only in OSI; its work is folded into the TCP/IP Application layer.",
    8: "MAN = **Metropolitan** Area Network: covers a city (e.g. cable TV network, city-wide Wi-Fi).",
    9: "File service, print service and database service are all services a network provides to users, so **all of the above**.",
    10: "The TCP/IP model has **4 layers**: Network interface (link), Internet, Transport, Application. (Some books show 5 by splitting link into Physical + Data link.)",
    11: "The **Physical layer** converts bits into electromagnetic signals (electrical, light or radio) and puts them on the medium.",
    12: "A **router** connects multiple LANs (different networks) and forwards packets between them using IP addresses. A repeater only extends one segment; a bridge joins segments of the same LAN.",
    13: "The concept of connected computers sharing resources is called **networking**.",
    14: "The Transport layer's main job is **end-to-end (process-to-process) delivery** of the whole message. Node-to-node delivery is the Data link layer.",
    15: "A **gateway** is a protocol converter that can operate at **any of the seven OSI layers**, translating between completely different network architectures. Router = L3, switch = L2, modem = L1.",
    16: "Latency = **propagation time + transmission time + queuing time + processing delay**. All four delays add up; none are subtracted.",
    17: "The time a device holds a message in its buffer before it can be processed is **queuing time**. It depends on how loaded the device is.",
    18: "A **wireless repeater** (range extender) receives the router's signal and re-broadcasts it, extending wireless coverage.",
    19: "ARPANET = **Advanced Research Projects Agency Network**.",
    20: "A set of rules that governs communication is a **protocol**. SMTP and FTP are examples of protocols.",
    21: "There are **2** IP versions in use: **IPv4** (32-bit) and **IPv6** (128-bit).",
    22: "The **Session layer** (and Presentation layer) is present in OSI but not in TCP/IP.",
    23: "An IPv4 address is **32 bits** (4 bytes), written as 4 decimal octets, e.g. 192.168.1.1.",
    24: "A **repeater** regenerates (boosts) a weak or corrupted signal so it can travel further. It works at the physical layer.",
    25: "IPv6 address = 128 bits = **16 bytes**.",
    26: "A MAC address is **48 bits** (6 bytes, e.g. 3A:12:34:B2:11:41) and is burned into the **NIC** (network interface card).",
    27: ("50 ms", """**Given:** d = 12000 km = 12 x 10^6 m, v = 2.4 x 10^8 m/s

**Tp = d / v** = 12 x 10^6 / 2.4 x 10^8 = 0.05 s = **50 ms**"""),
    28: ("0.02 ms", """**Given:** message = 2.5 KB = 2500 bytes = 20,000 bits, bandwidth = 1 Gbps = 10^9 bps

**Tt = L / B** = 20,000 / 10^9 = 2 x 10^-5 s = **0.02 ms** (20 microseconds)"""),
    29: ("14 ms", """**Given:** L = 1000 bytes = 8000 bits, d = 2500 km, v = 2.5 x 10^8 m/s, R = 2 Mbps

- Transmission: Tt = 8000 / (2 x 10^6) = **4 ms**
- Propagation: Tp = 2.5 x 10^6 / 2.5 x 10^8 = **10 ms**

Total time = Tt + Tp = 4 + 10 = **14 ms**"""),
    30: ("(a) 500 kbps (b) 64 s (c) 100 kbps, 320 s", """**(a)** Throughput = rate of the slowest (bottleneck) link = min(500 kbps, 2 Mbps, 1 Mbps) = **500 kbps**

**(b)** File = 4 million bytes = 32 x 10^6 bits. Time = 32 x 10^6 / 500 x 10^3 = **64 s**

**(c)** With R2 = 100 kbps the bottleneck becomes R2.
Throughput = **100 kbps**, time = 32 x 10^6 / 100 x 10^3 = **320 s**"""),
    31: ("(a) 700 kbps (b) 160 s (c) 100 kbps, 1120 s", """**(a)** Throughput = min(700 kbps, 5 Mbps, 1 Mbps) = **700 kbps**

**(b)** File = 14 x 10^6 bytes = 112 x 10^6 bits. Time = 112 x 10^6 / 700 x 10^3 = **160 s**

**(c)** R2 = 100 kbps is now the bottleneck: throughput = **100 kbps**, time = 112 x 10^6 / 10^5 = **1120 s** (about 18.7 min)"""),
    32: ("about 12.76 ms", """Speed of signal is not given, so take v = 2 x 10^8 m/s (as in Q39).

- Packets: N = 150,000 / 1500 = **100 packets**, hops h = 4
- Tt per packet per hop = 1500 x 8 / 100 x 10^6 = **0.12 ms**
- Tp per hop = 20 x 10^3 / 2 x 10^8 = **0.1 ms**

With store-and-forward, packets are pipelined. The first packet needs h x (Tt + Tp); every other packet arrives one Tt later:

**Delay = (N + h - 1) x Tt + h x Tp** = (100 + 3) x 0.12 + 4 x 0.1 = 12.36 + 0.4 = **12.76 ms**"""),
    33: ("1575 microseconds", """Link rate = 10^7 bps, Tp = 20 us per link, switch delay = 35 us, 2 packets of 5000 bits.

- Tt per packet = 5000 / 10^7 = **500 us**

Timeline:
1. Host sends packet 1: 0 to 500 us. Packet 2 follows: 500 to 1000 us.
2. Last bit of packet 1 reaches the switch at 500 + 20 = 520 us; switch forwards at 520 + 35 = 555 us.
3. Packet 2 reaches switch at 1000 + 20 = 1020 us; forwarding starts at 1055 us (switch is free since packet 1 finished at 1055).
4. Packet 2 transmitted on link 2: 1055 to 1555 us; last bit reaches host at 1555 + 20 = **1575 us**.

Formula view: 3 x Tt + 2 x Tp + switch delay = 1500 + 40 + 35 = **1575 us**"""),
    34: ("745 microseconds", """3000 bits sent as one packet. Tt = 3000 / 10^7 = **300 us**, Tp = 50 us per link, switch delay = 45 us.

Total = Tt (host) + Tp + switch delay + Tt (switch) + Tp
= 300 + 50 + 45 + 300 + 50 = **745 us**"""),
    35: ("24 ms", """Path A to C to D = **2 links**. Packet = 4000 bytes = 32,000 bits.

- Tt = 32,000 / 4 x 10^6 = **8 ms** per link
- Tp = 1000 x 10^3 / 2.5 x 10^8 = **4 ms** per link
- Processing and queuing at C = 0

Total = 2 x (Tt + Tp) = 2 x 12 = **24 ms**"""),
    36: ("168 ms", """Path D1 to D2 to D4 to D5 = **3 links**. Packet = 4000 bytes = 32,000 bits.

- Tt = 32,000 / 2 x 10^6 = **16 ms** per link
- Tp = 10,000 x 10^3 / 2.5 x 10^8 = **40 ms** per link

Total = 3 x (16 + 40) = **168 ms**"""),
    37: ("(a) 500 kbps (b) about 360.16 ms", """**(a)** Throughput = min(500 kbps, 1 Mbps, 2 Mbps) = **500 kbps**

**(b)** Only link R2 = 1 Mbps, Tp = 20 ms. File 40,000 B = 4 packets of 10,000 B.

- Tt per packet = 10,000 x 8 / 10^6 = 80 ms. Four packets back-to-back = **320 ms**
- Last packet's last bit then propagates: **20 ms**
- ACK of 20 bytes: Tt = 160 / 10^6 = **0.16 ms**, plus Tp = **20 ms**

Total = 320 + 20 + 0.16 + 20 = **360.16 ms**"""),
    38: ("10035 ms", """3 links, 1000 packets of 1000 bits, bandwidth 100 kbps, link 1000 km, v = 2 x 10^8 m/s.

- Tt per packet = 1000 / 10^5 = **10 ms**
- Tp per link = 10^6 / 2 x 10^8 = **5 ms**

Pipelined store-and-forward: **(N + h - 1) x Tt + h x Tp** = (1000 + 2) x 10 + 3 x 5 = 10020 + 15 = **10035 ms**"""),
    39: ("about 120.76 ms", """Message = 1,500,000 bytes ("150,0000"), packets of 1500 B, so N = **1000 packets**, h = 4 hops.

- Tt = 1500 x 8 / 100 x 10^6 = **0.12 ms**
- Tp = 20 x 10^3 / 2 x 10^8 = **0.1 ms**

Delay = (N + h - 1) x Tt + h x Tp = 1003 x 0.12 + 4 x 0.1 = 120.36 + 0.4 = **120.76 ms**"""),
    40: ("15 ms", "Tp = d / v = 3000 x 10^3 / 2 x 10^8 = 0.015 s = **15 ms**"),
    41: ("0.8 s", """File = 10 MB = 10 x 10^6 x 8 = 80 x 10^6 bits

Tt = 80 x 10^6 / 100 x 10^6 = **0.8 s** (0.839 s if 1 MB is taken as 2^20 bytes)"""),
    42: ("0.486 s", """Packet = 1 MB = 8 x 10^6 bits; 3 links (store-and-forward, so each link transmits it again).

- Tt per link = 8 x 10^6 / 50 x 10^6 = **0.16 s**
- Tp per link = 500 x 10^3 / 2.5 x 10^8 = **2 ms**

Total = 3 x (0.16 + 0.002) = **0.486 s**"""),
    43: ("about 1.623 s", """Packet = 2 MB = 16 x 10^6 bits.

- Tt = 16 x 10^6 / 10 x 10^6 = **1.6 s**
- Tp = 1000 x 10^3 / 3 x 10^8 = **3.33 ms**
- Processing = 4 nodes x 5 ms = **20 ms**

Total = 1.6 + 0.00333 + 0.02 = **1.6233 s**"""),
    44: ("about 4.91 s", """Packet = 10 MB = 80 x 10^6 bits; 3 links means 2 intermediate nodes (routers).

- Tt per link = 80 x 10^6 / 50 x 10^6 = **1.6 s**
- Tp per link = 5000 x 10^3 / 2.5 x 10^8 = **0.02 s**
- Per router: processing 20 ms + queuing 5 ms = **25 ms**

Total = 3 x (1.6 + 0.02) + 2 x 0.025 = 4.86 + 0.05 = **4.91 s**

(If you count processing and queuing at all 3 receiving nodes, it is 4.86 + 0.075 = 4.935 s. State your assumption in the exam.)"""),
    45: ("12.5 ms", "Tp = 2500 x 10^3 / 2 x 10^8 = 0.0125 s = **12.5 ms**. Bandwidth (1 Gbps) does not affect propagation delay."),
    46: ("30 ms", """Propagation delay is directly proportional to distance (speed is unchanged).

New Tp = 20 ms x (9000 / 6000) = **30 ms**

(Speed = 6000 km / 20 ms = 3 x 10^8 m/s; 9000 km / 3 x 10^8 = 30 ms.)"""),
    47: ("700.5 ms", """Packet = 500 KB = 4 x 10^6 bits.

| Link | Tt = L / R | Tp = d / v |
|---|---|---|
| 1 | 4 x 10^6 / 10 x 10^6 = 400 ms | 10^6 / 2 x 10^8 = 5 ms |
| 2 | 4 x 10^6 / 50 x 10^6 = 80 ms | 2 x 10^6 / 2.5 x 10^8 = 8 ms |
| 3 | 4 x 10^6 / 20 x 10^6 = 200 ms | 1.5 x 10^6 / 2 x 10^8 = 7.5 ms |

Total = (400 + 80 + 200) + (5 + 8 + 7.5) = 680 + 20.5 = **700.5 ms**"""),
    48: ("1.6 ms per packet, 8 s total", """1 KB = 1000 bytes = 8000 bits; 5 MB / 1 KB = **5000 packets**.

- Per packet: Tt = 8000 / 5 x 10^6 = **1.6 ms**
- Total: 5000 x 1.6 ms = **8 s** (same as 40 x 10^6 bits / 5 Mbps)"""),
    49: ("0.8005 s", """- Tt = 500 x 10^3 x 8 / 5 x 10^6 = **0.8 s**
- Tp = 100 x 10^3 / 2 x 10^8 = **0.5 ms**

Total = **0.8005 s**"""),
    50: ("about 2.816 s", """Packet = 2 MB = 16 x 10^6 bits.

| Link | Tt | Tp |
|---|---|---|
| 1 (20 Mbps, 800 km, 2 x 10^8) | 0.8 s | 4 ms |
| 2 (30 Mbps, 1000 km, 2.5 x 10^8) | 0.5333 s | 4 ms |
| 3 (15 Mbps, 600 km, 2 x 10^8) | 1.0667 s | 3 ms |
| 4 (40 Mbps, 1200 km, 2.5 x 10^8) | 0.4 s | 4.8 ms |

Total = 2.8 s + 15.8 ms = **2.8158 s**"""),
    51: ("16 packets, about 6.71 s", """8 MB / 512 KB = 8192 KB / 512 KB = **16 packets**.

- One packet = 512 x 1024 x 8 = 4,194,304 bits; Tt = 4,194,304 / 10^7 = **0.419 s**
- Total = 16 x 0.419 = **6.71 s**

(With decimal units, 64 x 10^6 bits / 10^7 = 6.4 s.)"""),
    52: ("12.5 ms", "Tp = 2500 x 10^3 / 2 x 10^8 = **12.5 ms**"),
    53: ("1.5 microseconds", "Tp = 300 / 2 x 10^8 = 1.5 x 10^-6 s = **1.5 us**"),
    54: ("32.5 ms", "Tp = 6500 x 10^3 / 2 x 10^8 = 0.0325 s = **32.5 ms**"),
    55: ("PAN, LAN, MAN, WAN", """| Type | Range | Example use |
|---|---|---|
| **PAN** (Personal) | ~10 m | Bluetooth phone to earbuds, smartwatch |
| **LAN** (Local) | room / building / campus | College lab, office Ethernet / Wi-Fi |
| **MAN** (Metropolitan) | a city | Cable TV network, city-wide Wi-Fi, bank branches in a city |
| **WAN** (Wide) | country / world | The Internet, airline reservation networks |

Other types: **CAN** (campus), **SAN** (storage area network for data centres), **WLAN** (wireless LAN)."""),
    56: ("Divide and conquer the communication task", """Layered architecture splits communication into layers, each doing one job and serving the layer above.

- **Modularity**: each layer can be designed and changed independently (e.g. switch from copper to fibre without touching HTTP).
- **Simplicity**: a complex task broken into small, understandable pieces.
- **Standardization and interoperability**: vendors build to standard interfaces so devices from different makers work together.
- **Easy troubleshooting**: problems are isolated to a layer.
- **Abstraction**: upper layers do not need to know how lower layers work.

Example: posting a letter. The writer, post office and carrier each do their own part, using the service of the layer below."""),
    57: ("7 layers: Physical to Application", """| # | Layer | Main functions | Unit of data |
|---|---|---|---|
| 7 | Application | User services: HTTP, FTP, SMTP, DNS | Message |
| 6 | Presentation | Translation, encryption, compression | Message |
| 5 | Session | Dialog control, synchronization (checkpoints) | Message |
| 4 | Transport | Process-to-process delivery, port addressing, segmentation, flow and error control | Segment |
| 3 | Network | Logical (IP) addressing, routing, fragmentation | Packet |
| 2 | Data link | Framing, MAC addressing, error and flow control, access control | Frame |
| 1 | Physical | Bits to signals, medium, bit rate, synchronization | Bits |

Mnemonic (top-down): **All People Seem To Need Data Processing**."""),
    58: ("4 layers: Network interface, Internet, Transport, Application", """1. **Network interface (Link)**: framing, MAC addressing, access to the medium. = OSI Physical + Data link.
2. **Internet**: IP addressing, routing, fragmentation. Protocols: IP, ICMP, ARP.
3. **Transport**: TCP (reliable, connection-oriented) and UDP (fast, connectionless); ports, segmentation, flow control.
4. **Application**: HTTP, FTP, SMTP, DNS, Telnet. = OSI Session + Presentation + Application.

TCP/IP is the practical model used on the Internet; OSI is the reference model."""),
    59: ("Repeater, hub, bridge, switch, router, gateway, modem", """| Device | Layer | Function |
|---|---|---|
| **Repeater** | 1 | Regenerates weak signals to extend a segment |
| **Hub** | 1 | Multiport repeater; sends every frame to all ports (one collision domain) |
| **Bridge** | 2 | Connects two LAN segments; filters frames by MAC address |
| **Switch** | 2 | Multiport bridge; forwards only to the destination port using a MAC table |
| **Router** | 3 | Connects different networks; forwards packets by IP using a routing table |
| **Gateway** | All / 7 | Protocol converter between dissimilar networks |
| **Modem** | 1 | Modulates digital data onto analog lines and demodulates back |
| **NIC** | 1-2 | Connects a host to the network; holds the 48-bit MAC address |

Draw: PCs to a switch/hub, switches to a router, router to the Internet through a modem."""),
    60: ("Switch = L2, MAC, within LAN; Router = L3, IP, between networks", """| Switch | Router |
|---|---|
| Data link layer (L2) | Network layer (L3) |
| Uses MAC address | Uses IP address |
| Connects devices within one LAN | Connects different networks (LAN to WAN) |
| Uses a MAC address table | Uses a routing table |
| Each port is a separate collision domain; one broadcast domain | Each port is a separate broadcast domain |
| Faster, cheaper | Can do NAT, firewalling, path selection |"""),
    61: ("Bits, signals, medium, rate, sync, topology, mode", """- **Physical characteristics** of interfaces and medium (cables, connectors).
- **Representation of bits**: encoding bits into electrical / optical / radio signals.
- **Data rate** (bits per second).
- **Bit synchronization** between sender and receiver clocks.
- **Line configuration**: point-to-point or multipoint.
- **Physical topology**: bus, star, ring, mesh.
- **Transmission mode**: simplex, half duplex, full duplex."""),
    62: ("Framing, physical addressing, flow, error, access control", """- **Framing**: divides the bit stream into frames.
- **Physical addressing**: adds sender/receiver MAC addresses in the header.
- **Flow control**: stops a fast sender from overwhelming a slow receiver.
- **Error control**: detects and retransmits damaged or lost frames (trailer holds CRC).
- **Access control**: decides which device uses a shared link (MAC protocols like CSMA/CD).

Sublayers: **LLC** (flow and error control) and **MAC** (access control)."""),
    63: ("Logical addressing, routing, forwarding, fragmentation", """- **Source-to-destination (host-to-host) delivery** across multiple networks.
- **Logical addressing**: IP addresses identify hosts globally.
- **Routing**: chooses the best path (routing algorithms).
- **Packet forwarding**: moves a packet to the correct output interface.
- **Fragmentation and reassembly** when a packet is larger than the next link's MTU.
- Congestion control (in some designs)."""),
    64: ("Transport: ports, segmentation, flow/error. Session: dialog, sync", """**Transport layer**
- Process-to-process delivery using **port numbers** (service-point addressing).
- **Segmentation and reassembly** with sequence numbers.
- **Connection control**: connection-oriented (TCP) or connectionless (UDP).
- End-to-end **flow control** and **error control**.

**Session layer**
- **Dialog control**: lets two systems talk in half or full duplex.
- **Synchronization**: inserts checkpoints so a long transfer can resume from the last checkpoint after a crash.
- Session establishment, maintenance, termination."""),
    65: ("Application: user services. Presentation: translation, encryption, compression", """**Application layer**
- Gives users access to the network: web (HTTP), email (SMTP), file transfer (FTP), remote login (Telnet), DNS.
- Network virtual terminal, file access and management, directory services.

**Presentation layer**
- **Translation** between data formats (ASCII to EBCDIC).
- **Encryption / decryption** for privacy (SSL/TLS).
- **Compression** to reduce bits (JPEG, MPEG)."""),
    66: ("Interconnected devices sharing resources; 5 components", """A **computer network** is a group of devices (nodes) connected by links (wired or wireless) to share data and resources.

**Components**
1. **Message**: the data to be sent (text, image, audio).
2. **Sender**: the device that sends the message.
3. **Receiver**: the device that receives it.
4. **Transmission medium**: the physical path (cable, fibre, radio waves).
5. **Protocol**: the set of rules governing communication.

Hardware view: NICs, cables, switches, routers, servers and clients."""),
}
