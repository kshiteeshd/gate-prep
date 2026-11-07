"""Computer Networks — curated concept questions."""
from content.kit import C

C("CN", "Layering & Physical Layer", "Concepts", [
    ("e", 1, "s", "Which layer of the OSI model is responsible for end-to-end reliable delivery?", ["Transport layer", "Network layer", "Data link layer", "Session layer"], 0, "TCP provides reliability at the transport layer."),
    ("e", 1, "s", "The OSI layer that translates data formats, encryption and compression is the", ["Presentation layer", "Session layer", "Application layer", "Transport layer"], 0, "Not present as a separate layer in TCP/IP."),
    ("e", 1, "s", "How many layers does the TCP/IP model (as usually taught) have?", ["4", "5", "7", "3"], 0, "Application, transport, internet, link (4); the 5-layer hybrid splits link into data-link and physical."),
    ("m", 1, "s", "Repeaters and hubs operate at the", ["Physical layer", "Data link layer", "Network layer", "Transport layer"], 0, "They regenerate bits and know nothing about frames."),
    ("m", 2, "m", "Which devices operate at least up to the network layer? (select all)", ["Router", "Layer-3 switch", "Hub", "Layer-2 bridge"], [0, 1], "Bridges and hubs are below layer 3."),
    ("m", 1, "s", "Attenuation in a transmission medium is the", ["loss of signal strength with distance", "delay variation", "unwanted external noise", "mixing of two channels"], 0, "Measured in dB."),
    ("h", 2, "s", "In a packet-switched network, store-and-forward switching means", ["a switch receives the entire packet before forwarding it", "packets are forwarded bit by bit", "packets are reordered at each hop", "a circuit is reserved end to end"], 0, "This adds a transmission delay per hop."),
    ("m", 2, "s", "Compared with circuit switching, packet switching", ["allows statistical multiplexing and better utilisation for bursty traffic", "guarantees a fixed delay", "needs call setup for every packet", "wastes bandwidth when idle"], 0, "Circuit switching reserves capacity even when idle."),
])

C("CN", "Data Link & Error Control", "Concepts", [
    ("e", 1, "s", "A single parity bit can detect", ["any odd number of bit errors", "any even number of bit errors", "all burst errors", "and correct a 1-bit error"], 0, "Even numbers of flips leave parity unchanged."),
    ("m", 1, "s", "CRC with a generator polynomial of degree r detects all burst errors of length", ["≤ r", "> r", "exactly 2r", "only odd lengths"], 0, "Bursts up to r bits are always detected."),
    ("m", 2, "s", "In Go-Back-N ARQ the receiver window size is", ["1", "equal to the sender window", "2^k", "unbounded"], 0, "The receiver accepts only the next in-order frame."),
    ("m", 2, "s", "Selective Repeat requires sender and receiver window sizes of at most", ["half the sequence-number space", "the full sequence-number space", "one less than the sequence space", "one"], 0, "To avoid ambiguity between old and new frames."),
    ("m", 1, "s", "Byte stuffing is used in", ["PPP", "Ethernet", "ARP", "ICMP"], 0, "PPP uses flag byte 0x7E with an escape byte."),
    ("h", 2, "m", "A code has minimum Hamming distance 5. Which are guaranteed? (select all)", ["Detects up to 4 errors", "Corrects up to 2 errors", "Corrects up to 4 errors", "Detects exactly 5 errors only"], [0, 1], "Detect d−1 = 4; correct ⌊(d−1)/2⌋ = 2."),
    ("h", 2, "s", "A Hamming (7,4) code can", ["correct any single-bit error", "correct any two-bit error", "only detect single errors", "correct burst errors of length 4"], 0, "3 check bits give single-error correction."),
    ("m", 1, "s", "Stop-and-wait ARQ becomes inefficient when", ["the bandwidth-delay product is large relative to the frame size", "frames are large and RTT is tiny", "the channel is error free", "the window equals one"], 0, "The sender idles during the RTT."),
])

