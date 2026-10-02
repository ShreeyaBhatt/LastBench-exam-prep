"""Unit 8 - Transport Layer Protocols: TCP and UDP (PB Q323-Q378)."""

TITLE = "TCP & UDP"
SOURCE = "Practice book Unit 8 (not covered in T1 notes; standard Forouzan / Kurose content)"

NOTES = {
    "summary": "UDP header and uses, TCP segment structure, the 3-way handshake, reliability, flow control (rwnd) and congestion control (cwnd, slow start).",
    "sections": [
        {"h": "UDP", "points": [
            "Connectionless, unreliable, **fixed 8-byte header**: Source port (2) | Destination port (2) | **Total length** (2, header + data) | Checksum (2).",
            "Adds only **demultiplexing (ports) and error checking (checksum)** to IP. Datagrams are **not numbered**.",
            "Used for DNS, real-time multimedia, VoIP, games, SNMP, DHCP, TFTP: anything that prefers speed to reliability.",
            "Hex dump: read 4 hex digits per field. Data length = total length - 8.",
        ]},
        {"h": "TCP segment", "points": [
            "Header **20-60 bytes**: Src port | Dst port | **Sequence no.** (32) | **Ack no.** (32) | HLEN | flags **URG ACK PSH RST SYN FIN** | **Window** (16) | Checksum | Urgent pointer | Options.",
            "Sequence number = number of the **first data byte** in the segment.",
            "**SYN and FIN consume one sequence number** each; a pure ACK consumes **none**.",
            "Window field 16 bits -> max 65,535 bytes; **window scale option** shifts it up to 2^14.",
        ]},
        {"h": "Connection management", "points": [
            "**3-way handshake**: SYN (seq=x) -> SYN+ACK (seq=y, ack=x+1) -> ACK (ack=y+1). Server does **passive open**, client **active open**.",
            "Termination: FIN -> ACK -> FIN -> ACK (4 segments; 3 if FIN+ACK combined). Total overhead about 7 packets per connection.",
        ]},
        {"h": "Reliability, flow and congestion control", "points": [
            "Reliability from **sequence numbers + ACKs + checksum + retransmission timer + duplicate ACKs (fast retransmit)**.",
            "**Flow control** protects the **receiver**: rwnd = buffer size - unprocessed data.",
            "**Congestion control** protects the **network**: cwnd.",
            "Sender window = **min(rwnd, cwnd)**.",
            "**Slow start**: cwnd starts at 1 MSS and **doubles every RTT** (+1 MSS per ACK) until ssthresh. Then **congestion avoidance**: +1 MSS per RTT.",
            "On **timeout**: ssthresh = cwnd / 2, cwnd = 1 MSS, slow start again.",
        ]},
    ],
    "formulas": [
        ["UDP data length", "total length - 8"],
        ["Receiver window", "rwnd = buffer - unprocessed bytes"],
        ["Sender window", "min(rwnd, cwnd)"],
        ["Usable window", "window - (LastByteSent - LastByteAcked)"],
        ["Need window scaling when", "bandwidth x RTT > 65,535 bytes"],
        ["Sequence wrap-around time", "2^32 bytes / bandwidth (bytes/s)"],
    ],
    "traps": [
        "Slow start doubles per RTT, not per ACK (per ACK it adds 1 MSS).",
        "UDP total length includes the 8-byte header.",
        "DNS uses UDP (and TCP for zone transfers); email (SMTP) uses TCP.",
        "TCP sequence numbers count bytes, not segments.",
    ],
}

NUMERICAL = {323, 324, 325, 342, 349, 353, 354, 355, 356, 359, 365, 366, 367, 368, 369, 371, 372, 373, 374}

TEXT_FIX = {
    378: "Explain how host A gets the IP address of host B (a server name) when it wants to connect with it.",
}

