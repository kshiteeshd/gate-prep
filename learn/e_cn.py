"""Textbook-style long-form teaching text: Computer Networks."""
from learn import elab

elab("cn-layering-physical",
 ("Why networks are built in layers", """
Sending a web page from a server to your laptop involves cables or radio, error handling, finding a route across many networks, making sure no data is lost, and finally the application protocol itself. Rather than one giant program, the work is divided into **layers**, each providing a service to the one above and using the service of the one below. Each layer talks to its *peer* layer on the other machine through a **protocol**.

The **OSI model** has seven layers (physical, data link, network, transport, session, presentation, application). The **TCP/IP model** used in practice has four or five: **application, transport, network (internet), link, physical**. As data moves down the stack, each layer adds its own **header** (and sometimes a trailer) — this is **encapsulation**; on the receiving side each layer strips its header.
"""),
 ("Where each layer works", """
- **Physical:** bits as signals on a medium.
- **Data link:** frames between neighbouring machines; MAC addresses, error detection, access to shared media.
- **Network:** packets between any two hosts across networks; IP addresses and routing.
- **Transport:** process-to-process delivery; ports; reliability (TCP) or speed (UDP).
- **Application:** HTTP, DNS, SMTP, FTP.

The device at each layer: hubs and repeaters (physical), bridges and switches (data link), routers (network).
"""),
 ("Delay and bandwidth", """
The time to send a packet of length $L$ bits over a link of bandwidth $R$ bits/s is the **transmission delay** $T_t=L/R$. The **propagation delay** is $T_p=d/s$ (distance over signal speed). The **bandwidth–delay product** $R\\times\\text{delay}$ is the number of bits "in flight" on the link. Total latency for one packet over one link ignoring queuing is $T_t+T_p$. A channel's capacity is limited by **Nyquist** (noiseless: $2B\\log_2V$ bits/s) and **Shannon** (noisy: $B\\log_2(1+\\text{SNR})$).
"""),
)

elab("cn-data-link-error",
 ("Framing and error detection", """
The data link layer groups bits into **frames** and must let the receiver find where each frame starts and ends. **Bit stuffing** inserts a 0 after every run of five 1s so that the flag pattern `01111110` never appears inside the data; the receiver removes the extra 0s. **Byte stuffing** does the same using escape characters.

Errors flip bits in transit, so frames carry extra bits for detection. A **parity bit** detects any odd number of bit errors. A **checksum** adds the data words. The **cyclic redundancy check (CRC)** treats the data as a polynomial, divides it by a generator polynomial $G(x)$ and appends the remainder; the receiver divides again and expects remainder 0. CRC detects all burst errors shorter than the degree of $G$.
"""),
 ("Error correction and flow control", """
The **Hamming distance** between two codewords is the number of bit positions in which they differ. A code with minimum distance $d$ can *detect* $d-1$ errors and *correct* $\\lfloor(d-1)/2\\rfloor$ errors.

**Flow control** stops a fast sender overwhelming a slow receiver. **Stop-and-wait** sends one frame and waits for the acknowledgement; its efficiency is $\\frac{T_t}{T_t+2T_p}$, poor for long links. **Sliding window** keeps several frames in flight: with window size $W$ the utilisation is $\\min\\bigl(1,\\frac{W\\,T_t}{T_t+2T_p}\\bigr)$. **Go-Back-N** retransmits all frames from the lost one onwards (receiver window 1, sender window up to $2^k-1$ for $k$-bit sequence numbers); **Selective Repeat** retransmits only the lost frame (both windows up to $2^{k-1}$).
"""),
)

