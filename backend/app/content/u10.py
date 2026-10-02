"""Unit 10 - Network Designing and Monitoring (PB Q410-Q420)."""

TITLE = "Network Design & Monitoring"
SOURCE = "Practice book Unit 10 (not covered in T1 notes; tool documentation)"

NOTES = {
    "summary": "Command-line utilities for inspecting a network and Wireshark display filters you are expected to recognise.",
    "sections": [
        {"h": "Command-line tools", "points": [
            "**ping**: checks reachability with ICMP Echo, shows RTT and loss.",
            "**traceroute / tracert**: lists every **router (hop)** between source and destination using increasing TTL.",
            "**route**: view and **manipulate the routing table** (route print / add / delete).",
            "**ipconfig** (Windows) / **ifconfig**, `ip a` (Linux): show interface IP, mask, gateway.",
            "**netstat**: active connections and listening ports. **nslookup / dig**: DNS queries. **arp -a**: ARP cache.",
            "**Nmap**: network scanner; **ping sweep** (host discovery), port scanning, OS detection.",
        ]},
        {"h": "Wireshark", "points": [
            "Wireshark is a **network protocol analyzer** (packet capture and inspection).",
            "`ip.addr == x` matches source **or** destination. `ip.src == x` source only. `ip.dst == x` destination only.",
            "`tcp.port == 25` either port. `tcp.dstport == 25` destination port. `tcp.srcport` source port.",
            "`http.host == \"example.com\"` filters by URL host. `http`, `dns`, `tcp.flags.syn == 1` filter by protocol/flag.",
            "Combine with `&&`, `||`, `!`.",
        ]},
        {"h": "Network design checklist", "points": [
            "Gather requirements (users, apps, bandwidth), choose topology and media, plan IP addressing (subnets / VLSM), pick devices, add redundancy and security, document, then monitor (SNMP, Wireshark, logs).",
        ]},
    ],
    "formulas": [
        ["Either address", "ip.addr == 10.10.50.1"],
        ["Destination port", "tcp.dstport == 25"],
        ["By host", "http.host == \"host name\""],
    ],
    "traps": [
        "The real Wireshark destination filter is ip.dst; the practice book writes ip.dest.",
        "traceroute counts routers; route edits the table.",
    ],
}

NUMERICAL = set()

SOL = {
    410: "**Traceroute** sends packets with TTL 1, 2, 3, ...; each router that drops one replies, revealing every hop to the destination.",
    411: "The **route** command manipulates the TCP/IP routing table.",
    412: "A ping sweep (sending pings across a range to find live hosts) is part of **Nmap** (-sn host discovery).",
    413: "Wireshark is a **network protocol analysis** tool.",
    414: "`ip.addr == 10.10.50.1` matches packets where the IP is source **or** destination.",
    415: "The key gives **ip.dest == 10.10.50.1** for destination IP. Note: in real Wireshark the field is **`ip.dst`**; `ip.dest` is not a valid field.",
    416: "Source IP filter: **`ip.src == 10.10.50.1`**.",
    417: "`tcp.port == 25` matches TCP traffic with port 25 as source or destination.",
    418: "Filter by URL/host name: **`http.host == \"host name\"`**.",
    419: "Destination port filter: **`tcp.dstport == 25`**.",
    420: "Packets from or to 8.8.8.8: **`ip.addr==8.8.8.8`**. The others are not valid Wireshark syntax.",
}
