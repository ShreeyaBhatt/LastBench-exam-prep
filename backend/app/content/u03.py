"""Unit 3 - Data Link Layer and LLC sublayer (PB Q117-Q162)."""

TITLE = "Data Link Layer & LLC"
SOURCE = "T1: CN Notes T2 Unit-3 LLC, DLL Design Issues - Services, DLL Protocols, ERROR-CONTROL"

HAM_NOTE = "**Bit numbering:** the T1 notes (Forouzan) number Hamming positions **from the right**: position 1 is the rightmost bit, parity bits sit at positions 1, 2, 4, 8."

NOTES = {
    "summary": "Framing, error detection (VRC, LRC, checksum, CRC), error correction (Hamming), and flow/error control protocols (Stop-and-Wait, Go-Back-N, Selective Repeat).",
    "sections": [
        {"h": "Framing", "points": [
            "Physical layer sends bits; DLL marks where each **frame** starts and ends.",
            "**Character count**: header says how many characters follow. One corrupted count breaks sync.",
            "**Byte (character) stuffing**: frame bounded by FLAG bytes. A FLAG or ESC inside data gets an **ESC added before it**. Receiver drops one ESC of each pair.",
            "**Bit stuffing**: flag = **01111110**. Sender inserts a **0 after five consecutive 1s** in data; receiver removes it. More efficient than byte stuffing.",
        ]},
        {"h": "Error detection", "points": [
            "**Single-bit error**: 1 bit changed. **Burst error**: 2+ bits changed; burst length = first corrupted bit to last corrupted bit.",
            "**VRC (parity)**: one parity bit per unit. Detects all single-bit and odd-count errors.",
            "**LRC**: arrange blocks in rows, compute parity of each column (XOR of rows). Detects bursts, misses some even patterns.",
            "**Checksum**: split into k segments of m bits, add with **wrap-around carry** (1's complement), complement the sum. Receiver adds everything incl. checksum and complements: **all 0s = accept**.",
            "**CRC**: append (degree) zeros to data, divide by generator using **XOR (mod-2)**, append remainder. Receiver divides codeword: **remainder 0 = no error**. Key/divisor is known to **both** sides. Strongest detector.",
            "Polynomial to binary: x^5 + x + 1 = 1x^5+0x^4+0x^3+0x^2+1x+1 = **100011**.",
        ]},
        {"h": "Hamming code (correction)", "points": [
            "Redundant bits r must satisfy **2^r >= m + r + 1**. m=4 -> r=3 (7,4); m=7 -> r=4 (11 bits).",
            "Parity bits at positions **1, 2, 4, 8** (powers of 2). r1 checks positions with bit-1 set (1,3,5,7,9,11), r2 checks (2,3,6,7,10,11), r4 checks (4,5,6,7), r8 checks (8,9,10,11).",
            "Receiver recomputes checks; the binary number c8c4c2c1 = **position of the error**. 0 = no error.",
            "Hamming distance = number of differing bits (XOR and count 1s). Min distance of Hamming code = **3**: detect 2, correct 1.",
            "Detection is easier than correction. ARQ = receiver asks for retransmission; FEC = receiver corrects itself.",
        ]},
        {"h": "Flow & error control (ARQ)", "points": [
            "**Stop-and-Wait**: send 1 frame, wait for ACK. Window = 1. Lost frame or lost ACK -> timeout -> resend (sequence numbers 0/1 catch duplicates).",
            "**Go-Back-N**: sender window up to 2^m - 1, **receiver window = 1**. A lost frame forces resending it and **all frames after it**.",
            "**Selective Repeat**: sender and receiver window up to 2^(m-1); only the damaged/lost frame is resent.",
            "ACK number = **next expected frame** (receive frame 8 -> send ACK 9).",
            "RTT = 2 x propagation delay.",
        ]},
    ],
    "formulas": [
        ["Hamming redundant bits", "2^r >= m + r + 1"],
        ["Hamming(7,4) message length", "k = 2^r - r - 1"],
        ["CRC remainder size", "degree of generator = (key length - 1)"],
        ["Burst length", "position of last flipped bit - first flipped bit + 1"],
        ["Checksum", "complement( 1's complement sum of segments )"],
        ["RTT", "2 x Tp"],
        ["Stop-and-Wait, every kth tx lost", "count transmissions; each loss adds one retransmission"],
        ["Number of MAC addresses", "2^48"],
    ],
    "traps": [
        "Hamming bit order: T1 notes number from the right. Check which end is position 1.",
        "Checksum: add the carry back (wrap-around) before complementing.",
        "In CRC append (key length - 1) zeros, not key length.",
        "Go-Back-N receiver window is always 1, regardless of sender window.",
        "A MAC address uses hex digits 0-9 and A-F only; 'G' is invalid. FF:FF:FF:FF:FF:FF is broadcast.",
    ],
}