C("CN", "MAC & Ethernet", "Concepts", [
    ("e", 1, "s", "CSMA/CD is used in", ["classic (half-duplex) Ethernet", "Wi-Fi 802.11", "token ring", "ATM"], 0, "Wireless uses CSMA/CA."),
    ("m", 1, "s", "In CSMA/CD, the minimum frame length is chosen so that", ["the sender can still detect a collision while transmitting", "frames are always aligned to 64 bits", "the preamble is long enough", "ACKs are not needed"], 0, "Frame transmission time ≥ 2 × propagation delay."),
    ("m", 2, "s", "If the bandwidth of an Ethernet segment is increased 10× with the same minimum frame size, the maximum cable length", ["decreases by a factor of 10", "increases 10×", "is unchanged", "doubles"], 0, "L_min = 2·Tp·R ⇒ Tp ∝ 1/R."),
    ("m", 1, "s", "The maximum efficiency of slotted ALOHA is", ["1/e ≈ 36.8%", "1/(2e) ≈ 18.4%", "50%", "100%"], 0, "At G = 1."),
    ("m", 2, "s", "A learning switch floods a frame when", ["the destination MAC is not in its forwarding table", "the source MAC is known", "the frame is a unicast to a known port", "the frame has a bad CRC"], 0, "Unknown unicast and broadcast frames are flooded."),
    ("h", 2, "s", "Which of these statements about VLANs is TRUE?", ["They create separate broadcast domains on the same physical switch", "They require a router for any communication within the same VLAN", "They increase the number of collision domains per port", "They operate at the physical layer"], 0, "Inter-VLAN traffic needs layer-3 routing."),
    ("h", 2, "s", "The spanning-tree protocol is used in switched LANs to", ["avoid loops in the topology", "assign IP addresses", "balance routing loads", "encrypt frames"], 0, "It blocks redundant links."),
])

C("CN", "IP Addressing & Subnetting", "Concepts", [
    ("e", 1, "s", "The number of bits in the network+subnet portion of 255.255.240.0 is", ["20", "16", "24", "18"], 0, "255.255.240.0 = /20."),
    ("e", 1, "s", "Which of the following is a valid private IPv4 address?", ["172.20.5.9", "172.32.5.9", "192.169.1.1", "11.0.0.1"], 0, "172.16.0.0/12 spans 172.16–172.31."),
    ("m", 1, "s", "The IPv4 header checksum covers", ["only the header", "header and payload", "payload only", "the pseudo-header only"], 0, "It is recomputed at every hop because TTL changes."),
    ("m", 2, "s", "A router receives a datagram with TTL = 1 destined elsewhere. It will", ["discard it and send an ICMP Time Exceeded message", "forward it with TTL 0", "forward it unchanged", "buffer it until the TTL is refreshed"], 0, "TTL is decremented to 0 ⇒ drop."),
    ("m", 1, "s", "Fragments of an IP datagram are reassembled", ["only at the final destination", "at each router", "at the first router", "by the sender"], 0, "Fragments may take different paths."),
    ("h", 2, "s", "NAT with port translation allows", ["many private hosts to share one public IP address", "unlimited public hosts per port", "end-to-end IP addressing without modification", "IPv6 to IPv4 translation only"], 0, "The NAT table maps (private IP, port) ↔ (public IP, port)."),
    ("h", 2, "s", "CIDR route aggregation (supernetting) is mainly used to", ["reduce the size of routing tables", "increase the number of hosts per network class", "enable multicast", "speed up ARP"], 0, "Contiguous prefixes are advertised as one."),
    ("m", 1, "s", "The all-ones host portion of an IPv4 subnet address is the", ["directed broadcast address", "network address", "gateway address", "loopback address"], 0, "The all-zeros host portion is the network address."),
    ("m", 2, "m", "Which of the following are TRUE about IPv6? (select all)", ["Addresses are 128 bits long", "Routers do not fragment packets in transit", "The header has a checksum field", "Broadcast is replaced by multicast/anycast"], [0, 1, 3], "IPv6 removed the header checksum."),
])

C("CN", "Routing", "Concepts", [
    ("e", 1, "s", "Distance-vector routing is a", ["Bellman–Ford based algorithm sharing tables with neighbours", "Dijkstra based algorithm using global topology", "static routing method", "flooding method"], 0, "Link-state uses Dijkstra with a full map."),
    ("m", 1, "s", "The count-to-infinity problem occurs in", ["distance-vector routing", "link-state routing", "static routing", "source routing"], 0, "Split horizon/poison reverse mitigate it."),
    ("m", 1, "s", "OSPF is a", ["link-state interior gateway protocol", "distance-vector interior gateway protocol", "path-vector exterior gateway protocol", "transport protocol"], 0, "BGP is path-vector."),
    ("m", 2, "s", "BGP is classified as", ["a path-vector protocol used between autonomous systems", "a link-state protocol", "a distance-vector protocol using hop count", "an interior routing protocol"], 0, "Policy-based routing between ASes."),
    ("m", 2, "m", "Which statements about link-state routing are TRUE? (select all)", ["Each router floods its link costs to all routers", "Each router runs Dijkstra on its own copy of the topology", "Routers exchange only with direct neighbours the full routing table", "It converges faster than basic distance-vector in general"], [0, 1, 3], "Exchanging whole tables with neighbours is distance-vector."),
    ("h", 2, "s", "Split horizon with poison reverse helps by", ["advertising a route back to the neighbour it was learned from with infinite metric", "never advertising any route", "delaying all updates", "using triggered updates only"], 0, "Prevents two-node loops."),
    ("h", 2, "s", "RIP limits the network diameter because", ["16 hops is treated as infinity", "it uses 4-bit costs only for bandwidth", "OSPF is required beyond 5 hops", "TTL cannot exceed 16"], 0, "Maximum usable hop count is 15."),
])

