"""Unit 4 - Data Link Layer and MAC sublayer (PB Q163-Q213)."""

TITLE = "MAC Sublayer & Ethernet"
SOURCE = "T1: CN Notes T2 Unit-4 Access Control, MAC Protocols, Unit-4 Examples and Ethernet"

NOTES = {
    "summary": "Who gets to transmit on a shared channel: ALOHA, CSMA, CSMA/CD (Ethernet), CSMA/CA (Wi-Fi), plus the Ethernet frame.",
    "sections": [
        {"h": "ALOHA", "points": [
            "**Pure ALOHA**: send whenever you have a frame; no ACK -> wait a random back-off time **TB = R x Tp (or Tfr)** with R in 0..2^K - 1, then resend. Give up after Kmax (usually 15) tries.",
            "Random wait is to **avoid more collisions** (stations that collided must not retry together).",
            "Pure ALOHA **vulnerable time = 2 x Tfr**. Throughput **S = G e^(-2G)**, max **0.184 at G = 0.5**.",
            "**Slotted ALOHA**: may send only at slot start. Vulnerable time = **Tfr**. **S = G e^(-G)**, max **0.368 at G = 1**.",
            "G = average frames generated **per frame time** (Tfr = frame bits / bandwidth).",
        ]},
        {"h": "CSMA family", "points": [
            "**CSMA** = Carrier Sense Multiple Access: listen before talk. Vulnerable time = **Tp**.",
            "Persistence methods: **1-persistent** (send immediately when idle), **non-persistent** (wait random time then sense again), **p-persistent** (send with probability p in slotted channels). No 'A-persistent'.",
            "**CSMA/CD** (Ethernet, wired): transmit while monitoring; on collision send **jam signal**, **K = K + 1**, wait back-off R x slot with **R in 0..2^K - 1**, retry.",
            "CSMA/CD rule: frame must still be transmitting when the collision returns -> **Tfr >= 2 x Tp**, so **min frame = 2 x Tp x bandwidth** (Ethernet: 512 bits = 64 bytes).",
            "**CSMA/CA** (Wi-Fi, wireless): collisions cannot be detected, so avoid them with **IFS**, **contention window** and **ACK**. After sending, wait for ACK until time-out. IFS also sets **priority**.",
        ]},
        {"h": "Ethernet (IEEE 802.3)", "points": [
            "Frame: **Preamble (7 B)** 10101010... | **SFD (1 B) 10101011** | Dest MAC (6) | Src MAC (6) | Type/Length (2) | **Data 46 - 1500 B** | CRC (4).",
            "Min frame 64 B, max 1518 B (excluding preamble/SFD). Max payload **1500 B** (= MTU).",
            "Standards: 10BASE5 (thick coax), 10BASE2 (thin coax), **10BASE-T** (twisted pair), 10BASE-F (fibre), Fast (100 Mbps), Gigabit, 10G.",
            "**IEEE 802.3** = Ethernet (wired). **802.11** = Wi-Fi. 802.15 = Bluetooth.",
        ]},
    ],
    "formulas": [
        ["Frame time", "Tfr = frame size / bandwidth"],
        ["Load G", "frames per second x Tfr"],
        ["Pure ALOHA", "S = G e^(-2G), Smax = 0.184 (G = 1/2)"],
        ["Slotted ALOHA", "S = G e^(-G), Smax = 0.368 (G = 1)"],
        ["Successful frames/s", "S x (frames generated per second)"],
        ["Back-off after K collisions", "R in {0 .. 2^K - 1},  P(R = x) = 1 / 2^K,  TB = R x slot"],
        ["CSMA/CD min frame", "Lmin = 2 x Tp x bandwidth"],
        ["Max channel use", "Smax x link rate (e.g. 800 kbps x 0.184 = 147.2 kbps)"],
    ],
    "traps": [
        "K is capped at 10 for the range: R in 0..2^min(K,10) - 1.",
        "After the n-th collision K = n, so there are 2^n possible values.",
        "Collision detection is impossible in wireless: Wi-Fi uses CSMA/CA, not CD.",
        "SFD ends in 11 (10101011); preamble bytes are 10101010.",
        "x^5 + 2x + 1 is not a valid binary (GF(2)) polynomial: coefficient 2 is not allowed.",
    ],
}

NUMERICAL = {181, 182, 196, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213}