elab("cn-mac-ethernet",
 ("Sharing one channel", """
When many stations share one medium, simultaneous transmissions **collide**. **Medium access control (MAC)** protocols decide who may transmit. **Pure ALOHA** lets anyone send at any time; the maximum throughput is $\\frac{1}{2e}\\approx18.4\\%$. **Slotted ALOHA** allows sending only at the start of slots, doubling the maximum to $\\frac1e\\approx36.8\\%$.

**CSMA (carrier sense multiple access)** listens before sending. **CSMA/CD** (collision detection, used in classic Ethernet) also listens *while* sending, and on a collision stops and waits a random time chosen by **binary exponential backoff**: after the $k$-th collision pick a delay from $0..2^k-1$ slot times.
"""),
 ("Ethernet details", """
For collisions to be detected, a station must still be transmitting when the collision signal returns, so the transmission time must be at least twice the propagation delay: $T_t\\ge2T_p$, i.e. **minimum frame length $=2\\,T_p\\times$ bandwidth**. Ethernet fixes a minimum frame of 64 bytes for this reason.

A MAC address is a 48-bit hardware address. A **switch** learns which MAC address lives on which port, forwards frames only where needed, and gives each port its own **collision domain**. A **VLAN** splits one physical switch into several broadcast domains. Wi-Fi uses **CSMA/CA** (collision avoidance) because a wireless station cannot easily listen while sending.
"""),
)

elab("cn-ip-subnetting",
 ("IP addresses", """
An **IPv4 address** has 32 bits, written as four decimal bytes (like 192.168.10.5). It consists of a **network part** and a **host part**. In the old **classful** scheme the first bits decide the class: class A (0xxxxxxx, /8), B (10xxxxxx, /16), C (110xxxxx, /24), D is multicast (1110) and E is reserved.

In **CIDR (classless)** notation, the prefix length is written explicitly: 192.168.10.0**/26** means the first 26 bits are the network and the remaining 6 are for hosts. The **subnet mask** has 1s for the network part: /26 is 255.255.255.192.
"""),
 ("Subnet arithmetic", """
With $h$ host bits a network has $2^h$ addresses, of which two are reserved (the **network address** with all host bits 0 and the **broadcast address** with all 1s), leaving $2^h-2$ usable hosts. To find the network address, AND the IP address with the mask.

To split a network into subnets, borrow host bits: borrowing $b$ bits gives $2^b$ subnets. For example /24 split into 4 subnets uses /26, each with $2^6-2=62$ usable hosts. **Variable-length subnet masking (VLSM)** uses different prefix lengths for different needs. **Route aggregation (supernetting)** combines contiguous blocks into one shorter prefix.
"""),
 ("Supporting protocols", """
**ARP** finds the MAC address for a known IP address on the local network; **DHCP** gives hosts their addresses automatically; **ICMP** reports errors (and underlies ping). **NAT** lets many private addresses share one public address by rewriting addresses and ports. **IPv6** has 128-bit addresses, which solves address exhaustion, and no fragmentation by routers.

IP **fragmentation**: if a packet is larger than the link's **MTU**, it is split into fragments; each carries a **fragment offset** (in units of 8 bytes) and a "more fragments" flag, and the destination reassembles them.
"""),
)

elab("cn-routing",
 ("Finding paths", """
A router looks at the destination address of each packet and chooses the **next hop** from its **routing table**, using **longest prefix match**: among all matching entries, the one with the longest prefix wins. Routing tables can be set by hand (**static**) or built automatically by **routing protocols** (**dynamic**).
"""),
 ("Distance vector routing", """
Each router keeps a table of distances to all destinations and periodically sends it to its neighbours. On receiving a neighbour's table, it updates by the **Bellman–Ford equation**: $d(x,y)=\\min_v[c(x,v)+d(v,y)]$. It is simple, but suffers from the **count-to-infinity problem**: when a link fails, bad news travels slowly because routers keep increasing their distances through each other. Remedies are **split horizon**, **poison reverse** and a small maximum "infinity" (RIP uses 16). **RIP** is the classic distance-vector protocol.
"""),
 ("Link state routing and the Internet", """
In **link-state** routing, every router learns the *whole* topology by flooding information about its links, and then runs **Dijkstra's algorithm** to compute the shortest paths. It converges quickly and avoids count-to-infinity but needs more memory. **OSPF** is the standard example.

The Internet is organised into **autonomous systems (AS)**. Inside an AS, an **interior gateway protocol** (RIP, OSPF) is used; between ASes, **BGP** (a path-vector protocol) exchanges reachability and applies policy.
"""),
)

