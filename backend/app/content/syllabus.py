"""Official LJU syllabus (Sem V, batch 2024) and the T1/T2 marks distribution.

Source: SEM_V_CN_SYLLABUS_LJU_BATCH 2024.pdf and CN_Marks Distribution.pdf.
Each topic lists where it is covered: notes sections ("u5:IPv6") and practice
questions (ids). Extra syllabus questions use ids 1000+.
"""

TESTS = {
    "T1": {"units": [1, 2, 3, 4], "share": 45.0, "marks": 50, "duration_min": 135,
           "pattern": {"mcq": 20, "theory": 5, "numerical": 25}},
    "T2": {"units": [5, 6, 7, 8, 9, 10], "share": 55.0, "marks": 50, "duration_min": 150,
           "pattern": {"mcq": 20, "theory": 5, "numerical": 25}},
}

# Theory 80% (MCQ 40, descriptive 10, numerical 50 of 100) + practical 20% (projects).
EVALUATION = [
    ["MCQ", "32%", 40], ["Theory descriptive", "8%", 10], ["Formulas and derivation", "0%", 0],
    ["Numerical", "40%", 50], ["Individual project (practical)", "10%", 50], ["Group project (practical)", "10%", 50],
]

UNITS = {
    1: {"weight": 12.5, "hours": 5, "test": "T1", "topics": [
        ("1.1", "Introduction to Networks and Layered Architecture", [1, 2, 3, 13, 56, 66]),
        ("1.2", "Networks and its types, Network Devices", [4, 5, 8, 12, 15, 18, 24, 55, 59, 60]),
        ("1.3", "OSI and TCP/IP Reference Model", [6, 7, 10, 11, 14, 22, 57, 58, 61, 62, 63, 64, 65]),
        ("1.4", "Understanding of Delay, Loss, and Throughput in Networks", [16, 17, 27, 28, 29, 30, 31, 32, 33, 37, 38, 40, 41]),
    ]},
    2: {"weight": 10.0, "hours": 4, "test": "T1", "topics": [
        ("2.1", "Data Communications Concepts", [67, 68, 69, 70, 71, 95, 1201, 1202]),
        ("2.2", "Transmission Media and Network Topology", [72, 73, 74, 78, 79, 84, 87, 101, 108, 109, 111, 112, 113]),
    ]},
    3: {"weight": 15.0, "hours": 6, "test": "T1", "topics": [
        ("3.1", "Design issues of Data Link Layer, Data Link Layer Services", [117, 119, 120, 125, 126, 151, 155]),
        ("3.2", "Error Correction and Detection Techniques", [118, 121, 124, 133, 139, 143, 144, 145, 146, 147, 150, 153, 156]),
        ("3.3", "Reliable Transmission and ARQ: Stop-and-Wait, Go-back-N, Selective Repeat", [123, 127, 136, 137, 138, 142, 148, 152, 162]),
    ]},
    4: {"weight": 7.5, "hours": 3, "test": "T1", "topics": [
        ("4.1", "Channel Allocation Problems", [1401, 1402, 1403]),
        ("4.2", "Multiple Access Protocols: Random Access, Collision Free", [165, 167, 176, 177, 181, 182, 198, 202, 210, 1404, 1405, 1406]),
        ("4.3", "Ethernet", [185, 186, 188, 190, 192, 197]),
    ]},
    5: {"weight": 12.5, "hours": 5, "test": "T2", "topics": [
        ("5.1", "Design issues of Network Layer, Packet Switching and Circuit Switching", [214, 215, 217, 218, 220, 229, 246]),
        ("5.2", "IPv4 and IPv6 Addressing and Headers, Classful, Classless, IPv4 to IPv6 transition",
         [221, 223, 224, 227, 232, 233, 235, 249, 250, 252, 253, 255, 1501, 1502, 1503, 1504, 1505]),
        ("5.3", "Fragmentation, Network Address Translation (NAT)", [225, 239, 240, 242, 244, 245, 261, 1506, 1507, 1508]),
    ]},
    6: {"weight": 12.5, "hours": 5, "test": "T2", "topics": [
        ("6.1", "Routing Algorithms: Shortest Path Routing, Flooding", [263, 264, 270, 275, 277, 281, 287, 295, 1601, 1602]),
        ("6.2", "Distance Vector Routing", [262, 274, 279, 280, 282, 285, 286, 288, 291]),
        ("6.3", "Link State Routing", [273, 276, 283, 293]),
    ]},
    7: {"weight": 7.5, "hours": 3, "test": "T2", "topics": [
        ("7.1", "Introduction and Transport Layer Services", [296, 297, 299, 305, 319, 322]),
        ("7.2", "Multiplexing and Demultiplexing", [298, 301, 309, 311, 312, 313, 316, 317]),
        ("7.3", "Connection Oriented versus Connectionless Services", [304, 314, 321, 357]),
    ]},
    8: {"weight": 10.0, "hours": 4, "test": "T2", "topics": [
        ("8.1", "Connectionless Transport Protocol (UDP)", [336, 337, 339, 340, 355, 356, 363, 371, 372]),
        ("8.2", "Connection Oriented Transport Protocol (TCP)", [331, 333, 334, 342, 343, 344, 349, 360, 361, 375, 377]),
        ("8.3", "Congestion Control", [323, 324, 352, 353, 354, 359, 365, 370, 1801, 1802, 1803, 1804]),
    ]},
    9: {"weight": 7.5, "hours": 2, "test": "T2", "topics": [
        ("9.1", "Principles of Computer Applications", [381, 382, 383, 384, 385, 392, 397, 1901, 1902]),
        ("9.2", "Web and HTTP, DNS, SMTP", [386, 387, 389, 390, 391, 398, 400, 401, 402, 403, 404, 406]),
    ]},
    10: {"weight": 5.0, "hours": 3, "test": "T2", "topics": [
        ("10.1", "Network Design using Packet Tracer", [2001, 2002, 2003, 2004]),
        ("10.2", "Network Monitoring using Wireshark", [410, 412, 413, 414, 415, 416, 417, 418, 419, 420]),
    ]},
}

COURSE_OUTCOMES = [
    ("CO1", "Basic concepts of data communications, networking, topology types, transmission media and internetworking."),
    ("CO2", "Error detection and recovery of data and link layer terminology."),
    ("CO3", "IPv4 and IPv6 addressing and their relation to connecting computers and media; routing algorithms."),
    ("CO4", "UDP and TCP for reliable data transfer, flow and congestion control; basic application layer protocols."),
]

BOOKS = [
    "Andrew S. Tanenbaum, Computer Networks, PHI",
    "Behrouz Forouzan, Data Communications and Networking, TMH",
    "Behrouz Forouzan, TCP/IP Protocol Suite, TMH",
    "William Stallings, Data and Computer Communications, Pearson",
    "Jim Kurose, Computer Networking: A Top-Down Approach, Pearson",
]