SOL = {
    163: "Stations that collided must not retry at the same moment, or they collide again. A random back-off spreads them out, **to avoid more collisions**.",
    164: "Pure ALOHA limits congestion by a **restriction on the number of re-transmission attempts** (Kmax, usually 15). After that the station aborts.",
    165: "A frame collides with any frame starting from Tfr before it to Tfr after it, so the vulnerable time is **2 x T**.",
    166: "S = G e^(-2G). dS/dG = 0 gives G = **0.5**, where S = 0.5 x e^(-1) = 0.184.",
    167: "Max throughput of pure ALOHA = 18.4%, so usable bandwidth = 0.184 x 800 kbps = **147.2 kbps**.",
    168: "Pure ALOHA throughput is **S = G x e^(-2G)** (the 2 comes from the 2 x Tfr vulnerable time).",
    169: "Maximum throughput for pure ALOHA = 1/(2e) = **0.184** (18.4%).",
    170: "Slotted ALOHA: S = G e^(-G) is maximum at **G = 1**.",
    171: "Slotted ALOHA: **S = G x e^(-G)** (vulnerable time is only Tfr).",
    172: "Maximum throughput for slotted ALOHA = 1/e = **0.368** (36.8%).",
    173: "0.368 x 800 kbps = **294.4 kbps**.",
    174: "ALOHA was designed for radio broadcast on a shared frequency (University of Hawaii), so the answer is the **ALOHA protocol**.",
    175: "**ALOHA** is a medium access control protocol for transmitting over a shared channel.",
    176: "CSMA = **Carrier Sense Multiple Access**.",
    177: "The CSMA persistence methods are 1-persistent, non-persistent and p-persistent. **A-persistent** does not exist.",
    178: "CSMA/CA avoids collisions using **all three**: Interframe Space (IFS), the Contention Window and Acknowledgements.",
    179: "CSMA/CD flow: collision detected -> send jam signal -> **increment K** -> if K > Kmax abort, else wait random back-off and retry.",
    180: "CSMA/CA flow: after sending the frame, the station **waits for the time-out** (for an ACK). ACK received = success; otherwise K is incremented and it retries.",
    181: "After the 5th collision K = 5, so R is chosen from 0..2^5 - 1 = 0..31 (32 values). P(R = 4) = 1/32 = **0.03125**.",
    182: """Tp = 1 km / 200,000 km/s = 5 us. Minimum frame time = 2 x Tp = 10 us.

Lmin = 10 x 10^-6 x 10^9 = 10,000 bits = **1250 bytes**""",
    183: "In CSMA/CA the **Inter Frame Space (IFS)** is also used to set priority: a shorter IFS means higher priority.",
    184: "A wireless station cannot hear a collision while it is transmitting (its own signal drowns everything; hidden stations), so **collision detection** is not possible. Wi-Fi uses CSMA/CA.",
    185: "CSMA/CD is the MAC method of classic **Ethernet**. Wi-Fi uses CSMA/CA.",
    186: "The Start Frame Delimiter is **10101011**: the final 11 tells the receiver that the next bits are the destination address.",
    187: "Wi-Fi = **IEEE 802.11**.",
    188: "Ethernet payload is 46 to **1500 bytes**.",
    189: "**Ethernet** is the standard protocol, built into hardware and software, for wired LANs.",
    190: "Ethernet = **IEEE 802.3**.",
    191: "IEEE 802.3 covers **wired Ethernet** networking (physical layer and MAC).",
    192: "**10BASE-T**: 10 Mbps, baseband, twisted pair. The others are not real standards.",
    193: "Binary (mod-2) polynomials can only have coefficients 0 or 1. **2x** is not valid, so none of the binary strings is a correct conversion: **None of the above**. (If 2x is reduced mod 2 it disappears, giving x^5 + 1 = 100001.)",
    194: "Each ESC or FLAG in the data gets an ESC in front: ESC -> **ESC ESC**, Flag -> **ESC Flag**, ESC -> **ESC ESC**. Result: ESC, ESC, ESC, flag, ESC, ESC.",
    195: "Remove the stuffed 0 that follows each run of five 1s: in the stuffed stream ...11111**0**1... the bold 0 is dropped. Reading the data part this way gives **111110101** (option B). (The original GATE 2014 question has output 01111100101 and input 0111110101.)",
    196: "After the 6th collision K = 6, so R is chosen from 0..2^6 - 1: **64** distinct values.",
    197: "CSMA/CD is a medium access method, so it is in the **Data Link layer** (MAC sublayer).",
    198: ("135 frames/s", """Tfr = 200 bits / 200 kbps = **1 ms**. 1000 frames/s = 1 frame per ms, so **G = 1**.

S = G e^(-2G) = 1 x e^(-2) = **0.135**

Throughput = 1000 x 0.135 = **135 frames/s** survive."""),
    199: ("92 frames/s", """Tfr = 1 ms. 500 frames/s = 0.5 frame per ms, so **G = 0.5**.

S = 0.5 x e^(-1) = **0.184** (the maximum)

Throughput = 500 x 0.184 = **92 frames/s**"""),
    200: ("38 frames/s", """Tfr = 1 ms. 250 frames/s -> **G = 0.25**.

S = 0.25 x e^(-0.5) = **0.152**

Throughput = 250 x 0.152 = **38 frames/s**"""),
    201: ("5000 frames/s per station", """Pure ALOHA is most efficient at G = 1/2: half a frame per Tfr = 1 us.

Total = 0.5 / 10^-6 = 500,000 frames/s for the system.

Per station = 500,000 / 100 = **5000 frames per second**"""),
    202: ("135", """Tfr = 1000 / 10^6 = 1 ms. Rate 1000 frames/s -> G = 1000 x 1 ms = **1**.

S = G e^(-2G) = e^(-2) = 0.1353

Throughput = 1000 x 0.1353 = **135 frames/s**"""),
    203: ("50 frames/s (both)", """G = 1 means 1 frame generated per frame time. Tfr = 20 ms, so frames per second = 1 / 0.020 = **50** for both pure and slotted ALOHA.

Successful frames: pure = 50 x e^(-2) = 6.77 per s; slotted = 50 x e^(-1) = 18.4 per s."""),
    204: ("10,000 frames/s per station", """Slotted ALOHA is best at G = 1: one frame per Tfr = 1 us -> 10^6 frames/s in total.

Per station = 10^6 / 100 = **10,000 frames per second**"""),
    205: ("368 frames/s", "Tfr = 1 ms, G = 1. S = 1 x e^(-1) = 0.368. Throughput = 1000 x 0.368 = **368 frames/s**."),
    206: ("151 frames/s", "G = 0.5. S = 0.5 x e^(-0.5) = 0.303. Throughput = 500 x 0.303 = **151 frames/s**."),
    207: ("49 frames/s", "G = 0.25. S = 0.25 x e^(-0.25) = 0.195. Throughput = 250 x 0.195 = **49 frames/s**."),
    208: ("K=1: 0 or 2 ms; K=2: 0,2,4,6 ms; K=3: 0..14 ms", """TB = R x Tp with Tp = 2 ms and R in 0..2^K - 1.

- **K = 1**: R in {0, 1} -> TB = **0 or 2 ms**
- **K = 2**: R in {0..3} -> TB = **0, 2, 4, 6 ms**
- **K = 3**: R in {0..7} -> TB = **0, 2, 4, ..., 14 ms**

(If K > 10 it is normally set to 10.)"""),
    209: ("No other station sends within 1 ms before or during this frame", """Tfr = 200 bits / 200 kbps = **1 ms**. Vulnerable time = 2 x Tfr = **2 ms**.

So **no other station may start sending within 1 ms before** this station starts, and **none may start during the 1 ms** this station is sending."""),
    210: ("512 bits = 64 bytes", """Tfr(min) = 2 x Tp = 2 x 25.6 = **51.2 us**

Lmin = 10 Mbps x 51.2 us = **512 bits = 64 bytes** (the Ethernet minimum frame)."""),
    211: ("1/8 = 0.125", "After the 3rd collision K = 3, so R in 0..7 (8 values). P(K value = 2) = **1/8 = 0.125**."),
    212: ("1/16; 0.625 us", """After the 4th collision K = 4, so R in 0..15 (16 values). P(R = 5) = **1/16 = 0.0625**.

Delay = R x Tfr = 5 x 0.125 us = **0.625 us** (6.25 x 10^-7 s)."""),
    213: ("1/64; 5 us", """After the 6th collision R in 0..63 (64 values). P(R = 10) = **1/64 = 0.015625**.

Delay = 10 x 0.5 us = **5 us** (5 x 10^-6 s)."""),
}
