"""Computer Networks part 2: IP & subnetting, routing, transport, application layer & security."""
import heapq
import ipaddress
import math

from learn import Ex, lesson

S = "CN"


def fragments(total, mtu, header=20):
    payload = total - header
    per = (mtu - header) // 8 * 8
    out, off = [], 0
    while payload > 0:
        n = min(per, payload)
        out.append((n, off // 8, 1 if payload > n else 0))
        payload -= n
        off += n
    return out


def dijkstra(edges, src):
    adj = {}
    for a, b, w in edges:
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))
    d = {n: float("inf") for n in adj}
    d[src] = 0
    h = [(0, src)]
    while h:
        du, u = heapq.heappop(h)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(h, (d[v], v))
    return d


def tcp(rounds, ss, ev):
    cwnd, out = 1, []
    for r in range(1, rounds + 1):
        out.append(cwnd)
        e = ev.get(r)
        if e == "timeout":
            ss = max(2, cwnd // 2)
            cwnd = 1
        elif e == "dup":
            ss = max(2, cwnd // 2)
            cwnd = ss
        elif cwnd < ss:
            cwnd = min(cwnd * 2, ss)
        else:
            cwnd += 1
    return out


def lpm(table, addr):
    a = ipaddress.ip_address(addr)
    best = max((ipaddress.ip_network(p) for p, _ in table if a in ipaddress.ip_network(p)), key=lambda n: n.prefixlen)
    return dict(table)[str(best)]


# ======================================================================================================
lesson(subject=S, chapter="Network & Transport Layers", ch_no=2, no=1, slug="cn-ip-subnetting", title="IP Addressing, Subnetting, CIDR & Fragmentation",
       topic="IP Addressing & Subnetting", minutes=26, weight=7, widget="subnet",
       widget_hint="Enter an IP address and prefix to get the network, broadcast, host range and mask; then ask for a number of subnets to see the new prefix.",
       key="An IPv4 address is 32 bits split into network and host parts by the subnet mask. CIDR notation a.b.c.d/p replaces the old classes; subnetting borrows host bits, supernetting aggregates, routers use longest-prefix match, and fragmentation splits datagrams larger than the link MTU.",
       analogy=("🏘️", "Street address and house number", "The network part of an address is the street; the host part is the house number. Subnetting subdivides a street into smaller lanes, each with fewer houses; routers only need to know which street, not every house."),
       sections=[
           dict(h="Classful and classless addressing", md="""| Class | First bits | Range of first octet | Default mask | Hosts/net |
|---|---|---|---|---|
| A | 0 | 0–127 | /8 | 2²⁴ − 2 |
| B | 10 | 128–191 | /16 | 2¹⁶ − 2 |
| C | 110 | 192–223 | /24 | 254 |
| D | 1110 | 224–239 | – | multicast |
| E | 1111 | 240–255 | – | reserved |

**CIDR** a.b.c.d/p: p network bits, 32 − p host bits. Usable hosts = **2^(32−p) − 2** (network and broadcast addresses excluded; /31 point-to-point uses both). **Network address** = IP AND mask; **broadcast** = network with all host bits 1. Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16; loopback 127.0.0.0/8; link-local 169.254.0.0/16."""),
           dict(h="Subnetting, VLSM and supernetting", md="""**Subnetting:** borrow b host bits to create 2ᵇ subnets, each with 2^(32−p−b) − 2 hosts. To get at least n subnets borrow ⌈log₂ n⌉ bits; to have at least h hosts leave ⌈log₂(h + 2)⌉ host bits.

**VLSM (variable-length subnet masks):** allocate the largest subnets first, each aligned on its size boundary.

**Supernetting / route aggregation:** four contiguous /24 blocks 200.1.0.0 … 200.1.3.0 aggregate to 200.1.0.0/22 if the first is aligned on a 4-block boundary. A router's forwarding uses **longest-prefix match**: among the table entries matching the destination, take the one with the longest prefix (default route 0.0.0.0/0 matches everything)."""),
           dict(h="The IPv4 header and fragmentation", md="""IPv4 header: 20 bytes minimum (up to 60); fields: version, IHL (in 4-byte words), total length (≤ 65,535), identification, flags (DF, MF), **fragment offset (in 8-byte units)**, TTL, protocol, checksum (header only), source, destination.

**Fragmentation:** if a datagram exceeds the link **MTU**, each fragment's data (except the last) is a multiple of 8 bytes; the MF flag is 1 on all but the last fragment; offset = data bytes before it / 8. Reassembly happens only at the destination. Total length of a fragment = data + 20.

Example: a 4000-byte datagram (20-byte header, 3980 bytes of data) over MTU 1500: per fragment 1480 data bytes ⇒ fragments of 1480, 1480 and 1020 data bytes with offsets 0, 185, 370."""),
           dict(h="Helper protocols and IPv6", md="""**ARP** maps IP to MAC (broadcast request); **RARP/DHCP** assign addresses (DHCP: Discover, Offer, Request, Ack over UDP 67/68); **ICMP** reports errors (echo/ping, destination unreachable, time exceeded used by traceroute); **NAT** maps private to public address/port pairs. **IPv6:** 128-bit addresses, 40-byte fixed header, no fragmentation by routers, no header checksum, ::1 loopback, tunnelling for transition."""),
       ],
       examples=[
           Ex("Subnet details", "For the host 192.168.10.77/26, find the network address, broadcast address and number of usable hosts.",
              ["/26 leaves 6 host bits: block size 64; 77 lies in the block starting at 64.", "Network 192.168.10.64, broadcast 192.168.10.127, usable hosts 2⁶ − 2 = **62**."],
              "Network **192.168.10.64**, broadcast **192.168.10.127**, **62** hosts.", verify=lambda: (lambda n: "Network %s, broadcast %s, %d hosts" % (n.network_address, n.broadcast_address, n.num_addresses - 2))(ipaddress.ip_network("192.168.10.77/26", strict=False))),
           Ex("Fragmentation", "A datagram of 4000 bytes (20-byte header) is sent over a link with MTU 1500. How many fragments, and what are their offsets?",
              ["Data = 3980 bytes; each fragment carries at most 1480 bytes (multiple of 8).", "Fragments: 1480, 1480, 1020 bytes with offsets 0, 185, 370 — **3** fragments."],
              "**3** fragments with offsets 0, 185, 370.", verify=lambda: "%d fragments with offsets %s" % (len(fragments(4000, 1500)), ", ".join(str(f[1]) for f in fragments(4000, 1500)))),
           Ex("Longest-prefix match", "A router has routes 10.0.0.0/8 → A, 10.1.0.0/16 → B, 10.1.2.0/24 → C, 0.0.0.0/0 → D. Where does it send a packet for 10.1.2.77, and for 10.9.9.9?",
              ["10.1.2.77 matches /8, /16, /24 and /0; the longest is /24 ⇒ C.", "10.9.9.9 matches only /8 and /0 ⇒ A."],
              "10.1.2.77 → **C**; 10.9.9.9 → **A**.", verify=lambda: "10.1.2.77 → %s; 10.9.9.9 → %s" % tuple(lpm([("10.0.0.0/8", "A"), ("10.1.0.0/16", "B"), ("10.1.2.0/24", "C"), ("0.0.0.0/0", "D")], x) for x in ("10.1.2.77", "10.9.9.9"))),
           Ex("Aggregation", "Four consecutive /24 networks starting at 200.1.0.0 are summarised. What is the aggregate?",
              ["Four /24s span 4 × 256 = 1024 addresses = 2¹⁰ ⇒ prefix 32 − 10 = /22.", "Aggregate: **200.1.0.0/22**."],
              "**200.1.0.0/22**", verify=lambda: str(ipaddress.collapse_addresses([ipaddress.ip_network("200.1.%d.0/24" % i) for i in range(4)]).__next__())),
       ],
       traps=[("Usable hosts", "Subtract 2 for the network and broadcast addresses."),
              ("Fragment offsets", "Offsets are in 8-byte units; data per fragment is a multiple of 8."),
              ("Longest prefix wins", "Not the first match and not the lowest metric."),
              ("Private addresses", "172.16.0.0/12 spans 172.16–172.31 only.")],
       quick=[("A /27 network has how many usable hosts?", ["30", "32", "62", "14"], 0, "2⁵ − 2."),
              ("The IPv4 fragment offset is measured in", ["bits", "bytes", "8-byte units", "words of 4 bytes"], 2, "8-byte units."),
              ("A router chooses among matching routes by", ["shortest prefix", "longest prefix", "first listed", "random"], 1, "Longest-prefix match."),
              ("Which protocol maps IP addresses to MAC addresses?", ["DHCP", "ARP", "ICMP", "NAT"], 1, "ARP.")],
       summary=["Classes A/B/C: /8, /16, /24; CIDR /p gives 2^(32−p) − 2 hosts.", "Network = IP AND mask; broadcast = host bits all 1.", "Subnets: borrow ⌈log₂ n⌉ bits; VLSM largest first; aggregate contiguous blocks.",
                "Longest-prefix match forwarding; default route /0.", "Fragment data multiples of 8; offset = bytes/8; MF flag; reassembly at the destination.", "ARP, DHCP, ICMP, NAT; IPv6 = 128 bits, fixed 40-byte header."])


# ======================================================================================================
lesson(subject=S, chapter="Network & Transport Layers", ch_no=2, no=2, slug="cn-routing", title="Routing: Distance Vector, Link State & Internet Routing",
       topic="Routing", minutes=22, weight=5, widget="none",
       key="Routers build forwarding tables with routing algorithms: distance-vector (Bellman–Ford: each router tells neighbours its distances), link-state (flood the topology, run Dijkstra) and path-vector (BGP). Know their convergence behaviour, count-to-infinity, and the major protocols RIP, OSPF and BGP.",
       analogy=("🧭", "Asking for directions", "Distance vector is asking each neighbour ‘how far is town X from you?’ and adding the road to them. Link state is everyone broadcasting their local map until all have the full map, then each plots their own route. The first is cheap but can mislead (count-to-infinity); the second is precise but heavier."),
       sections=[
           dict(h="Distance-vector routing", md="""Each router keeps a table of (destination, cost, next hop) and periodically sends its vector to neighbours. On receiving a neighbour's vector, apply **Bellman–Ford**: d(x, y) = min over neighbours v of [ c(x, v) + d(v, y) ].

- Converges in at most (diameter) iterations on a static network; good news travels fast, **bad news slowly** (**count-to-infinity**).
- Fixes: define infinity as a small number (RIP: 16), **split horizon** (do not advertise a route back to where you learned it), **poison reverse**, hold-down timers.
- **RIP:** hop-count metric, maximum 15 hops, updates every 30 s, UDP port 520."""),
           dict(h="Link-state routing and Dijkstra", md="""Each router floods **link-state packets** (its neighbours and link costs) to everyone, builds the identical full graph and runs **Dijkstra**: repeatedly add the unvisited node with the smallest tentative distance, relax its edges. Complexity O(E log V) (or O(V²)).

- **OSPF** uses link state (costs; hierarchical areas; multicast 224.0.0.5; IP protocol 89).
- Fast convergence, loop-free at steady state, more memory/bandwidth than DV.
- Dijkstra needs non-negative weights; Bellman–Ford handles negative edges (but not negative cycles).""",
                formulas=[("d(x,y) = min_v [ c(x,v) + d(v,y) ]", "Bellman–Ford / distance vector")]),
           dict(h="Inter-domain routing and other topics", md="""The Internet is divided into **autonomous systems (AS)**. **Intra-AS** protocols: RIP, OSPF. **Inter-AS:** **BGP**, a **path-vector** protocol over TCP port 179 that advertises full AS paths (loop prevention) and applies *policy* (not just shortest path). eBGP between ASes, iBGP within.

Other routing ideas: **broadcast/multicast** (reverse path forwarding, spanning trees, IGMP), **hierarchical routing**, **mobile IP**, **MPLS** (label switching). Static, default and dynamic routes; metric = hop count, delay, bandwidth or composite."""),
           dict(h="Congestion and QoS (brief)", md="""**Token bucket** shapes traffic: a bucket of capacity b tokens refilled at rate r; sending a packet consumes tokens; the maximum burst is b and the long-run rate r; a burst can go out at the full line rate C for at most b / (C − r) seconds (when C > r), after which the sender is held to rate r. The **leaky bucket** outputs at a constant rate regardless of burstiness. Example: b = 1 MB, r = 2 MB/s, C = 10 MB/s gives a maximum burst time of 1 / (10 − 2) = 0.125 s."""),
       ],
       examples=[
           Ex("Dijkstra", "Weighted undirected graph: A–B 2, A–C 5, B–C 1, B–D 4, C–D 2, C–E 6, D–E 1. What is the shortest distance from A to E?",
              ["A→B = 2, then B→C = 1 (total 3), C→D = 2 (total 5), D→E = 1 (total 6).", "Alternative A→C→E = 11. Shortest = **6** (path A-B-C-D-E)."],
              "**6**", verify=lambda: str(dijkstra([("A", "B", 2), ("A", "C", 5), ("B", "C", 1), ("B", "D", 4), ("C", "D", 2), ("C", "E", 6), ("D", "E", 1)], "A")["E"])),
           Ex("Distance-vector update", "Router X has neighbours Y (link cost 2) and Z (link cost 7). Y advertises distance 5 to destination T, Z advertises 1. What is X's new cost to T and the next hop?",
              ["Via Y: 2 + 5 = 7. Via Z: 7 + 1 = 8.", "Minimum is 7 through **Y**."],
              "Cost **7**, next hop **Y**.", verify=lambda: "Cost %d, next hop %s" % min((2 + 5, "Y"), (7 + 1, "Z"))),
           Ex("RIP limit", "A RIP network has a path of 16 hops between two routers. Is the destination reachable?",
              ["RIP uses 16 as ‘infinity’ to stop count-to-infinity from going on forever.", "So a route of 16 hops is unreachable; the longest usable path is 15 hops."],
              "**No** (16 = infinity).", verify=lambda: "No" if 16 >= 16 else "Yes"),
       ],
       traps=[("DV vs LS", "DV exchanges tables with neighbours only; LS floods link states to everyone."),
              ("Count-to-infinity", "Split horizon does not cure it in all topologies."),
              ("BGP is path-vector", "It runs over TCP and is policy-driven."),
              ("Dijkstra weights", "Negative edges break Dijkstra.")],
       quick=[("OSPF is an example of", ["distance vector", "link state", "path vector", "static routing"], 1, "Link state."),
              ("RIP's maximum hop count is", ["15", "16", "30", "255"], 0, "16 means unreachable."),
              ("BGP runs over", ["UDP", "TCP", "ICMP", "raw IP"], 1, "TCP port 179."),
              ("The count-to-infinity problem affects", ["link-state", "distance-vector", "ARP", "DNS"], 1, "Bad news travels slowly.")],
       summary=["DV: Bellman–Ford, neighbours only, RIP (hop count ≤ 15, UDP 520).", "Count-to-infinity; split horizon, poison reverse, small infinity.", "LS: flood topology + Dijkstra; OSPF with areas.",
                "BGP: path-vector, policy, TCP 179; eBGP/iBGP.", "Dijkstra O(E log V), needs non-negative weights.", "Token bucket: burst b, rate r."])


# ======================================================================================================
lesson(subject=S, chapter="Network & Transport Layers", ch_no=2, no=3, slug="cn-transport-tcp", title="Transport Layer: UDP, TCP, Flow & Congestion Control",
       topic="Transport Layer (TCP/UDP)", minutes=26, weight=7, widget="tcp",
       widget_hint="Set the initial slow-start threshold and add timeout or triple-duplicate-ACK events at chosen rounds; the chart shows slow start, congestion avoidance and the reaction to loss.",
       key="UDP is a thin connectionless service; TCP provides reliable, ordered byte streams with a three-way handshake, cumulative ACKs, a receiver-advertised window for flow control and slow start / congestion avoidance / fast retransmit for congestion control.",
       analogy=("🚰", "Filling a pipe carefully", "TCP opens the tap slowly (slow start doubles the flow each round), then cautiously adds a little at a time (congestion avoidance), and when the pipe bursts (loss) it cuts the flow, remembers half the level as the safe threshold, and starts again."),
       sections=[
           dict(h="UDP and TCP basics", md="""**UDP:** 8-byte header (source port, destination port, length, checksum); connectionless, no ordering or retransmission; used for DNS, DHCP, streaming. **TCP:** 20-byte minimum header (ports, 32-bit sequence number, 32-bit ACK number, header length, flags URG/ACK/PSH/RST/SYN/FIN, 16-bit window, checksum); connection-oriented, byte-stream, full duplex.

**Connection setup (three-way handshake):** SYN (seq = x) → SYN+ACK (seq = y, ack = x + 1) → ACK (ack = y + 1). **Teardown:** FIN, ACK, FIN, ACK (four steps; half-close possible). SYN consumes one sequence number; a segment carrying n data bytes starting at sequence s is acknowledged by ack = s + n (**cumulative**, next expected byte). Ports: 16 bits; well-known ports 0–1023 (HTTP 80, HTTPS 443, DNS 53, SMTP 25, FTP 21/20)."""),
           dict(h="Flow control and reliability", md="""**Flow control:** the receiver advertises a window (rwnd); the sender never has more than min(cwnd, rwnd) bytes unacknowledged. The window field is 16 bits (max 65,535 bytes; larger with the window-scaling option). **Throughput** ≤ window / RTT.

**Reliability:** retransmission on timeout (RTO from smoothed RTT: SRTT = (1−α)·SRTT + α·RTT, RTO = SRTT + 4·RTTVAR), **fast retransmit** after three duplicate ACKs, and **Karn's algorithm** (do not sample RTT for retransmitted segments). The sequence-number space (32 bits) must not wrap within the maximum segment lifetime: wrap time = 2³² bytes / rate (at 1 Gbps ≈ 34 s).""",
                formulas=[("throughput ≤ window / RTT", "window-limited TCP")]),
           dict(h="Congestion control", md="""State variables: **cwnd** (congestion window, in MSS) and **ssthresh**.

- **Slow start:** cwnd starts at 1 MSS and **doubles every RTT** (+1 MSS per ACK) until cwnd ≥ ssthresh.
- **Congestion avoidance (AIMD):** cwnd increases by **1 MSS per RTT**.
- **Timeout:** ssthresh = cwnd/2, cwnd = 1 MSS, back to slow start.
- **3 duplicate ACKs (fast retransmit/recovery, Reno):** ssthresh = cwnd/2, cwnd = ssthresh (+3), continue in congestion avoidance. **Tahoe** treats it like a timeout.
- The sending rate ≈ cwnd / RTT. Average throughput of AIMD ≈ 0.75 × W_max / RTT.""",
                call=[("trap", "Round-by-round growth", "cwnd after k rounds of slow start from 1 is 2ᵏ⁻¹ at the start of round k (cwnd values 1, 2, 4, 8…). The tool above uses exactly this model.")]),
           dict(h="Sockets and ports", md="""A **socket** is identified by (IP, port); a TCP connection by the 4-tuple (source IP, source port, destination IP, destination port). TCP states: LISTEN, SYN-SENT, SYN-RCVD, ESTABLISHED, FIN-WAIT-1/2, CLOSE-WAIT, LAST-ACK, TIME-WAIT (2·MSL wait). **SYN flood** attacks exploit the half-open state."""),
       ],
       examples=[
           Ex("Sequence and ACK numbers", "A TCP sender starts with sequence number 1000 (ISN, after the handshake) and sends three segments of 500 bytes each. What is the ACK number after all three are received?",
              ["Segments carry bytes 1000–1499, 1500–1999, 2000–2499.", "The cumulative ACK is the next expected byte: **2500**."],
              "**2500**", verify=lambda: str(1000 + 3 * 500)),
           Ex("Window-limited throughput", "A TCP connection has a 64 KB window and an RTT of 100 ms. What is the maximum throughput?",
              ["Throughput = W / RTT = 65,536 × 8 bits / 0.1 s.", "= 5,242,880 bit/s ≈ **5.24 Mbps**."],
              "≈ **5.24 Mbps**", verify=lambda: "%.2f Mbps" % (65536 * 8 / 0.1 / 1e6)),
           Ex("Congestion window evolution", "ssthresh = 16 initially, cwnd starts at 1 and a timeout occurs at the end of round 11. List cwnd at the start of rounds 1–14.",
              ["Slow start: 1, 2, 4, 8, 16 (rounds 1–5); then congestion avoidance +1 per round: 17, 18, 19, 20, 21, 22 (rounds 6–11).", "At the timeout in round 11: ssthresh = 22/2 = 11, cwnd = 1. Round 12: 1, round 13: 2, round 14: 4."],
              "1, 2, 4, 8, 16, 17, 18, 19, 20, 21, 22, 1, 2, 4", verify=lambda: ", ".join(str(x) for x in tcp(14, 16, {11: "timeout"}))),
           Ex("Sequence number wrap-around", "How long does it take a 1 Gbps sender to wrap the 32-bit sequence space?",
              ["2³² bytes = 4.295 GB ⇒ 3.436 × 10¹⁰ bits at 10⁹ bit/s.", "≈ **34.4 s**."],
              "≈ **34.4 s**", verify=lambda: "%.1f s" % (2 ** 32 * 8 / 1e9)),
       ],
       traps=[("ACK means next expected byte", "ack = last byte received + 1."),
              ("Timeout vs 3 dup ACKs", "Timeout resets cwnd to 1; fast retransmit (Reno) sets it to ssthresh."),
              ("SYN uses a sequence number", "The ACK of a SYN is x + 1."),
              ("Window units", "cwnd counts MSS in questions, bytes in the real protocol.")],
       quick=[("Slow start doubles cwnd every", ["segment", "RTT", "timeout", "10 ms"], 1, "Per RTT."),
              ("Three duplicate ACKs trigger", ["connection reset", "fast retransmit", "slow start only", "FIN"], 1, "Fast retransmit."),
              ("UDP header size is", ["8 bytes", "20 bytes", "4 bytes", "16 bytes"], 0, "Four 16-bit fields."),
              ("TCP closes a connection with", ["2 steps", "3 steps", "4 steps", "1 step"], 2, "FIN/ACK each way.")],
       summary=["UDP: 8-byte header, no reliability; TCP: 20-byte header, reliable byte stream.", "Handshake SYN → SYN+ACK → ACK; teardown 4 steps; ACK = next expected byte.", "Throughput ≤ window/RTT; flow control via rwnd.",
                "Slow start (×2/RTT) → congestion avoidance (+1/RTT).", "Timeout: ssthresh = cwnd/2, cwnd = 1; 3 dup ACKs: cwnd = ssthresh (Reno).", "Connection = 4-tuple; TIME-WAIT = 2·MSL."])


# ======================================================================================================
lesson(subject=S, chapter="Application Layer", ch_no=3, no=1, slug="cn-application-security", title="Application Layer Protocols & Network Security",
       topic="Application Layer & Security", minutes=24, weight=5, widget="none",
       key="Application protocols (DNS, HTTP, SMTP, FTP) run over TCP or UDP; DNS maps names to addresses hierarchically; HTTP latency depends on connection reuse. Security rests on symmetric and public-key cryptography (AES, RSA, Diffie–Hellman), hashes and digital signatures, and on firewalls, TLS and IPsec.",
       analogy=("🔐", "A padlock and a mailbox", "Public-key cryptography is a mailbox with a slot: anyone can drop a letter in (encrypt with the public key) but only the owner holds the key to take them out (decrypt with the private key). A digital signature is the reverse: only the owner can seal it, anyone can check the seal."),
       sections=[
           dict(h="DNS, HTTP, e-mail and file transfer", md="""- **DNS:** hierarchical distributed database (root → TLD → authoritative). UDP port 53 (TCP for zone transfers/large replies). Resolution is **recursive** (resolver does the work) or **iterative** (referrals). Records: A, AAAA, NS, MX, CNAME, PTR.
- **HTTP:** request/response over TCP port 80 (HTTPS 443). **Non-persistent** HTTP needs 2 RTT per object (TCP handshake + request); **persistent** reuses the connection (1 RTT per object, **pipelining** sends several requests at once). Methods GET, POST, HEAD, PUT, DELETE; status 200, 301, 404, 500. Cookies and caching/proxies reduce latency.
- **E-mail:** SMTP (port 25, push, TCP) between servers/from sender; POP3 / IMAP (pull) for retrieval; MIME for attachments.
- **FTP:** control connection port 21 and data connection port 20 — out-of-band control. **Telnet/SSH** remote login; **DHCP, SNMP** (161), **NTP**."""),
           dict(h="Symmetric and public-key cryptography", md="""- **Symmetric** (shared key): DES (56-bit key, 64-bit block, broken), 3DES, **AES** (128/192/256-bit keys, 128-bit block). Fast; the problem is key distribution. n users need n(n−1)/2 keys.
- **Public-key (asymmetric):** each user has a (public, private) pair; n users need 2n keys. Used for key exchange and signatures; slow.
- **RSA:** choose primes p, q; n = pq; φ(n) = (p−1)(q−1); pick e coprime to φ with d·e ≡ 1 (mod φ). Public key (e, n), private (d, n). **Encrypt:** c = mᵉ mod n. **Decrypt:** m = cᵈ mod n. Security relies on the difficulty of factoring n.
- **Diffie–Hellman:** public p, g; Alice sends gᵃ mod p, Bob sends gᵇ mod p; shared key gᵃᵇ mod p.""",
                formulas=[("c = mᵉ mod n;  m = cᵈ mod n;  d·e ≡ 1 (mod (p−1)(q−1))", "RSA")]),
           dict(h="Hashes, signatures and certificates", md="""A **cryptographic hash** (SHA-256, MD5 is broken) maps data to a fixed-size digest; it is one-way and collision-resistant. A **message authentication code (HMAC)** uses a shared key with a hash. A **digital signature** = encrypt the hash with the **private** key; the receiver decrypts with the signer's public key and compares (provides authentication, integrity and non-repudiation). A **certificate** binds a public key to an identity, signed by a CA (X.509, public-key infrastructure).

Security goals: confidentiality, integrity, authentication, non-repudiation, availability. Attacks: eavesdropping, replay, man-in-the-middle, DoS/DDoS, SYN flood, spoofing, phishing."""),
           dict(h="Network security mechanisms", md="""- **Firewalls:** packet filters (header fields), stateful, application-level proxies.
- **IPsec** (network layer): AH (authentication), ESP (encryption + authentication), transport vs tunnel mode (VPNs).
- **SSL/TLS** (above TCP): handshake negotiates ciphers and keys with public-key crypto, then symmetric encryption; HTTPS = HTTP over TLS.
- **PGP/S-MIME** for e-mail; **WPA2/WPA3** for Wi-Fi; **IDS/IPS** intrusion detection/prevention."""),
       ],
       examples=[
           Ex("RSA by hand", "With p = 3, q = 11, e = 7: compute n, φ(n), d, and encrypt m = 2.",
              ["n = 33, φ = 2 × 10 = 20. d with 7d ≡ 1 (mod 20): d = 3.", "Ciphertext c = 2⁷ mod 33 = 128 mod 33 = 29. Decrypting: 29³ mod 33 = 2 ✔."],
              "n = **33**, φ = **20**, d = **3**, c = **29**.", verify=lambda: "n = %d, φ = %d, d = %d, c = %d" % (3 * 11, 2 * 10, pow(7, -1, 20), pow(2, 7, 33))),
           Ex("Diffie–Hellman", "p = 23, g = 5, Alice's secret a = 6, Bob's secret b = 15. What is the shared key?",
              ["Alice sends 5⁶ mod 23 = 8; Bob sends 5¹⁵ mod 23 = 19.", "Shared key = 19⁶ mod 23 = 8¹⁵ mod 23 = **2**."],
              "**2**", verify=lambda: str(pow(pow(5, 15, 23), 6, 23))),
           Ex("HTTP latency", "A page has one base HTML file and 10 small embedded objects; RTT = 50 ms; ignore transmission time. Compare non-persistent HTTP without parallel connections to persistent HTTP without pipelining.",
              ["Non-persistent: 11 objects × 2 RTT = 22 RTT = 1100 ms.", "Persistent: 1 RTT handshake + 11 × 1 RTT = 12 RTT = 600 ms."],
              "Non-persistent **1100 ms**, persistent **600 ms**.", verify=lambda: "Non-persistent %d ms, persistent %d ms" % (11 * 2 * 50, (1 + 11) * 50)),
           Ex("Number of keys", "How many keys are needed for 100 users to communicate pairwise using symmetric and using public-key cryptography?",
              ["Symmetric: one key per pair of users ⇒ 100 × 99 / 2 = 4950.", "Public key: each user has one pair, i.e. two keys ⇒ 200."],
              "Symmetric **4950**, public-key **200**.", verify=lambda: "Symmetric %d, public-key %d" % (100 * 99 // 2, 2 * 100)),
       ],
       traps=[("Signing uses the private key", "Encryption for confidentiality uses the receiver's public key; signing uses the sender's private key."),
              ("DNS transport", "UDP for ordinary queries, TCP for zone transfers."),
              ("FTP uses two connections", "Control (21) and data (20)."),
              ("RSA decrypt exponent", "d is the modular inverse of e modulo φ(n), not modulo n.")],
       quick=[("Which port does SMTP use?", ["21", "25", "53", "80"], 1, "25."),
              ("A digital signature is created with the", ["receiver's public key", "sender's private key", "sender's public key", "session key"], 1, "Private key of the signer."),
              ("Which is a symmetric cipher?", ["RSA", "AES", "Diffie–Hellman", "ECC"], 1, "AES."),
              ("Persistent HTTP saves", ["TCP handshakes", "DNS lookups only", "port numbers", "cookies"], 0, "Reuses the connection.")],
       summary=["DNS (UDP 53, hierarchical), HTTP (TCP 80/443, persistent vs non-persistent), SMTP 25, FTP 21/20.", "Symmetric: AES, n(n−1)/2 keys; public key: 2n keys.", "RSA: n = pq, d·e ≡ 1 mod φ(n), c = mᵉ mod n.",
                "Diffie–Hellman shared key gᵃᵇ mod p.", "Hash + private-key signature gives integrity, authentication, non-repudiation.", "Firewalls, IPsec (AH/ESP), TLS protect traffic."])