C("CN", "Transport Layer (TCP/UDP)", "Concepts", [
    ("e", 1, "s", "Which transport protocol is connectionless and unreliable?", ["UDP", "TCP", "SCTP", "ICMP"], 0, "UDP just adds ports and an optional checksum."),
    ("m", 1, "s", "TCP flow control is implemented by", ["the receiver's advertised window", "the sender's congestion window", "ICMP source quench", "the router queue size"], 0, "rwnd limits unacknowledged data."),
    ("m", 2, "s", "In TCP, the congestion window grows exponentially during", ["slow start", "congestion avoidance", "fast recovery", "timeout"], 0, "It doubles each RTT until ssthresh."),
    ("m", 2, "s", "On three duplicate ACKs, TCP Reno", ["halves ssthresh, performs fast retransmit and enters fast recovery", "sets cwnd to 1 MSS", "closes the connection", "ignores the ACKs"], 0, "Tahoe would reset cwnd to 1."),
    ("m", 1, "s", "A TCP connection is terminated using", ["FIN / ACK exchanges (four-way close)", "RST only", "SYN-ACK", "a single FIN"], 0, "Each direction is closed separately."),
    ("h", 2, "s", "The sequence number in a TCP segment header identifies", ["the first byte of data in the segment", "the segment count", "the last byte of data", "the connection ID"], 0, "TCP numbers bytes, not segments."),
    ("h", 2, "m", "Which of these are functions of TCP but NOT of UDP? (select all)", ["Congestion control", "Reliable in-order delivery", "Port multiplexing", "Flow control"], [0, 1, 3], "Both protocols use ports."),
    ("h", 2, "s", "The Nagle algorithm is intended to", ["reduce the number of small packets by coalescing data", "speed up slow start", "remove delayed ACKs", "increase the MSS"], 0, "Send small data only when previous data is acknowledged."),
])

C("CN", "Application Layer & Security", "Concepts", [
    ("e", 1, "s", "DNS translates", ["domain names to IP addresses", "IP addresses to MAC addresses", "ports to services", "URLs to files"], 0, "ARP does IP→MAC."),
    ("m", 1, "s", "Which protocol is used by a mail client to SEND mail to its server?", ["SMTP", "IMAP", "POP3", "FTP"], 0, "IMAP/POP3 fetch mail."),
    ("m", 1, "s", "HTTP is a stateless protocol; web servers maintain sessions using", ["cookies", "TCP sequence numbers", "DNS records", "ARP tables"], 0, "Cookies carry a session id."),
    ("m", 2, "s", "In public-key cryptography, to send a confidential message to Bob you encrypt with", ["Bob's public key", "your private key", "Bob's private key", "your public key"], 0, "Only Bob's private key can decrypt."),
    ("m", 2, "s", "A digital signature is created by encrypting the message digest with the signer's", ["private key", "public key", "session key", "hash key"], 0, "Anyone verifies using the public key."),
    ("h", 2, "s", "A man-in-the-middle attack on an unauthenticated Diffie–Hellman exchange is possible because", ["DH alone does not authenticate the parties", "the shared key is sent in clear", "the modulus is public", "the exponent is small"], 0, "Authentication (certificates) is needed."),
    ("h", 2, "m", "Which of these protocols run over TCP? (select all)", ["HTTP", "SMTP", "FTP", "DNS zone transfer", "DHCP"], [0, 1, 2, 3], "DHCP uses UDP; DNS queries use UDP but zone transfers use TCP."),
    ("h", 2, "s", "Symmetric-key encryption compared with public-key encryption is generally", ["much faster but needs a secure key distribution method", "slower and needs no shared secret", "unable to provide confidentiality", "only usable for signatures"], 0, "Hybrid schemes (TLS) combine both."),
])
