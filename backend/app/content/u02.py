"""Unit 2 - Physical Layer: topology and transmission media (PB Q67-Q116)."""

TITLE = "Physical Layer"
SOURCE = "T1: Unit-2 Network Topology, Unit-2 Transmission Media Notes"

NOTES = {
    "summary": "How devices are physically arranged (topologies) and the media that carry the signal: twisted pair, coax, fibre, and radio/microwave/infrared.",
    "sections": [
        {"h": "Topologies", "points": [
            "**Topology** = geometric arrangement of devices and links. *Physical* topology = actual layout; *logical* = how data flows.",
            "**Mesh**: dedicated point-to-point link between every pair. Links = **n(n-1)/2**, ports per device = **n-1**. Most reliable, most expensive.",
            "**Star**: every device to a central **hub/switch** (controller). Easy to install and isolate faults; hub is a single point of failure.",
            "**Bus**: one **backbone** cable + n drop lines (multipoint). Cheap; a backbone break kills the network, hard to fault-isolate.",
            "**Ring**: each device links to two neighbours; data goes **one direction** (sometimes two in dual ring) through repeaters. A break can disable the ring.",
            "**Tree / Hybrid**: hierarchy of stars / mix of topologies.",
            "**Reliability** = frequency of failure + recovery time after failure.",
        ]},
        {"h": "Guided (bounded) media", "points": [
            "**Twisted pair**: two insulated copper wires twisted to cancel noise. **UTP** (cheap, LAN, RJ-45) and **STP** (foil shield, less EMI). 2 forms.",
            "**Coaxial**: central copper conductor, insulator, braided **shield**, outer jacket. Thinnet (10Base2) / Thicknet (10Base5). Connectors: **BNC, T-connector, terminator, barrel**.",
            "**Optical fibre**: carries **light**; core of **glass or plastic** with cladding of lower refractive index. Works by **total internal reflection** (incidence angle > critical angle).",
            "Fibre modes: **Multimode step-index**, **Multimode graded-index**, **Single-mode** (thinnest core, least dispersion, longest distance).",
            "Fibre advantages: highest bandwidth, immune to EMI, low attenuation, light weight, hard to tap. Disadvantages: costly, fragile, one-way light, skilled installation.",
        ]},
        {"h": "Unguided (wireless) media", "points": [
            "**Ground propagation** below 2 MHz, **sky propagation** (ionosphere) for HF, **line-of-sight** for very high frequencies.",
            "**Radio waves** (3 kHz - 1 GHz): **omnidirectional**, penetrate walls. AM/FM radio, TV, paging.",
            "**Microwaves** (1 - 300 GHz): **unidirectional**, need **line-of-sight**, parabolic dish / horn antennas. Cellular, satellite, WLAN.",
            "**Infrared** (300 GHz - 400 THz): short range, cannot pass walls. TV remotes.",
        ]},
    ],
    "formulas": [
        ["Mesh links", "n(n - 1) / 2"],
        ["Mesh ports per device", "n - 1"],
        ["Star links", "n (one per device to the hub)"],
        ["Bus cables", "1 backbone + n drop lines"],
        ["Ring links", "n"],
    ],
    "traps": [
        "Modem is a device, not a transmission medium.",
        "Microwave is unguided; coax, fibre, twisted pair are guided.",
        "UTP is a twisted-pair type, not a coax connector.",
        "Radio = omnidirectional, microwave = unidirectional (dish).",
        "Interactive applications need full-duplex lines.",
    ],
}

NUMERICAL = {79, 111}

