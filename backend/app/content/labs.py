"""Practical list and hands-on projects from the LJU Sem V CN syllabus, with step guides."""

PRACTICALS = [
    {"no": 1, "title": "Implementation of bus topology in Packet Tracer", "units": [1, 2, 10], "guide": """**Aim:** build a bus LAN and test connectivity.

1. Place 4 **PCs** and 4 **switches** (Packet Tracer has no coax bus, so a chain of switches acts as the backbone).
2. Connect each PC to its own switch with a **copper straight-through** cable.
3. Connect the switches in a line with **copper crossover** cables (switch to switch = like devices). This chain is the "bus".
4. Give PCs 192.168.1.1 - 192.168.1.4, mask 255.255.255.0 (Desktop -> IP Configuration).
5. From PC0: `ping 192.168.1.4`. Replies = success.
6. Delete one backbone link and ping again: PCs past the break are unreachable. That is the main weakness of a bus.

**Viva:** bus = one backbone + drop lines, multipoint, cheap, a backbone fault stops the network."""},
    {"no": 2, "title": "Implementation of star topology using switch and hub in Packet Tracer", "units": [1, 2, 10], "guide": """1. Place one **2960 switch** and 4 PCs; connect each PC with a **straight-through** cable.
2. Assign 192.168.1.1-.4 /24 and ping between PCs.
3. Repeat with a **hub** (Network Devices -> Hubs).
4. Switch to **Simulation mode**, send a ping, and compare:
   - **Hub**: the frame is copied to every port (one collision domain).
   - **Switch**: after learning MAC addresses, the frame goes only to the destination port (`show mac address-table` on the switch).

**Viva:** star needs a central device; hub = layer 1, switch = layer 2; a switch gives each port its own collision domain."""},
    {"no": 3, "title": "Perform TCP/IP configuration for a PC network", "units": [5], "guide": """**On Windows**
1. Settings -> Network -> Change adapter options -> Ethernet -> Properties -> IPv4 -> Properties.
2. Set IP 192.168.1.10, mask 255.255.255.0, gateway 192.168.1.1, DNS 8.8.8.8 (or choose "Obtain automatically" for DHCP).
3. Verify in Command Prompt:
```
ipconfig /all
ping 192.168.1.1
ping 8.8.8.8
nslookup google.com
tracert google.com
```

**In Packet Tracer:** Desktop -> IP Configuration -> Static or DHCP.

**Viva:** IP identifies the host, mask separates network and host bits, gateway is the router for other networks, DNS resolves names."""},
    {"no": 4, "title": "Write a program for an error detecting mechanism", "units": [3], "guide": """A CRC sender and receiver in Python (same mod-2 division as Unit 3):

```python
def xor_divide(dividend: str, key: str) -> str:
    bits = list(dividend)
    for i in range(len(bits) - len(key) + 1):
        if bits[i] == "1":
            for j, k in enumerate(key):
                bits[i + j] = "0" if bits[i + j] == k else "1"
    return "".join(bits[-(len(key) - 1):])

def crc_send(data: str, key: str) -> str:
    rem = xor_divide(data + "0" * (len(key) - 1), key)
    return data + rem

def crc_check(codeword: str, key: str) -> bool:
    return set(xor_divide(codeword, key)) == {"0"}

sent = crc_send("1101011011", "10011")
print("Transmitted:", sent)              # 11010110111110
print("No error:", crc_check(sent, "10011"))
print("Corrupted:", crc_check("11010110101110", "10011"))
```
Try it on Q153 and Q156 and compare with the solutions. Variations: parity (VRC), checksum, Hamming."""},
    {"no": 5, "title": "IP addressing basics", "units": [5], "guide": """1. Identify the class from the first octet: A 1-126, B 128-191, C 192-223.
2. Network address = IP AND mask; broadcast = host bits all 1; usable hosts = 2^h - 2.
3. Subnet 192.168.10.0/24 into 4 subnets: borrow 2 bits -> /26, block size 64.

| Subnet | Network | First host | Last host | Broadcast |
|---|---|---|---|---|
| 1 | 192.168.10.0 | .1 | .62 | .63 |
| 2 | 192.168.10.64 | .65 | .126 | .127 |
| 3 | 192.168.10.128 | .129 | .190 | .191 |
| 4 | 192.168.10.192 | .193 | .254 | .255 |

4. Build it in Packet Tracer: one router with 4 interfaces (or a router + switches), one PC per subnet, ping across subnets. More practice: Unit 5, Q248-Q260."""},
    {"no": 6, "title": "Implementation of static routing", "units": [6], "guide": """Topology: PC0 - R1 - R2 - PC1. Networks: 192.168.1.0/24 (PC0-R1), 10.0.0.0/30 (R1-R2), 192.168.2.0/24 (R2-PC1).

```
R1(config)# interface g0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.0
R1(config-if)# no shutdown
R1(config)# interface g0/1
R1(config-if)# ip address 10.0.0.1 255.255.255.252
R1(config-if)# no shutdown
R1(config)# ip route 192.168.2.0 255.255.255.0 10.0.0.2

R2(config)# ... (mirror: g0/0 192.168.2.1, g0/1 10.0.0.2)
R2(config)# ip route 192.168.1.0 255.255.255.0 10.0.0.1
```
PCs: gateway = their router's LAN address. Test `ping` and `tracert`; check `show ip route` (S = static)."""},
    {"no": 7, "title": "Implementation of dynamic routing using RIP", "units": [6], "guide": """Same topology as Practical 6, but remove the static routes and add:

```
R1(config)# router rip
R1(config-router)# version 2
R1(config-router)# no auto-summary
R1(config-router)# network 192.168.1.0
R1(config-router)# network 10.0.0.0
```
Repeat on R2 with its networks. Verify `show ip route` (R entries, metric = hop count) and `show ip protocols`.

**Viva:** RIP is distance vector (Bellman-Ford), metric = hops, max 15, updates every 30 s, slow convergence / count-to-infinity."""},
    {"no": 8, "title": "Implementation of dynamic routing using OSPF", "units": [6], "guide": """```
R1(config)# router ospf 1
R1(config-router)# network 192.168.1.0 0.0.0.255 area 0
R1(config-router)# network 10.0.0.0 0.0.0.3 area 0
```
Repeat on R2. Verify: `show ip ospf neighbor` (state FULL), `show ip route` (O entries).

**Viva:** OSPF is link state (Dijkstra), uses cost = reference bandwidth / interface bandwidth, areas, fast convergence, wildcard mask = inverse of subnet mask."""},
    {"no": 9, "title": "Implementation of application layer protocol: HTTP", "units": [9], "guide": """**Packet Tracer:** add a **Server**; Services -> HTTP -> On; edit index.html. Give it an IP (192.168.1.100). On a PC: Desktop -> Web Browser -> `http://192.168.1.100`. Add a DNS record (Services -> DNS: www.lab.com -> 192.168.1.100) and browse by name.

**Python (real machine):**
```
python -m http.server 8080
```
Open http://localhost:8080 and watch the GET requests and 200/404 status codes in the terminal.

**Viva:** HTTP runs on TCP port 80, request-response, stateless; methods GET/POST; status 200, 301, 404, 500."""},
    {"no": 10, "title": "Study of Wireshark tool", "units": [10], "guide": """1. Open Wireshark, choose the active Wi-Fi/Ethernet interface, click the shark fin to capture.
2. Browse a website, then stop.
3. Apply filters:
   - `http` or `tls`, `dns`, `tcp.flags.syn == 1` (handshakes)
   - `ip.addr == 8.8.8.8`, `ip.src == x`, `ip.dst == x`
   - `tcp.port == 443`, `tcp.dstport == 80`
4. Click a packet: see Ethernet II -> IP -> TCP -> HTTP layers (the TCP/IP stack in action).
5. Statistics -> **Protocol Hierarchy**, **Conversations**, **Flow Graph** (shows SYN, SYN-ACK, ACK).

**Viva:** Wireshark is a protocol analyzer; capture filter vs display filter; it shows header fields of every layer."""},
]

