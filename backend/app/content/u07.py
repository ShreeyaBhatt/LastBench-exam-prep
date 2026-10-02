"""Unit 7 - Introduction to the Transport Layer (PB Q296-Q322)."""

TITLE = "Transport Layer Basics"
SOURCE = "Practice book Unit 7 (not covered in T1 notes; standard Forouzan / Kurose content)"

NOTES = {
    "summary": "Process-to-process delivery with port numbers, multiplexing, sockets, and the services the transport layer gives applications.",
    "sections": [
        {"h": "Role", "points": [
            "Transport = **process-to-process** delivery (network layer is host-to-host, data link is node-to-node).",
            "Address used = **port number** (16 bits, **0 - 65,535**). IP + port = **socket**, the endpoint of a connection (TCP's name for a transport service access point is the **port**).",
            "Ports: **0-1023 well-known**, **1024-49151 registered**, **49152-65535 dynamic / private (ephemeral)**. Clients use ephemeral ports.",
            "Unit of data = **segment** (TCP) / user datagram (UDP).",
        ]},
        {"h": "Services", "points": [
            "**Multiplexing** at sender (many processes -> one IP stream) and **demultiplexing** at receiver (by port).",
            "**Connectionless** (UDP: no setup, independent datagrams) vs **connection-oriented** (TCP: handshake, ordered, reliable).",
            "End-to-end **flow control** (receiver buffer), **error control** (checksum, ACK, retransmission, ARQ), **congestion control**.",
            "Segmentation and reassembly with sequence numbers.",
            "TCP = reliable; **UDP does not** provide reliable end-to-end delivery. SSL/TLS works on top of the transport layer.",
        ]},
        {"h": "Multiplexing (TDM)", "points": [
            "Multiplexing = sharing one link among several devices. A **multiplexer** combines several inputs into one line.",
            "Synchronous TDM: n sources -> **n slots per frame**; empty slots are wasted.",
            "Link rate = frames per second x bits per slot x slots.",
        ]},
        {"h": "Sliding window throughput", "points": [
            "A window of W packets can be sent per RTT, so **rate = W / RTT** (limited by link capacity).",
        ]},
    ],
    "formulas": [
        ["Port range", "0 to 2^16 - 1 = 65,535"],
        ["Sliding window rate", "min( W / RTT, link capacity )"],
        ["TDM link rate", "frames/s x bits per frame"],
        ["Sync TDM efficiency", "used slots / total slots"],
    ],
    "traps": [
        "IP address = host, port = process. Transport uses port addresses.",
        "TCP header 20-60 bytes; UDP header fixed 8 bytes.",
        "Fragment offset is an IP field, not TCP.",
        "TCP is a byte stream, not a message stream.",
    ],
}

NUMERICAL = {313, 316, 320}

SOL = {
    296: "The transport layer multiplexes data from many applications and hands it to the **network layer** below it.",
    297: "Transport protocols provide **process-to-process** communication (between application processes on two hosts).",
    298: "TCP calls its transport service access point a **port**. (Socket = IP address + port.)",
    299: "Multiplexing/demultiplexing, connectionless and connection-oriented service, and congestion control are **all** transport-layer functions.",
    300: "UDP = **User Datagram Protocol**.",
    301: "Port numbers are 16 bits: **0 to 65,535**.",
    302: "I is true (TCP is full duplex). II is false: TCP has a **SACK (selective acknowledgement) option**. III is false: TCP is a **byte stream**, not a message stream. So **only I**.",
    303: "Sequence number, window size and checksum are TCP header fields. **Fragment offset** is an IP header field.",
    304: "UDP is connectionless because **each datagram is treated independently**: no connection setup, no relation between datagrams.",
    305: "Process-to-process delivery uses the **port address**.",
    306: "The transport layer reacts to overloaded nodes with **flow control** (and congestion control), slowing the sender.",
    307: "SSL = **Secure Socket Layer**; it sits on top of TCP and secures data at the **transport layer** (now TLS).",
    308: "Like the **data link layer**, the transport layer can do flow and error control, but end-to-end instead of hop-to-hop.",
    309: "A **multiplexer** combines transmissions from several I/O devices onto one line.",
    310: "**TCP and UDP** are transport protocols. FTP and HTTP are application protocols.",
    311: "Sharing one medium/link among two or more devices is **multiplexing**.",
    312: "With n sources of equal rate, each TDM frame has **n** slots (one per source).",
    313: "Rate = 4000 frames/s x 8 bits = 32,000 bps = **32 kbps**.",
    314: "**UDP** gives no reliability: no ACKs, no retransmission, no ordering.",
    315: "ARQ = **Automatic Repeat Request**.",
    316: "Synchronous TDM keeps a slot for every device even when empty. Used slots = 3 of 5, efficiency = 3/5 = **0.6** (60%).",
    317: "0-1023 **well-known**, 1024-49151 **registered**, 49152-65535 **dynamic** (private/ephemeral).",
    318: "TCP header: **20 bytes minimum** (no options), **60 bytes maximum** (40 bytes of options). HLEN is 4 bits x 4 bytes.",
    319: ("Process-to-process delivery, ports, segmentation, connection, flow, error, congestion control", """1. **Process-to-process delivery** using port numbers.
2. **Multiplexing and demultiplexing** of many application streams.
3. **Segmentation and reassembly** with sequence numbers.
4. **Connection control**: connection-oriented (TCP) or connectionless (UDP).
5. **Flow control** end to end (sliding window, rwnd).
6. **Error control**: checksum, ACKs, retransmission of lost/damaged segments.
7. **Congestion control** (TCP slow start, congestion avoidance).
8. Ordered delivery, duplicate detection."""),
    320: ("40 packets/s", """With a fixed window of 4 packets, the sender can have 4 unacknowledged packets per round trip.

Rate = W / RTT = 4 packets / 0.1 s = **40 packets/s**

This is below the link capacity (100 packets/s), so the window, not the link, limits traffic. To use the full link you need W >= 100 x 0.1 = 10 packets."""),
    321: ("TCP and UDP", """1. **TCP (Transmission Control Protocol)**: connection-oriented, reliable, ordered byte stream, flow and congestion control. Used by HTTP, FTP, SMTP.
2. **UDP (User Datagram Protocol)**: connectionless, unreliable, low overhead, 8-byte header. Used by DNS, streaming, VoIP, online games.

(SCTP is a third, less common transport protocol.)"""),
    322: ("Services + socket = IP address + port", """**Services of the transport layer**
- Process-to-process delivery, multiplexing/demultiplexing
- Connection-oriented and connectionless service
- Reliable delivery (error control, ACKs, retransmission)
- Flow control and congestion control
- Segmentation and reassembly, in-order delivery

**Socket**
A socket is the endpoint of communication: **socket address = IP address + port number** (e.g. 192.168.1.5:80). A TCP connection is uniquely identified by the pair of sockets (client IP:port, server IP:port).

**Importance**
- Identifies the exact **process** on a host, so the transport layer can demultiplex segments.
- Lets one server serve many clients at once (each connection has a different client socket).
- Provides the programming interface (socket API: socket, bind, listen, accept, connect, send, recv) that applications use to access TCP/UDP."""),
}