NUMERICAL = {136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
             153, 154, 155, 156, 157, 158, 159, 160, 161, 162}

SOL = {
    117: "Framing, error control and flow control are DLL jobs. **Channel coding** (modulation/signal encoding) belongs to the physical layer.",
    118: "When 2 or more bits change, it is a **burst error**. (Changed bits need not be consecutive.)",
    119: "A MAC address is 12 **hex** digits (0-9, A-F). Option D contains **1G**, and G is not a hex digit, so it is invalid.",
    120: "**FF:FF:FF:FF:FF:FF** (all 48 bits = 1) is the broadcast MAC address; every NIC on the LAN accepts it.",
    121: "**Hamming code** both detects and corrects (single-bit) errors. LRC, VRC and CRC only detect.",
    122: "The CRC generator (key/divisor) must be known to **both** the sender (to compute the remainder) and the receiver (to check it).",
    123: "In Go-Back-N the receiver accepts frames only in order, so its window size is **1**.",
    124: f"""{HAM_NOTE}

The answer key (**A: 1010101**) uses the **left-to-right** order p1 p2 d3 p4 d5 d6 d7 with data 1101:
- p1 = d3 ^ d5 ^ d7 = 1 ^ 1 ^ 1 = **1**
- p2 = d3 ^ d6 ^ d7 = 1 ^ 0 ^ 1 = **0**
- p4 = d5 ^ d6 ^ d7 = 1 ^ 0 ^ 1 = **0**
- Codeword = 1 0 1 0 1 0 1 = **1010101**

With the notes' right-to-left order (d7 d6 d5 r4 d3 r2 r1) the same data gives 1100110 (option D). Follow whichever convention your examiner uses; the key here uses left-to-right.""",
    125: "In bit stuffing a **0 is stuffed after five consecutive 1s** so data never looks like the flag 01111110.",
    126: "**Bit stuffing** is more efficient: it adds 1 bit when needed, while byte stuffing adds a whole 8-bit ESC byte.",
    127: "In **ARQ (Automatic Repeat Request)** the receiver asks the sender to resend. In FEC the receiver corrects errors itself.",
    128: "The CRC divisor is called the **generator** (generator polynomial).",
    129: "The minimum Hamming distance of the Hamming code is **3**, so it can detect up to 2-bit errors and correct 1-bit errors.",
    130: "k data bits + r redundant bits = n-bit blocks called **codewords**. The original k-bit blocks are datawords.",
    131: "For Hamming codes n = 2^r - 1, so k = n - r = **2^r - r - 1**. For r = 3: k = 8 - 3 - 1 = 4, giving (7,4).",
    132: "**Correction** of errors is more difficult than **detection**: detection only needs to know *whether* an error exists; correction must find *where* it is.",
    133: """Segments: 1001, 0001, 1111, 0000

- 1001 + 0001 = 1010
- 1010 + 1111 = 11001, carry wraps: 1001 + 1 = 1010
- 1010 + 0000 = **1010** (sum)

Checksum = complement of 1010 = **0101** (option A)""",
    134: "Need 2^r >= m + r + 1 with m = 17. r = 4: 16 >= 22? No. r = **5**: 32 >= 23. Yes, so **5** parity bits.",
    135: "CRC is based on polynomial division and detects all burst errors shorter than the generator and most others, so it has **higher error detection capability** than VRC and LRC. It cannot correct errors.",
    136: ("1", "Stop-and-Wait sends one frame and waits for its ACK, which is exactly a sliding window of size **1**."),
    137: ("9", "ACKs carry the number of the **next expected** frame. After receiving frame 8 the receiver sends **ACK 9**."),
    138: ("1", "In Go-Back-N (GB9 = sender window 9), the receiver window is always **1**: it accepts only the next in-order frame."),
    139: ("5 bits", """Sent:     0100010001000011
Received: 0101110101000011

Flipped bits are at positions 4, 5 and 8 (counting from the left, 1-based).
Burst length = first to last corrupted bit = 8 - 4 + 1 = **5 bits**."""),
    140: ("100011", "x^5 + x + 1 = 1x^5 + 0x^4 + 0x^3 + 0x^2 + 1x^1 + 1x^0 -> **100011**"),
    141: ("4 bits", """Codeword 100100001 = 9 bits; original data = 6 bits, so remainder (CRC) = 9 - 6 = 3 bits.

Remainder length = key length - 1, so key = 3 + 1 = **4 bits**."""),
    142: ("13", """Count every transmission; every 4th one is lost and that packet is resent.

| Tx # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Packet | 1 | 2 | 3 | 4 (lost) | 4 | 5 | 6 | 7 (lost) | 7 | 8 | 9 | 10 (lost) | 10 |

Total transmissions = **13**"""),
    143: ("1110", """Segments of 4 bits: 0101, 0011, 1000

- 0101 + 0011 = 1000
- 1000 + 1000 = 10000, wrap carry: 0000 + 1 = **0001**

Checksum = complement of 0001 = **1110**"""),
    144: ("Codeword 01010110001; error at position 6", f"""{HAM_NOTE}

**1. Encode 0100110 (m = 7, so r = 4, 11 bits)**

Positions 11..1: d d d r8 d d d r4 d r2 r1. Place data 0 1 0 0 1 1 0 at positions 11, 10, 9, 7, 6, 5, 3:

| Pos | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bit | 0 | 1 | 0 | r8 | 0 | 1 | 1 | r4 | 0 | r2 | r1 |

- r1 (1,3,5,7,9,11) = 0+1+0+0+0 -> **1**
- r2 (2,3,6,7,10,11) = 0+1+0+1+0 -> **0**
- r4 (4,5,6,7) = 1+1+0 -> **0**
- r8 (8,9,10,11) = 0+1+0 -> **1**

Codeword = **0 1 0 1 0 1 1 0 0 0 1 = 01010110001**

**2. Received 01010010001**

| Pos | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bit | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |

- c1 (1,3,5,7,9,11) = 1+0+1+0+0+0 = 2 -> 0
- c2 (2,3,6,7,10,11) = 0+0+0+0+1+0 = 1 -> 1
- c4 (4,5,6,7) = 0+1+0+0 = 1 -> 1
- c8 (8,9,10,11) = 1+0+1+0 = 2 -> 0

c8c4c2c1 = 0110 = **error at position 6** (bit 6 should be 1)."""),
    145: ("10101010", """LRC = XOR of all blocks, column by column (even parity per column):

```
  11100111
  11011101
  00111001
  10101001
  --------
  10101010   <- LRC
```"""),
    146: ("CRC = 01110; No (error)", """Generator x^5 + x^4 + x^2 + 1 = **110101** (6 bits), so append 5 zeros.

**1)** Divide 1010001101 + 00000 by 110101 (mod-2):

{{crc:101000110100000:110101}}
Remainder = **01110**, so transmitted frame = 1010001101**01110**.

**2)** Divide the received word by 110101:

{{crc:101000110101100:110101}}

Remainder **00010**, not zero, so **No**: the codeword has an error (it differs from 101000110101110)."""),
    147: ("11011010", """Segments: 10011001, 11100010, 00100100, 10000100

- 10011001 + 11100010 = 1 01111011 -> wrap: 01111100
- 01111100 + 00100100 = 10100000
- 10100000 + 10000100 = 1 00100100 -> wrap: 00100101

Sum = 00100101, checksum = complement = **11011010** (same worked example as the T1 notes)."""),
    148: ("7.4 ms", "RTT = 2 x Tp = 2 x 3.7 = **7.4 ms**"),
    149: ("4 bits", "2^r >= m + r + 1 with m = 7: r = 3 gives 8 >= 11 (no); r = **4** gives 16 >= 12 (yes)."),
    150: ("Error at bit 7; corrected 10010000101", f"""{HAM_NOTE}

Received 10010100101, positions 11..1:

| Pos | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bit | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 |

- c1 (1,3,5,7,9,11) = 1+1+0+0+0+1 = 3 -> **1**
- c2 (2,3,6,7,10,11) = 0+1+1+0+0+1 = 3 -> **1**
- c4 (4,5,6,7) = 0+0+1+0 = 1 -> **1**
- c8 (8,9,10,11) = 1+0+0+1 = 2 -> **0**

c8c4c2c1 = 0111 = **7**. Flip bit 7 (0 -> 1):
corrected codeword = **10011100101**, data bits (11,10,9,7,6,5,3) = **1001101**."""),
    151: ("2 ESC", "In byte stuffing every ESC in the data is sent as ESC ESC. Receiving 4 ESC means 2 data ESCs, each with one stuffed ESC. The receiver discards the stuffed ones: **2 ESC** discarded (2 kept as data)."),
    152: ("Retransmit the frame after timeout", "If the ACK is lost, the sender's **timer expires and it resends the same frame**. The receiver sees the repeated sequence number, discards the duplicate and re-sends the ACK."),
    153: ("10011101100", """Generator x^3 + 1 = **1001**, append 3 zeros:

{{crc:10011101000:1001}}
Remainder = **100**, transmitted = 10011101**100**"""),
    154: ("No error (remainder 000)", """Divide 100100001 by 1101:

{{crc:100100001:1101}}

The division leaves remainder **000**, so the codeword is **accepted (no error)**. Data = 100100, CRC = 001."""),
    155: ("1 ESC per ESC/flag", "Byte stuffing adds **one ESC before each** ESC or FLAG byte that appears in the data. So a data ESC becomes ESC ESC."),
    156: ("11010110111110", """Generator x^4 + x + 1 = **10011**, append 4 zeros: 1101011011 0000

{{crc:11010110110000:10011}}

Remainder **1110**.

Transmitted = 1101011011**1110** (classic Tanenbaum example)."""),
    157: ("Error (remainder 011)", """Divide 100000001 by 1101 (mod-2):

{{crc:100000001:1101}}

The remainder is **011**, which is non-zero, so the codeword **has an error** and is rejected."""),
    158: ("2^48 (about 2.8 x 10^14)", "A MAC address is 48 bits, so there are **2^48 = 281,474,976,710,656** possible addresses."),
    159: ("1010101", f"""{HAM_NOTE}

Data 1011 at positions 7, 6, 5, 3 (d7=1, d6=0, d5=1, d3=1):

- r1 = d3 ^ d5 ^ d7 = 1 ^ 1 ^ 1 = **1**
- r2 = d3 ^ d6 ^ d7 = 1 ^ 0 ^ 1 = **0**
- r4 = d5 ^ d6 ^ d7 = 1 ^ 0 ^ 1 = **0**

| Pos | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| Bit | d 1 | d 0 | d 1 | r4 0 | d 1 | r2 0 | r1 1 |

Encoded message = **1010101**"""),
    160: ("Error at position 2", f"""{HAM_NOTE}

1010111: pos7=1, pos6=0, pos5=1, pos4=0, pos3=1, pos2=1, pos1=1

- c1 (1,3,5,7) = 1+1+1+1 = 4 -> 0
- c2 (2,3,6,7) = 1+1+0+1 = 3 -> 1
- c4 (4,5,6,7) = 0+1+0+1 = 2 -> 0

c4c2c1 = 010 = **position 2** (a parity bit). Corrected codeword 1010101, data 1011.
(Left-to-right numbering would give position 6.)"""),
    161: ("Error at position 7", f"""{HAM_NOTE}

1101101: pos7=1, pos6=1, pos5=0, pos4=1, pos3=1, pos2=0, pos1=1

- P1 check (1,3,5,7) = 1+1+0+1 = 3 -> **1**
- P2 check (2,3,6,7) = 0+1+1+1 = 3 -> **1**
- P4 check (4,5,6,7) = 1+0+1+1 = 3 -> **1**
- P8 is not used (only 7 bits)

Syndrome = 111 = **error at position 7**. Corrected codeword = 0101101."""),
    162: ("17", """Go-Back-4: window = 4, every 6th **transmission** is lost.

`1 2 3 4 5 [6 lost] 7 8 9 | 6 7 [8 lost] 9 10 | 8 9 10`

- Tx 1-9: frames 1-9 (frame 6 lost at tx 6; 7, 8, 9 already sent are discarded by receiver)
- Timeout for 6: resend 6, 7, 8, 9, 10 (tx 10-14); tx 12 (frame 8) is the next 6th, lost
- Resend 8, 9, 10 (tx 15-17)

Total = **17 transmissions** (same as the worked example in the T1 notes)."""),
}