PROJECTS = [
    {"no": 1, "title": "Cable construction and testing (CAT 5/6 straight-through and crossover)", "units": [1, 2], "guide": """**Tools:** CAT5/6 cable, RJ-45 connectors, crimping tool, cable tester.

| Pin | T568A | T568B |
|---|---|---|
| 1 | white-green | white-orange |
| 2 | green | orange |
| 3 | white-orange | white-green |
| 4 | blue | blue |
| 5 | white-blue | white-blue |
| 6 | orange | green |
| 7 | white-brown | white-brown |
| 8 | brown | brown |

- **Straight-through:** both ends T568B (PC-switch).
- **Crossover:** one end T568A, the other T568B (PC-PC, switch-switch).

Steps: strip 2-3 cm of jacket, untwist and order the pairs, cut evenly, insert into the RJ-45 (clip down), crimp, then test: all 8 LEDs light in order (straight) or 1-3, 2-6 swapped (crossover)."""},
    {"no": 2, "title": "Peer-to-peer network and switched LAN with 4 PCs", "units": [1, 2], "guide": """a. Two PCs, **crossover** cable, IPs 192.168.1.1 and .2 /24, ping each other.
b. One switch, 4 PCs, **straight-through** cables, IPs .1-.4, ping all pairs. Record the design (diagram + IP table) and the ping results."""},
    {"no": 3, "title": "Internetwork with multiple subnets and routers", "units": [5], "guide": """a. Two subnets: 192.168.1.0/24 (2 hosts + switch) and 192.168.2.0/24 (1 host), joined by one router.
b. Three subnets: two host subnets plus a 10.0.0.0/30 link between two routers; add static routes (Practical 6) or RIP/OSPF.
c. Join with another group's network: agree non-overlapping subnets and add routes to their networks.
Record each design, the IP plan, and ping/tracert results."""},
    {"no": 4, "title": "Configure DHCP on a Cisco 1841 router", "units": [5], "guide": """Requirement: pool 192.168.1.0/24, first 49 addresses excluded, gateway 192.168.1.1, DNS 192.168.1.10, passwords `cisco`.

```
Router> enable
Router# configure terminal
Router(config)# enable secret cisco
Router(config)# line console 0
Router(config-line)# password cisco
Router(config-line)# login
Router(config-line)# exit
Router(config)# interface fastEthernet0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.49
Router(config)# ip dhcp pool LAN
Router(dhcp-config)# network 192.168.1.0 255.255.255.0
Router(dhcp-config)# default-router 192.168.1.1
Router(dhcp-config)# dns-server 192.168.1.10
Router(dhcp-config)# end
Router# show ip dhcp binding
```
Set PCs to DHCP: they receive 192.168.1.50 onward. DHCP steps: Discover, Offer, Request, Ack (DORA)."""},
    {"no": 5, "title": "Packet capture and analysis with Wireshark", "units": [10], "guide": """a. Capture while browsing a site; for a few packets note the protocol of each layer, key header fields (IP TTL, TCP ports, seq/ack numbers, HTTP method/status) and packet sizes.
b. Explore: display filters, **Statistics -> Flow Graph** (TCP handshake), **Protocol Hierarchy**, **Conversations**, **I/O Graph**. See Practical 10 for the filter list."""},
]