elab("cn-transport-tcp",
 ("What the transport layer adds", """
IP delivers packets between *hosts* on a best-effort basis: packets may be lost, duplicated or reordered. The transport layer provides delivery between *processes*, identified by **port numbers**. **UDP** adds only ports and a checksum: connectionless and fast (DNS, streaming). **TCP** provides a **reliable, ordered byte stream**: it numbers bytes, acknowledges them, retransmits losses, and controls flow and congestion.
"""),
 ("TCP connections and reliability", """
A TCP connection starts with a **three-way handshake**: SYN, SYN+ACK, ACK. Closing uses FIN and ACK in each direction. Every byte has a **sequence number**; the acknowledgement number is the next byte expected (**cumulative ack**). A lost segment is retransmitted after a **timeout**, or earlier after three duplicate ACKs (**fast retransmit**).

**Flow control:** the receiver advertises a **window** (`rwnd`); the sender never has more unacknowledged data than the window allows. Throughput is at most window / RTT.
"""),
 ("Congestion control", """
The sender also keeps a **congestion window (`cwnd`)** and may send $\\min(\\text{cwnd},\\text{rwnd})$. In **slow start**, `cwnd` starts at 1 segment and **doubles every RTT** (it grows by one segment per ACK) until it reaches the **slow-start threshold (ssthresh)**; then **congestion avoidance** grows it by one segment per RTT (additive increase). On a timeout, `ssthresh` is set to half of the current `cwnd` and `cwnd` drops to 1 (**multiplicative decrease**). On three duplicate ACKs (Reno), the window is halved and the sender continues in congestion avoidance. This is the AIMD pattern that makes TCP share links fairly.
"""),
)

elab("cn-application-security",
 ("Application-layer protocols", """
Applications use the network through well-known protocols. **DNS** maps names to IP addresses through a hierarchy of servers, using UDP port 53. **HTTP** (port 80, HTTPS 443) fetches web resources: requests carry a method (GET, POST), responses a status code (200, 404). **SMTP** (25) sends email, **POP3/IMAP** read it, **FTP** (21) transfers files, **Telnet/SSH** give remote access.
"""),
 ("Cryptography basics", """
**Symmetric** cryptography (AES, DES) uses the same secret key to encrypt and decrypt; it is fast but requires sharing the key. **Public-key** cryptography uses a key pair: a *public* key anyone may use to encrypt and a *private* key that decrypts. With $n$ users, symmetric keys need $\\frac{n(n-1)}{2}$ pairs; public-key needs $n$ pairs.

**RSA.** Choose primes $p,q$; $n=pq$; $\\phi=(p-1)(q-1)$; pick $e$ coprime to $\\phi$; compute $d$ with $de\\equiv1\\pmod\\phi$. Public key $(e,n)$, private key $(d,n)$. Encrypt $c=m^e\\bmod n$; decrypt $m=c^d\\bmod n$.

A **digital signature** applies the *private* key to a hash of the message; anyone can verify with the public key. A **hash function** maps data to a fixed-size digest; it should be one-way and collision-resistant.
"""),
 ("Network security", """
A **firewall** filters packets by address, port and state. **TLS/SSL** secures a connection by authenticating the server with a **certificate** and agreeing a session key. Typical attacks: **denial of service** (flooding), **man-in-the-middle**, **replay**, **SQL injection**, **phishing**. Authentication (who are you), confidentiality (secrecy), integrity (unchanged) and non-repudiation (cannot deny) are the four goals.
"""),
)