SOL = {
    67: "**Gbps** (10^9 bits per second) is the fastest. Kbps = 10^3 bps, bps = 1. Bandwidth is not a unit.",
    68: "**Multipoint**: three or more devices share one link. Point-to-point is a dedicated link between two devices.",
    69: "The three legitimate modes are simplex, half duplex and full duplex. **Double duplex** does not exist.",
    70: "A **protocol** is the set of rules that governs data communication. Standards are agreed guidelines; a forum is an organization.",
    71: "Both directions, but only one at a time = **half duplex** (like a walkie-talkie).",
    72: "In a **bus** topology all devices tap into the same backbone cable.",
    73: "**Topology** is the geometric arrangement of devices and links.",
    74: "**Star** topology needs a central controller (hub or switch); devices never talk directly.",
    75: "A **bus** is multipoint: one cable shared by all devices. Mesh/star/ring use point-to-point links.",
    76: "**Mesh** is the most reliable: every pair has a dedicated link, so one failed link does not affect others and traffic can be rerouted.",
    77: "Frequency of failure and recovery time are measures of **reliability**.",
    78: "Fully connected mesh with n devices needs **n(n-1)/2** cables (each of the n(n-1) directed links counted once for duplex).",
    79: "Links = n(n-1)/2 = 99 x 98 / 2 = **4851**.",
    80: "A bus uses **one backbone cable and n drop lines** (one per device).",
    81: "The **physical** topology describes the geometric arrangement of the components of the LAN. Logical topology describes the data flow.",
    82: "Signals below 2 MHz travel by **ground propagation**, following the curvature of the earth.",
    83: "A parabolic dish focuses waves in one direction, so it is a **unidirectional** antenna (used for microwaves).",
    84: "**Twisted-pair** cable = two insulated copper wires twisted together to cancel crosstalk and noise.",
    85: "A **guided** medium provides a physical conduit (cable) from one device to another.",
    86: "**Coaxial** cable has a central conductor surrounded by insulation and a metallic **shield** (braid).",
    87: "**Fibre-optic** cables carry data as pulses of light.",
    88: "Radio waves are **omnidirectional**: they spread in all directions, so sender and receiver need not be aligned.",
    89: "The physical layer takes requests from the **data link** layer (the layer directly above it) and turns them into hardware operations.",
    90: "Fibre optics carry **light** waves.",
    91: "The core of an optical fibre is **glass or plastic** (silica).",
    92: "**Optical fibre** has the highest bandwidth / transmission speed (Gbps to Tbps over long distances).",
    93: "A **modem** is a device (modulator-demodulator), not a medium. Telephone lines, coax and microwave are media.",
    94: "Fibre gives **all** of these: hard to tap (resistance to data theft), very high data rate and low noise (immune to EMI).",
    95: "Interactive processing needs both sides to talk simultaneously, so **full-duplex lines** suit it best.",
    96: "Guided media are also called **bound (bounded) media**; unguided = unbound.",
    97: "Twisted pair comes in **2** forms: **UTP** (unshielded) and **STP** (shielded).",
    98: "**Microwave** is wireless, so it is unguided. Coax, fibre and twisted pair are guided.",
    99: "Coax comes as **thinnet** (RG-58, 10Base2) and **thicknet** (RG-8, 10Base5), so A and B both.",
    100: "Coax connectors: BNC, T-connector, terminator, barrel. **UTP** is a cable type (its connector is RJ-45), not a coax connector.",
    101: "Total internal reflection happens when the **incidence angle is greater than the critical angle**; light then reflects back into the core instead of refracting out.",
    102: "The physical layer transmits **raw bits over the channel**. Routing/addressing is the network layer; error detection is data link.",
    103: "**Fibre optic** carries light, so electromagnetic interference does not affect it.",
    104: "Microwaves **require line-of-sight**: they are high-frequency, unidirectional and cannot bend around obstacles or pass well through buildings.",
    105: "**Mesh**: every device has a dedicated point-to-point link to every other device.",
    106: "In a ring, data travels **in one direction** (or two in a dual ring) from device to device until it reaches its destination.",
    107: ("Arrangement of nodes: bus, star, ring, mesh, tree, hybrid", """**Topology** is the geometric (physical or logical) arrangement of devices (nodes) and links in a network.

Common topologies: **Bus, Star, Ring, Mesh**, plus **Tree** (hierarchy of stars) and **Hybrid** (combination)."""),
    108: ("Bus, star, ring, mesh, tree, hybrid with uses", """| Topology | How it works | Pros | Cons | Used in |
|---|---|---|---|---|
| **Bus** | One backbone, devices tap in | Cheap, little cable | Backbone break stops all; hard to troubleshoot | Early Ethernet (10Base2) |
| **Star** | All devices to central hub/switch | Easy install, fault isolation, robust | Hub is single point of failure; more cable | Home / office LANs |
| **Ring** | Each device to 2 neighbours, one direction | Equal access, easy fault location | One break can stop the ring | Token Ring, FDDI, SONET |
| **Mesh** | Dedicated link between every pair | Most reliable, private, no traffic sharing | n(n-1)/2 links, costly | WAN backbones, military |
| **Tree** | Stars connected in a hierarchy | Scalable | Root failure affects branches | Campus networks |
| **Hybrid** | Mix of above | Flexible | Complex | Large enterprises |"""),
    109: ("Guided: twisted pair, coax, fibre. Unguided: radio, microwave, infrared", """**Guided (wired)**
- **Twisted pair** (UTP / STP): telephone lines, Ethernet LANs. Cheap, but limited distance and EMI.
- **Coaxial cable**: cable TV, old Ethernet. Higher bandwidth than twisted pair, shielded.
- **Optical fibre**: backbones, undersea cables. Light signals, highest bandwidth, immune to EMI.

**Unguided (wireless)**
- **Radio waves** (3 kHz - 1 GHz): omnidirectional; AM/FM, TV.
- **Microwaves** (1 - 300 GHz): unidirectional, line-of-sight; satellite, cellular, Wi-Fi.
- **Infrared** (300 GHz - 400 THz): short range, line-of-sight; remote controls."""),
    110: ("Bits to signals, data rate, synchronization, topology, mode", """1. Defines **physical characteristics** of interface and medium.
2. **Representation of bits** (encoding into signals).
3. **Data rate** (bits per second).
4. **Synchronization** of sender and receiver clocks.
5. **Line configuration** (point-to-point / multipoint).
6. **Physical topology** (bus, star, ring, mesh).
7. **Transmission mode** (simplex / half / full duplex)."""),
    111: ("15 cables, 5 ports per device", """- Cables = n(n-1)/2 = 6 x 5 / 2 = **15**
- Ports per device = n - 1 = **5** (total ports = 30)"""),
    112: ("Multimode step-index, multimode graded-index, single-mode", """1. **Multimode step-index**: thick core with constant density; refractive index changes abruptly at the cladding. Beams take many zig-zag paths, so they arrive at different times (**modal dispersion**). Short distances.
2. **Multimode graded-index**: core density is highest at the centre and decreases toward the edge, so beams curve smoothly and arrive more together. Less distortion than step-index.
3. **Single-mode**: very thin core and a highly focused source; beams travel almost horizontally along one path. Almost no dispersion; used for long-distance high-speed links."""),
    113: ("Guided has a physical path; unguided travels through air", """| Guided media | Unguided media |
|---|---|
| Signal travels through a physical conductor | Signal travels through air / vacuum |
| Also called wired / bounded | Also called wireless / unbounded |
| Twisted pair, coax, fibre | Radio, microwave, infrared |
| Direction fixed by cable | Broadcast or directional by antenna |
| Less interference, more secure | More interference, easier to intercept |
| Point-to-point, needs cabling | Easy mobility, no cabling |"""),
    114: ("Centre conductor, insulator, braided shield, jacket", """**Structure**: central copper conductor, insulating layer, braided metal **shield** (outer conductor), plastic protective jacket.

- Carries higher frequencies than twisted pair; shield reduces EMI.
- Categories by RG rating: **RG-59** (cable TV), **RG-58** (thin Ethernet), **RG-11** (thick Ethernet).
- Connectors: **BNC**, **T-connector**, **terminator**, barrel.
- Uses: cable TV, older Ethernet (10Base2, 10Base5), analog telephone trunks.
- Drawback: attenuation is high at high frequencies, so repeaters are needed often."""),
    115: ("Light through glass core by total internal reflection", """**Structure**: **core** (glass/plastic, higher refractive index), **cladding** (lower index), buffer and jacket.

**Principle**: light hits the core-cladding boundary at an angle greater than the critical angle, so **total internal reflection** keeps it inside the core.

**Modes**: multimode step-index, multimode graded-index, single-mode.

**Advantages**: very high bandwidth, low attenuation (long distance), immune to EMI, light, hard to tap.
**Disadvantages**: expensive, needs skilled installation, fragile, unidirectional (needs two fibres for duplex).

**Uses**: Internet backbones, undersea cables, FTTH, data centres."""),
    116: ("3 kHz - 1 GHz, omnidirectional, penetrates walls", """- Radio waves range from about **3 kHz to 1 GHz**.
- **Omnidirectional**: the antenna sends in all directions, so sender and receiver need not be aligned.
- Can travel long distances and **penetrate walls**, which suits broadcasting.
- Drawback: waves from different antennas on the same band interfere; limited bandwidth; easy to intercept.
- Uses: **AM/FM radio, television, maritime radio, cordless phones, paging**.
- Propagation: ground (below 2 MHz), sky / ionospheric (2 - 30 MHz)."""),
}
