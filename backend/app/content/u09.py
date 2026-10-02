"""Unit 9 - Application Layer (PB Q379-Q409)."""

TITLE = "Application Layer"
SOURCE = "Practice book Unit 9 (not covered in T1 notes; standard Forouzan / Kurose content)"

NOTES = {
    "summary": "Client-server and P2P paradigms, what application protocols define, and the big four: HTTP, SMTP (email), DNS, FTP/Telnet.",
    "sections": [
        {"h": "Basics", "points": [
            "Address used = **URL / domain name**; unit of data = **message**.",
            "Paradigms: **client-server** and **peer-to-peer** (and hybrids).",
            "An application protocol defines **message types, syntax, semantics, and rules for when/how processes send and respond**.",
            "Developer chooses the **transport protocol and a few parameters** (e.g. buffer sizes), nothing deeper.",
            "**Elastic** apps (email, file transfer, web) use whatever bandwidth is available. **Time-sensitive** apps: internet telephony, interactive games, live video.",
        ]},
        {"h": "Protocols and ports", "points": [
            "**HTTP** 80 (HTTPS 443): web, request-response, stateless, over TCP.",
            "**SMTP** 25: push mail between servers. **POP3** 110 / **IMAP** 143: user pulls mail.",
            "**FTP** 20 (data) / 21 (control): two TCP connections. **Telnet** 23 / SSH 22: remote login (keystrokes to remote host).",
            "**DNS** 53 (UDP; TCP for zone transfer): domain name -> IP address. **DHCP** 67/68, **SNMP** 161.",
            "HTTP and FTP can both open **multiple TCP connections** between the same client and server.",
        ]},
        {"h": "Email", "points": [
            "**UA** (user agent: Outlook, Gmail web) composes/reads mail. **MTA** (mail transfer agent) moves mail between servers with SMTP. **MAA** (POP3/IMAP) retrieves it.",
            "Flow: sender UA -> SMTP -> sender's mail server (MTA) -> SMTP -> receiver's mail server (mailbox) -> POP3/IMAP -> receiver UA.",
        ]},
        {"h": "Web documents", "points": [
            "**Static**: fixed file. **Dynamic**: created by the server per request (CGI, PHP). **Active**: program sent to and run on the **client** (Java applet, JavaScript).",
            "HTTP messages: **request** (method GET/POST/HEAD/PUT/DELETE, URL, version, headers, body) and **response** (version, status code 200/301/404/500, headers, body).",
        ]},
    ],
    "formulas": [
        ["HTTP / HTTPS", "TCP 80 / 443"],
        ["SMTP / POP3 / IMAP", "25 / 110 / 143"],
        ["FTP data / control", "20 / 21"],
        ["Telnet / SSH / DNS", "23 / 22 / 53"],
    ],
    "traps": [
        "UDP and TCP are transport protocols, not application protocols.",
        "Active document runs on the client; dynamic document is built on the server.",
        "Email is elastic (not time-sensitive); interactive games are the odd one out.",
    ],
}

NUMERICAL = set()