SOL = {
    323: """Timeout at cwnd = 32 KB -> **ssthresh = 16 KB**, cwnd restarts at 1 MSS = 2 KB.

- Slow start (doubles each RTT): 2 -> 4 -> 8 -> 16 KB: **3 RTTs**
- Congestion avoidance (+2 KB each RTT): 16 -> 18 -> ... -> 32 KB: **8 RTTs**

Total = 11 RTT x 100 ms = **1100 ms**, in the range **1100 to 1300** (option A).""",
    324: """Sender window = min(cwnd, rwnd) = min(4 KB, 6 KB) = **4 KB = 4096 bytes** (option B).

Bytes in flight = 10240 - 8192 = 2048, so the sender may still send 4096 - 2048 = 2048 more bytes.""",
    325: """Without scaling, max window = 65,535 bytes. Scaling is needed when bandwidth x RTT exceeds it:

RTT = 65,535 x 8 / 1,048,560 = 0.5 s -> **a = 500 ms**

The window scale option allows a shift of up to 14 bits: **b = 65,535 x 2^14** (option C).""",
    326: "**UDP is a datagram (connectionless) service, whereas TCP is connection-oriented.**",
    327: "Host-to-host **end-to-end** connectivity (between processes on the two hosts) is provided by the **transport layer**.",
    328: "In this question bank, the **transport layer** provides security-based (SSL/TLS) connections.",
    329: "The transport layer divides the message into **segments**.",
    330: "Statement C is wrong: format translation and code conversion are done by the **presentation** layer, not the transport layer.",
    331: "A pure ACK carrying no data consumes **no** sequence number.",
    332: "TCP and UDP are **transport protocols**.",
    333: "A SYN segment carries no data but consumes **one** sequence number.",
    334: "The client asking its TCP to connect to a server performs an **active open**. The server waiting for connections does a passive open.",
    335: "TCP needs sending and receiving buffers for **storage** of data (unsent/unacked data and out-of-order received data).",
    336: "The UDP header is fixed at **8 bytes**.",
    337: "Source port identifies **the process running on the sending computer**.",
    338: "TCP establishes a **virtual path** (a logical connection) between the two ends.",
    339: "UDP user datagrams are **not numbered**: no sequence numbers.",
    340: "Beyond IP, UDP adds **demultiplexing (ports) and error checking (checksum)**.",
    341: "UDP total length = **header plus data**.",
    342: "The sequence number of a segment is the number of its first byte: **10001**.",
    343: "TCP connection establishment uses **three-way handshaking** (SYN, SYN+ACK, ACK).",
    344: "Sequence numbers show which bytes are missing and ACK numbers tell the sender what arrived: **both** let TCP detect and recover from lost segments.",
    345: "Beyond IP, UDP adds **demultiplexing and error checking** (same as Q340).",
    346: "The **client** uses a temporary (ephemeral) port; servers use well-known ports.",
    347: "UDP is a **transport-layer, connectionless** protocol.",
    348: "(1) is the session layer's job, not application: false. (2) data link reliable transfer across the link: true. (3) transport end-to-end error recovery and flow control: true. So **2 and 3 only**.",
    349: """Sequence numbers are 32 bits, so they wrap after 2^32 bytes.

Time = 2^32 x 8 / 10^9 = 34.36 s -> **34-35 s** (option B)""",
    350: "Real-time multimedia uses **UDP** (speed, loss-tolerant); file transfer uses **TCP** (reliable).",
    351: "DNS queries use **UDP**; email (SMTP) uses **TCP**.",
    352: "In slow start cwnd grows by 1 MSS **per ACK**, which makes it **approximately double every RTT**. Only (iv) is true.",
    353: "rwnd = buffer - unprocessed data = 7000 - 1000 = **6000 bytes**.",
    354: "Window = min(rwnd, cwnd) = min(3000, 5500) = **3000 bytes**.",
    355: """CB84 | 002C | 001C | 0AEC

Destination port = 0x002C = 2 x 16 + 12 = **44**""",
    356: """DB84 | 002C | 001E | 0A1C

Total length = 0x001E = **30**. Data length = 30 - 8 = **22 bytes**""",
    357: ("Setup vs no setup; reliable vs best effort", """| Connection-oriented | Connectionless |
|---|---|
| Connection set up before data, released after | No setup; each packet sent independently |
| Packets follow the same path, arrive in order | Packets may take different paths, arrive out of order |
| Reliable: ACKs, retransmission, flow control | Best effort, no guarantee |
| More overhead, higher delay | Low overhead, fast |
| Example: TCP, telephone call, virtual circuit | Example: UDP, IP, postal letters, datagram networks |
| Good for file transfer, email, web | Good for DNS, streaming, VoIP, games |"""),
    358: ("Bandwidth, throughput, latency, jitter, packet loss", """- **Bandwidth**: maximum data rate of the link (bps).
- **Throughput**: actual data delivered per second (limited by the bottleneck).
- **Latency (delay)**: propagation + transmission + queuing + processing.
- **Jitter**: variation in packet delay (critical for audio/video).
- **Packet loss**: fraction of packets dropped (congestion, errors).
- **Bandwidth-delay product**: bits in flight; decides required window size.
- Utilization / efficiency of the link."""),
    359: ("1100 ms (range 1100-1300)", """Same as Q323.

- Timeout: ssthresh = 32 / 2 = **16 KB**, cwnd = 2 KB.
- Slow start: 2 -> 4 -> 8 -> 16 KB = **3 RTTs**
- Congestion avoidance: 16 -> 18 -> 20 -> ... -> 32 KB = **8 RTTs**

Total = 11 x 100 ms = **1100 ms**"""),
    360: ("Sequence numbers, ACKs, checksum, timers, retransmission, flow/congestion control", """- **Sequence numbers** on every byte: detect loss, duplicates, reordering.
- **Cumulative acknowledgements**: receiver tells sender what arrived.
- **Checksum** in every segment detects corruption; bad segments are discarded.
- **Retransmission timer** (RTO): unacknowledged segments are resent.
- **Fast retransmit** on 3 duplicate ACKs.
- **Flow control** (rwnd) prevents receiver buffer overflow.
- **Congestion control** (cwnd) prevents network overload.
- **Connection management** (3-way handshake) synchronizes sequence numbers."""),
    361: ("Checksum + ACK + timeout/retransmission", """TCP error control detects and fixes **corrupted, lost, out-of-order and duplicate** segments.

1. **Checksum**: mandatory in every segment; a corrupted segment is discarded (treated as lost).
2. **Acknowledgement**: cumulative ACK = next byte expected. ACK segments consume no sequence number and are not themselves ACKed.
3. **Retransmission**:
   - **On time-out** (RTO expires for the oldest unacked segment).
   - **On three duplicate ACKs** (fast retransmit), without waiting for the timer.
4. **Out-of-order** segments are stored (not discarded) until the missing one arrives.
5. **Duplicates** are recognized by sequence number and dropped."""),
    362: ("Process-to-process delivery, reliability, flow, congestion, multiplexing", """End-to-end services provided by the transport layer:
1. Process-to-process (end-to-end) delivery using port numbers
2. Multiplexing and demultiplexing
3. Connection-oriented / connectionless service
4. Reliable delivery: error control and retransmission
5. Flow control
6. Congestion control
7. Segmentation, sequencing and reassembly"""),
    363: ("Faster, lighter, no connection, supports broadcast", """- **No connection setup**: no handshake delay (good for one-shot queries like DNS).
- **Small 8-byte header** vs 20+ for TCP: less overhead.
- **No connection state** at the server: can serve many more clients.
- **No congestion control throttling**: the application controls the sending rate (good for live audio/video).
- **Supports broadcast and multicast**.
- **Message boundaries preserved** (datagrams), unlike TCP's byte stream.
- Lower latency for real-time apps where a late packet is useless anyway."""),
    364: ("DNS (also SNMP, SIP)", """**DNS** uses both:
- **UDP port 53** for normal queries and responses (small, fast).
- **TCP port 53** for **zone transfers** between servers and for responses larger than 512 bytes.

Other examples: SIP, SNMP-related services, and many apps registered on both protocols for the same port number."""),
    365: ("5000 bytes", "rwnd = 6000 - 1000 = **5000 bytes**"),
    366: ("4000 bytes", "rwnd = 5000 - 1000 = **4000 bytes**"),
    367: ("3000 bytes", "Window = min(rwnd, cwnd) = min(3000, 4500) = **3000 bytes**"),
    368: ("4000 bytes", "Window = min(4000, 4500) = **4000 bytes**"),
    369: ("3000 bytes", "Window = min(3000, 3500) = **3000 bytes**"),
    370: ("Flow = protect the receiver; congestion = protect the network", """| Flow control | Congestion control |
|---|---|
| Prevents the **sender** from overwhelming the **receiver** | Prevents senders from overloading the **network** (routers) |
| End-to-end, between two hosts | Global, involves the whole network path |
| Uses **rwnd** advertised by receiver | Uses **cwnd** maintained by sender |
| Receiver tells sender its free buffer | Sender infers congestion from loss / timeouts / duplicate ACKs |
| Sliding window, stop-and-wait | Slow start, congestion avoidance, fast recovery, AIMD |"""),
    371: ("43652, 13, 26, 18", """AA84 | 000D | 001A | 001A

- i. Source port = 0xAA84 = 10 x 4096 + 10 x 256 + 8 x 16 + 4 = **43652**
- ii. Destination port = 0x000D = **13**
- iii. Total length = 0x001A = **26 bytes**
- iv. Data length = 26 - 8 = **18 bytes**"""),
    372: ("43947, 13, 28, 20", """ABAB | 000D | 001C | 001C

- i. Source port = 0xABAB = 43776 + 171 = **43947**
- ii. Destination port = 0x000D = **13**
- iii. Total length = 0x001C = **28 bytes**
- iv. Data = 28 - 8 = **20 bytes**"""),
    373: ("52445, 13, 28, 20", """CCDD | 000D | 001C | 001C

- i. Source port = 0xCCDD = 52224 + 221 = **52445**
- ii. Destination port = **13**
- iii. Total length = **28 bytes**
- iv. Data = **20 bytes**"""),
    374: ("52100, 13, 28, 20", """CB84 | 000D | 001C | 001C

- i. Source port = 0xCB84 = 51968 + 132 = **52100**
- ii. Destination port = **13** (daytime service)
- iii. Total length = **28 bytes**
- iv. Data = 28 - 8 = **20 bytes**"""),
    375: ("Header 20-60 B: ports, seq, ack, HLEN, flags, window, checksum, urgent pointer, options", """| Field | Bits | Why it matters |
|---|---|---|
| Source port | 16 | Identifies sending process |
| Destination port | 16 | Identifies receiving process (demultiplexing) |
| Sequence number | 32 | Number of first data byte; ordering and loss detection |
| Acknowledgement number | 32 | Next byte expected; reliability |
| HLEN | 4 | Header length in 4-byte words (5-15 -> 20-60 B) |
| Reserved | 6 | Future use |
| Flags | 6 | **URG** urgent data, **ACK** ack valid, **PSH** push now, **RST** reset, **SYN** sync seq numbers (open), **FIN** finish (close) |
| Window size | 16 | Receiver window (rwnd) for flow control |
| Checksum | 16 | Error detection over header, data and pseudo-header |
| Urgent pointer | 16 | End of urgent data when URG = 1 |
| Options | 0-40 B | MSS, window scale, SACK, timestamps |

Together these fields give TCP reliable, ordered, flow-controlled, full-duplex byte-stream delivery."""),
    376: ("Checksum, ACK, sequence numbers, timers, retransmission, windows", """| Mechanism | Purpose |
|---|---|
| **Checksum** | Detect bit errors |
| **Sequence numbers** | Detect loss and duplicates, reorder data |
| **Acknowledgements** (ACK/NAK) | Tell sender what arrived |
| **Timer / timeout** | Recover from lost packets or lost ACKs |
| **Retransmission** (ARQ: Stop-and-Wait, Go-Back-N, Selective Repeat) | Resend lost/corrupt data |
| **Sliding window / pipelining** | Higher utilization while staying reliable |
| **Flow control** | Avoid receiver overflow |"""),
    377: ("3 for setup + 4 for teardown = 7 overhead packets", """**Overhead packets**: connection setup takes **3** (SYN, SYN+ACK, ACK) and termination takes **4** (FIN, ACK, FIN, ACK), so about **7 packets** of overhead (6 if FIN and ACK are combined).

**Three-way handshake**
```
Client                          Server (passive open)
  | --- SYN, seq = x ------------> |   active open
  | <-- SYN+ACK, seq = y, ack = x+1|
  | --- ACK, ack = y+1 ----------> |   ESTABLISHED
```

**Termination (four-way)**
```
Client                          Server
  | --- FIN, seq = u ------------> |   active close
  | <-- ACK, ack = u+1 ----------- |   (half-close: server may still send)
  | <-- FIN, seq = v ------------- |   passive close
  | --- ACK, ack = v+1 ----------> |   client waits 2 x MSL (TIME-WAIT)
```"""),
    378: ("Through DNS (after DHCP gives A its own IP)", """1. **A's own address**: A gets its IP address, subnet mask, default gateway and DNS server address from a **DHCP** server (DISCOVER, OFFER, REQUEST, ACK).
2. **B's address**: the user gives a name (e.g. www.example.com). A's resolver sends a **DNS query** (UDP port 53) to its local DNS server.
3. The local server answers from its cache or resolves it **recursively/iteratively**: root server -> TLD server (.com) -> authoritative server for example.com.
4. The IP address of B comes back to A (and is cached).
5. A uses **ARP** to find the MAC address of its default gateway, then opens a TCP connection (3-way handshake) to B's IP address and port."""),
}