SOL = {
    379: "Applications identify resources by **URL** (domain names). Port = transport, MAC = data link, IP = network.",
    380: "The application-layer data unit is a **message**.",
    381: "Both **peer-to-peer and client-server** are application architecture paradigms. HTTP is a protocol.",
    382: "The developer can pick **both the transport protocol and the maximum buffer size** (and a few other socket parameters).",
    383: "The key gives **end to end**: the application layer offers services between end systems (the two hosts), without involving routers in between.",
    384: "Email can tolerate delay and uses whatever bandwidth is available: an **elastic application**. It is not loss-tolerant (mail must arrive intact).",
    385: "**Internet telephony** is time-sensitive: late voice packets are useless.",
    386: "Email is sent with **SMTP**.",
    387: "The **Domain Name System** translates domain/host names to IP addresses.",
    388: "**Telnet** lets a user log in to a remote host and passes keystrokes to it.",
    389: "**HTTP and FTP** can both use multiple TCP connections between the same client and server (HTTP parallel connections; FTP separate control and data connections).",
    390: "Mail is moved between machines with **SMTP**.",
    391: "A program sent by the server and executed at the client is an **active** document (e.g. Java applet, JavaScript).",
    392: "File transfer, file download and email are elastic, loss-intolerant applications. **Interactive games** are time-sensitive, so they are the odd one out.",
    393: "Same as Q387: the **domain name system**.",
    394: "The key marks **C (rules for when and how processes send and respond)**. In reality an application-layer protocol defines all three (message types, syntax/semantics, and timing rules); if your exam has 'all of the mentioned', that is the complete answer.",
    395: "**UDP** is a transport protocol. HTTP, SMTP, HTTPS are application protocols.",
    396: "**TCP** is a transport protocol, not an application protocol.",
    397: ("Network access for users: services, protocols, resource sharing", """- Provide the **user interface** to the network (browsers, mail clients).
- Provide services: **web (HTTP), email (SMTP/POP/IMAP), file transfer (FTP), remote login (Telnet/SSH), name resolution (DNS)**.
- Define message formats and rules for each service.
- **Resource sharing** and remote file access.
- Directory services and network management (SNMP).
- Identifying communication partners and checking resource availability."""),
    398: ("Compose (UA) -> SMTP to server -> SMTP between MTAs -> mailbox -> POP3/IMAP -> read", """1. Sender composes mail in a **user agent** (UA).
2. UA hands the mail to the sender's **mail server** using **SMTP**; it waits in the outgoing queue.
3. The sender's **MTA** opens a TCP connection (port 25) to the receiver's mail server and transfers the mail with SMTP (HELO, MAIL FROM, RCPT TO, DATA, QUIT).
4. The receiving server stores the mail in the recipient's **mailbox**.
5. The recipient's UA retrieves it with **POP3 or IMAP** (message access agent) and displays it."""),
    399: ("HTTP, FTP, SMTP, POP3, IMAP, DNS, Telnet, SSH, DHCP, SNMP + TCP, UDP, IP, ICMP, ARP", """| Layer | Protocols |
|---|---|
| Application | HTTP/HTTPS, FTP, SMTP, POP3, IMAP, DNS, Telnet, SSH, DHCP, SNMP, TFTP |
| Transport | TCP, UDP, SCTP |
| Internet | IP (IPv4/IPv6), ICMP, IGMP, ARP, RARP |
| Network access | Ethernet, Wi-Fi (802.11), PPP |"""),
    400: ("HyperText Transfer Protocol, TCP port 80 (HTTPS 443)", """**HTTP** (HyperText Transfer Protocol) transfers web pages and other resources between browsers (clients) and web servers.

- Uses **TCP port 80** (HTTPS = HTTP over TLS on **port 443**).
- Request-response: client sends a request (GET /index.html HTTP/1.1), server sends a response (200 OK + content).
- **Stateless** (cookies add state); persistent and non-persistent connections."""),
    401: ("Push mail between servers over TCP 25", """- **Simple Mail Transfer Protocol**, a **push** protocol over **TCP port 25**.
- Transfers mail from the sender's UA to its mail server and **between mail servers** (MTA to MTA).
- Three phases: **connection establishment** (220, HELO/EHLO), **mail transfer** (MAIL FROM, RCPT TO, DATA, message, '.'), **connection termination** (QUIT, 221).
- Uses text commands and numeric reply codes (250 OK, 354 start mail input, 550 mailbox unavailable).
- Handles only 7-bit ASCII; **MIME** extends it for attachments, images, other languages.
- Does not retrieve mail: POP3 / IMAP do that."""),
    402: ("UA = user's mail program; MTA = server software that transfers mail", """| User Agent (UA) | Mail Transfer Agent (MTA) |
|---|---|
| Program the user interacts with (Outlook, Thunderbird, Gmail web) | Server software that sends/relays mail (Sendmail, Postfix) |
| Composes, reads, replies, forwards, organizes mail | Transfers mail between servers using SMTP |
| Runs on the user's machine | Runs on mail servers |
| Uses SMTP to send to its server, POP3/IMAP to read | Uses SMTP client and server |"""),
    403: ("Mapping names to IP addresses", """DNS is the Internet's distributed directory:

- Translates **domain names to IP addresses** (and reverse lookups IP -> name).
- **Hierarchical, distributed database**: root servers, TLD servers (.com, .in), authoritative servers.
- Supports **host aliasing** (CNAME), **mail server aliasing** (MX records), and **load distribution** (several IPs per name).
- Resolution can be **recursive** or **iterative**; answers are **cached** to reduce traffic.
- Uses **UDP port 53** for queries (TCP for zone transfers)."""),
    404: ("Stateless, connectionless request-response, media independent, uses TCP", """1. **Connectionless (request-response)**: client sends a request, server responds; each request is independent (with persistent connections the TCP connection may be reused).
2. **Stateless**: the server keeps no information about previous requests (cookies/sessions add state).
3. **Media independent**: any data type can be sent, identified by the **Content-Type** (MIME type).
4. **Uses TCP** (reliable) on port 80 and works with URLs to locate resources.

(Also: text-based, extensible headers.)"""),
    405: ("Same as Q397", """- Provide network services directly to user applications: web, email, file transfer, remote login, DNS.
- Define message types, formats, syntax, semantics and timing rules for each service.
- Identify communication partners and check resource availability.
- Synchronize communication and support authentication / privacy.
- Provide network transparency: users need not know how data is moved."""),
    406: ("Request and response", """**Request message**
- Request line: **method** (GET, POST, HEAD, PUT, DELETE, OPTIONS), URL, HTTP version
- Header lines (Host, User-Agent, Accept, Cookie, ...)
- Blank line and optional body (form data for POST)

**Response message**
- Status line: HTTP version, **status code**, phrase (200 OK, 301 Moved Permanently, 404 Not Found, 500 Internal Server Error)
- Header lines (Content-Type, Content-Length, Set-Cookie, ...)
- Blank line and body (the HTML page, image, ...)"""),
    407: ("Same as Q401", """- **SMTP** = Simple Mail Transfer Protocol, TCP port 25, a push protocol.
- Sends mail from UA to mail server and **between mail servers**.
- Phases: connection setup (HELO), mail transfer (MAIL FROM, RCPT TO, DATA), termination (QUIT).
- Text commands + numeric replies; MIME for non-ASCII content.
- Retrieval is done by POP3/IMAP, not SMTP."""),
    408: ("UA composes, SMTP sends, POP3/IMAP retrieves, DNS finds the server", """1. **User agent** provides the interface to compose the mail and attach files (MIME encodes attachments).
2. **DNS** (MX record) finds the recipient's mail server.
3. **SMTP** pushes the mail from the sender's UA to its server and on to the recipient's server.
4. The mail waits in the recipient's mailbox.
5. **POP3 / IMAP** lets the recipient's UA pull and display it.

All of these are application-layer protocols; TCP below them gives reliable delivery."""),
    409: ("Browsing, email, file transfer, DNS lookup, remote login, streaming", """1. **Web browsing**: browser uses HTTP/HTTPS to fetch a page.
2. **Email**: SMTP to send, POP3/IMAP to read.
3. **File transfer**: FTP / SFTP to upload a project to a server.
4. **Name resolution**: DNS turns www.google.com into an IP address.
5. **Remote login**: Telnet / SSH to administer a server.
6. Also: **video streaming** (HTTP-based DASH), **network management** (SNMP), **DHCP** assigning addresses."""),
}
