"""Computer Networks part 1: layering & physical layer, data link & error control, MAC & Ethernet."""
import math

from learn import Ex, lesson

S = "CN"


def crc(data, gen):
    d, g = int(data, 2), int(gen, 2)
    r = len(gen) - 1
    v = d << r
    while v.bit_length() > r:
        v ^= g << (v.bit_length() - len(gen))
    return format(v, "0%db" % r)


def hamming_r(m):
    r = 1
    while 2 ** r < m + r + 1:
        r += 1
    return r


def bit_stuff(bits):
    out, ones = "", 0
    for b in bits:
        out += b
        ones = ones + 1 if b == "1" else 0
        if ones == 5:
            out += "0"
            ones = 0
    return out


# ======================================================================================================
lesson(subject=S, chapter="Physical & Link Layers", ch_no=1, no=1, slug="cn-layering-physical", title="Network Layering, Delays & the Physical Layer",
       topic="Layering & Physical Layer", minutes=22, weight=4, widget="none",
       key="Networks are organised into layers (OSI's seven, TCP/IP's four or five) so each layer can be designed independently. The end-to-end delay of a packet is the sum of transmission, propagation, queuing and processing delays, and channel capacity is bounded by Nyquist (noiseless) and Shannon (noisy).",
       analogy=("📬", "Sending a parcel", "You pack the item (application), the post office labels it (transport and network), the van driver follows the road (link), and the road itself is the physical medium. Each stage only talks to the same stage at the other end and to its neighbour above and below."),
       sections=[
           dict(h="Layers and protocol data units", md="""| OSI layer | TCP/IP | PDU | Examples / devices |
|---|---|---|---|
| 7 Application | Application | message | HTTP, SMTP, DNS, FTP |
| 6 Presentation | | | encryption, compression, encoding |
| 5 Session | | | dialog control, synchronisation |
| 4 Transport | Transport | segment / datagram | TCP, UDP |
| 3 Network | Internet | packet | IP, routers, ICMP |
| 2 Data link | Link | frame | Ethernet, switches, bridges |
| 1 Physical | | bits | hubs, repeaters, cables |

Each layer adds a **header** (encapsulation) on the way down and removes it on the way up. **Connection-oriented** services (TCP) set up a connection; **connectionless** ones (UDP, IP) do not. **Circuit switching** reserves a path (constant delay, wasteful); **packet switching** shares links (statistical multiplexing, store-and-forward, variable delay)."""),
           dict(h="Delays and throughput", md="""For a packet of L bits over a link of rate R bits/s and length d with propagation speed s:

- **Transmission delay** Tt = L / R.
- **Propagation delay** Tp = d / s (about 2 × 10⁸ m/s in copper/fibre, 3 × 10⁸ m/s in air).
- **Queuing** and **processing** delays depend on load and hardware.
- With **store-and-forward**, a packet crosses N links in N × L/R (plus propagation); splitting a message into pipelined packets reduces the total time.
- **RTT** = 2·Tp (plus transmission and queuing). **Bandwidth–delay product** = R × RTT (or R × one-way delay) = number of bits 'in flight' filling the pipe.
- **Throughput** of a path = the minimum link rate (bottleneck).""",
                formulas=[("Tt = L / R;  Tp = d / s;  BDP = R × delay", "basic delay model")]),
           dict(h="Channel capacity: Nyquist and Shannon", md="""- **Nyquist (noiseless channel, bandwidth B Hz, L signal levels):** maximum bit rate = **2 B log₂ L** bits/s. Sampling theorem: sample at least 2B times per second.
- **Shannon (noisy channel):** C = **B log₂(1 + SNR)** where SNR is a *ratio*. Convert decibels: SNR = 10^(dB/10). The real limit is the smaller of the two.

**Transmission media:** twisted pair, coaxial, optical fibre (immune to EMI, highest rate), wireless. **Encoding:** NRZ, Manchester (self-clocking: the baud rate is twice the bit rate), 4B/5B. **Multiplexing:** FDM, TDM (synchronous/statistical), WDM. Hubs/repeaters regenerate signals (layer 1); a hub extends one collision domain."""),
           dict(h="Switching and network devices", md="""| Device | Layer | Splits |
|---|---|---|
| Repeater / hub | 1 | nothing (one collision domain) |
| Bridge / switch | 2 | collision domains (each port separate) |
| Router | 3 | broadcast domains |
| Gateway | up to 7 | protocol translation |

Delay in a **datagram** network: each packet routed independently; **virtual-circuit** network: path set up first, packets carry a VC id. Circuit-switch setup time is paid once."""),
       ],
       examples=[
           Ex("Shannon capacity", "A channel has bandwidth 3000 Hz and SNR of 30 dB. What is the maximum data rate?",
              ["SNR = 10^(30/10) = 1000.", "C = 3000 × log₂(1 + 1000) = 3000 × 9.967 ≈ **29,900 bps**."],
              "≈ **29,900** bps.", verify=lambda: "%d bps" % round(3000 * math.log2(1 + 10 ** (30 / 10)), -2)),
           Ex("Nyquist rate", "A noiseless 4 kHz channel uses 8 signal levels. What is the maximum bit rate?",
              ["Rate = 2 B log₂ L = 2 × 4000 × log₂ 8 = 2 × 4000 × 3.", "= **24,000 bps**."],
              "**24,000** bps.", verify=lambda: "%d bps" % (2 * 4000 * math.log2(8))),
           Ex("Store-and-forward delay", "A 12,000-bit packet crosses 3 links of 10 Mbps each (propagation ignored). What is the end-to-end delay?",
              ["Each link takes 12,000 / 10⁷ s = 1.2 ms to transmit the packet.", "Store-and-forward repeats this on each link: 3 × 1.2 = **3.6 ms**."],
              "**3.6 ms**", verify=lambda: "%.1f ms" % (3 * 12000 / 10 ** 7 * 1000)),
           Ex("Bandwidth–delay product", "A 100 Mbps link has a round-trip time of 40 ms. How many bits can be in flight?",
              ["BDP = 100 × 10⁶ × 0.040 s.", "= 4,000,000 bits = **4 Mbit** (500 KB)."],
              "**4 × 10⁶** bits.", verify=lambda: "%d × 10⁶ bits" % (100e6 * 0.040 / 1e6)),
       ],
       traps=[("dB is logarithmic", "Convert with 10^(dB/10) before using Shannon's formula."),
              ("Which delay?", "Transmission = L/R; propagation = d/s — they scale with different quantities."),
              ("Collision vs broadcast domains", "Switches split collision domains; routers split broadcast domains."),
              ("Manchester encoding", "Needs twice the bandwidth: baud rate = 2 × bit rate.")],
       quick=[("Which device operates at the network layer?", ["hub", "switch", "router", "repeater"], 2, "Routers."),
              ("Shannon capacity depends on", ["levels only", "bandwidth and SNR", "distance only", "frame size"], 1, "B log₂(1+SNR)."),
              ("PDU of the transport layer is a", ["bit", "frame", "packet", "segment"], 3, "Segment."),
              ("Propagation delay = ", ["L/R", "d/s", "R·d", "L·s"], 1, "Distance over speed.")],
       summary=["Layers: physical, link, network, transport, (session, presentation), application; PDUs: bits, frames, packets, segments.", "Delays: Tt = L/R, Tp = d/s; BDP = R × RTT.", "Store-and-forward over N links: N·L/R.",
                "Nyquist 2B log₂ L; Shannon B log₂(1+SNR), SNR = 10^(dB/10).", "Hub: one collision domain; switch: per port; router: per broadcast domain.", "Circuit vs packet switching."])


# ======================================================================================================
lesson(subject=S, chapter="Physical & Link Layers", ch_no=1, no=2, slug="cn-data-link-error", title="Data Link Layer: Framing, Error Control & Sliding Window",
       topic="Data Link & Error Control", minutes=26, weight=6, widget="crc",
       widget_hint="Enter data bits and a generator polynomial to get the CRC remainder and the transmitted codeword; then paste a corrupted copy into the received box to see the error detected.",
       key="The data link layer frames bits, detects/corrects errors (parity, checksum, CRC, Hamming codes) and controls flow with sliding-window protocols. GATE focuses on CRC division, Hamming bits, bit stuffing, window sizes and link efficiency.",
       analogy=("✉️", "Registered post with tracking", "Each envelope has a clear start and end (framing), a seal that shows tampering (CRC), a receipt that the recipient signs (ACK), and a limit on how many envelopes you may have out at once (window)."),
       sections=[
           dict(h="Framing and error detection", md="""**Framing:** character count, flag bytes with byte stuffing, and **bit stuffing** (HDLC flag 01111110; insert a 0 after five consecutive 1s of data).

**Error detection:** parity (detects odd numbers of bit errors), checksum (Internet checksum: 16-bit one's complement sum), and **CRC**. For CRC with generator G of degree r (r + 1 bits): append r zeros, divide by G using XOR (mod-2) division, and append the **r-bit remainder**. The receiver divides the whole codeword by G; remainder 0 ⇒ accepted.

A CRC detects **all single-bit errors** if G has ≥ 2 terms including 1, all burst errors of length ≤ r, all odd numbers of errors if (x + 1) divides G, and a burst longer than r + 1 bits with probability 1 − 2^(−r) (a burst of exactly r + 1 bits escapes with probability 2^(−(r−1)))."""),
           dict(h="Error correction: Hamming codes", md="""The **Hamming distance** between two codewords is the number of differing bits. A code with minimum distance d **detects** d − 1 errors and **corrects** ⌊(d − 1)/2⌋ errors.

**Hamming code:** check bits sit at positions 1, 2, 4, 8, …; with m data bits we need r check bits where **2ʳ ≥ m + r + 1**. For m = 11, r = 4 (the (15,11) code); for m = 4, r = 3 (the (7,4) code). The syndrome (parity of each check group) gives the position of a single erroneous bit.""",
                formulas=[("2ʳ ≥ m + r + 1", "check bits for single-error correction"), ("detects d−1, corrects ⌊(d−1)/2⌋ errors", "minimum distance d")]),
           dict(h="Flow control: stop-and-wait and sliding window", md="""Let Tt = frame transmission time and Tp = one-way propagation delay. Define a = Tp / Tt.

- **Stop-and-wait** efficiency η = Tt / (Tt + 2Tp) = 1 / (1 + 2a).
- **Sliding window** with window size N: η = min(1, N / (1 + 2a)); to keep the pipe full N ≥ 1 + 2a.
- **Go-Back-N:** receiver window 1; on error the sender retransmits the lost frame **and all following ones**; with k sequence-number bits the sender window ≤ **2ᵏ − 1**.
- **Selective Repeat:** receiver buffers out-of-order frames; only the erroneous frame is resent; windows ≤ **2ᵏ⁻¹** each (sender + receiver total ≤ 2ᵏ).
- **Piggybacking** carries ACKs inside data frames.""",
                call=[("trap", "Why the window limit?", "If the sender window were too large, a retransmitted old frame could be mistaken for a new frame with the same number after wrap-around.")]),
           dict(h="Protocols and addressing at this layer", md="""**HDLC / PPP** are standard link protocols. The data link layer also handles MAC addresses (48 bits, hex, first 24 bits = OUI), **ARP** (maps IP → MAC; broadcast request, unicast reply) lives between layers 2 and 3. The **channel utilisation** with errors and window N: efficiency also reduces by a factor (1 − p) for frame error probability p."""),
       ],
       examples=[
           Ex("CRC remainder", "Data 1101011011 with generator 10011 (x⁴ + x + 1). What is the CRC and the transmitted codeword?",
              ["Append 4 zeros: 11010110110000. Divide (XOR) by 10011.", "Remainder = 1110, so the codeword is 1101011011**1110**."],
              "CRC **1110**; codeword **11010110111110**.", verify=lambda: "CRC %s; codeword %s" % (crc("1101011011", "10011"), "1101011011" + crc("1101011011", "10011"))),
           Ex("Hamming check bits", "How many check bits are needed to protect 11 data bits with a single-error-correcting Hamming code?",
              ["Need 2ʳ ≥ 11 + r + 1: r = 3 gives 8 ≥ 15 ✘; r = 4 gives 16 ≥ 16 ✔.", "So **4** check bits."],
              "**4** check bits.", verify=lambda: str(hamming_r(11))),
           Ex("Stop-and-wait efficiency", "A 1000-bit frame is sent at 1 Mbps over a link with one-way propagation delay 20 ms. What is the stop-and-wait efficiency?",
              ["Tt = 1000 / 10⁶ = 1 ms; Tp = 20 ms.", "η = 1 / (1 + 2 × 20) = 1/41 ≈ **2.4 %**."],
              "≈ **2.4 %**", verify=lambda: "%.1f %%" % (100 / (1 + 2 * 20))),
           Ex("Window size to fill the pipe", "In the same link, what is the minimum sliding-window size for 100% utilisation, and how many sequence-number bits are needed for Go-Back-N?",
              ["N ≥ 1 + 2a = 41 frames.", "Go-Back-N needs N ≤ 2ᵏ − 1 ⇒ 2ᵏ ≥ 42 ⇒ k = **6** bits."],
              "Window **41**; **6** bits.", verify=lambda: "Window %d; %d bits" % (1 + 2 * 20, math.ceil(math.log2(41 + 1)))),
           Ex("Bit stuffing", "What is transmitted for the data bits 0111111011111010 after bit stuffing (insert 0 after five 1s)?",
              ["Data: 0 111111 0 11111 0 1 0. The first run has six 1s: after the fifth a 0 is inserted (the sixth 1 follows it).", "The second run has exactly five 1s, so a 0 is inserted after it as well (the receiver cannot tell it from a flag otherwise).", "Result: **011111010111110010**."],
              "**011111010111110010**", verify=lambda: bit_stuff("0111111011111010")),
       ],
       traps=[("Remainder length", "CRC remainder has one bit fewer than the generator."),
              ("Window size limits", "GBN: 2ᵏ − 1; SR: 2ᵏ⁻¹."),
              ("Efficiency formula", "Use a = Tp/Tt, and 1/(1+2a) for stop-and-wait."),
              ("Correct vs detect", "Distance d detects d−1 errors but corrects only ⌊(d−1)/2⌋.")],
       quick=[("A CRC with a 5-bit generator appends how many bits?", ["5", "4", "6", "1"], 1, "Degree = bits − 1."),
              ("Go-Back-N with 3-bit sequence numbers has maximum window", ["8", "7", "4", "3"], 1, "2³ − 1."),
              ("Minimum distance 5 corrects how many errors?", ["1", "2", "3", "4"], 1, "⌊4/2⌋."),
              ("Which protocol buffers out-of-order frames?", ["stop-and-wait", "Go-Back-N", "selective repeat", "ALOHA"], 2, "Selective repeat.")],
       summary=["Framing by flags and bit stuffing (0 after five 1s).", "CRC: append r zeros, divide by G, append remainder; receiver checks remainder 0.", "Hamming: 2ʳ ≥ m + r + 1; distance d detects d−1 and corrects ⌊(d−1)/2⌋.",
                "Stop-and-wait η = 1/(1+2a); sliding window η = min(1, N/(1+2a)).", "GBN window ≤ 2ᵏ−1; SR ≤ 2ᵏ⁻¹.", "Parity detects odd numbers of errors; Internet checksum is a 16-bit one's-complement sum."])


# ======================================================================================================
lesson(subject=S, chapter="Physical & Link Layers", ch_no=1, no=3, slug="cn-mac-ethernet", title="Medium Access Control, Ethernet & Switching",
       topic="MAC & Ethernet", minutes=22, weight=5, widget="none",
       key="When many stations share a channel the MAC protocol decides who talks: ALOHA and slotted ALOHA are simple but inefficient, CSMA/CD (Ethernet) listens and detects collisions and needs a minimum frame size of 2·Tp·R, and switches learn MAC addresses to forward frames only where needed.",
       analogy=("🗣️", "A conversation in a room", "If everyone speaks whenever they like (ALOHA) many words collide. If you wait for a pause (CSMA) it's better, and if you stop as soon as you hear someone else (collision detection) and try again after a random pause, the room works well — as long as the room isn't too big for people to hear each other quickly."),
       sections=[
           dict(h="Random access protocols", md="""| Protocol | Idea | Max efficiency |
|---|---|---|
| **Pure ALOHA** | transmit any time; collision window 2·T | S = G·e^(−2G), max **1/(2e) ≈ 18.4 %** at G = 0.5 |
| **Slotted ALOHA** | transmit only at slot starts; window T | S = G·e^(−G), max **1/e ≈ 36.8 %** at G = 1 |
| **CSMA** (1-persistent, p-persistent, non-persistent) | sense before sending | higher |
| **CSMA/CD** | sense, detect collision while sending, abort, back off | high for small a |
| **CSMA/CA** (Wi-Fi) | avoid collisions with random back-off, RTS/CTS | – |

G = average frames offered per frame time, S = throughput."""),
           dict(h="CSMA/CD and Ethernet", md="""A collision is detected only if the sender is still transmitting when the collision signal returns, which takes up to **2·Tp** (round-trip propagation). So the frame transmission time must satisfy **Tt ≥ 2·Tp**, i.e. the **minimum frame size = 2 · Tp · R**. Classic 10 Mbps Ethernet: slot time 51.2 µs ⇒ **512 bits = 64 bytes** minimum frame; maximum payload 1500 bytes.

After the n-th collision the station chooses K uniformly from {0, 1, …, 2ⁿ − 1} (**binary exponential backoff**, n capped at 10, give up after 16 attempts) and waits K × slot time.

**Ethernet frame:** preamble (7 B) + SFD (1 B) + destination MAC (6) + source MAC (6) + type/length (2) + data (46–1500) + FCS (4). Fast/Gigabit Ethernet keep the 64-byte minimum, shrinking the allowed distance (or using carrier extension/frame bursting)."""),
           dict(h="Switches, bridges and VLANs", md="""A **learning switch** builds a table MAC → port by reading the **source** address of incoming frames; it forwards to the port of the **destination** if known, otherwise **floods** to all ports except the incoming one. Frames to the same port they arrived on are filtered. Each switch port is its own collision domain, so full-duplex Ethernet has no CSMA/CD at all; the whole LAN remains one broadcast domain unless **VLANs** (802.1Q) are used. **Spanning Tree Protocol** blocks redundant links to prevent loops.

**Wi-Fi (802.11)** uses CSMA/CA with ACKs, because the hidden-terminal problem prevents collision detection. **Token ring** passes a token so only the holder may send — no collisions, bounded delay."""),
       ],
       examples=[
           Ex("Minimum frame size", "A CSMA/CD network runs at 10 Mbps and the maximum one-way propagation delay between stations is 25.6 µs. What is the minimum frame size?",
              ["Round trip = 2 × 25.6 µs = 51.2 µs.", "Minimum frame = 51.2 µs × 10 Mbps = 512 bits = **64 bytes**."],
              "**512** bits (64 bytes).", verify=lambda: "%d bits (%d bytes)" % (2 * 25.6e-6 * 10e6, 2 * 25.6e-6 * 10e6 / 8)),
           Ex("Slotted ALOHA throughput", "Compute the throughput of slotted ALOHA at G = 1 and pure ALOHA at G = 0.5.",
              ["Slotted: S = G e^(−G) = e⁻¹ ≈ 0.368 at G = 1.", "Pure: S = G e^(−2G) = 0.5 e⁻¹ ≈ 0.184 at G = 0.5."],
              "Slotted **0.368**, pure **0.184**.", verify=lambda: "Slotted %.3f, pure %.3f" % (1 * math.exp(-1), 0.5 * math.exp(-1))),
           Ex("Backoff range", "After the 4th collision, from how many values does the station choose its backoff, and what is the maximum wait in slot times?",
              ["K is chosen from {0, …, 2⁴ − 1} = {0, …, 15}: 16 values.", "Maximum wait = 15 slot times."],
              "**16** values; maximum **15** slots.", verify=lambda: "%d values; maximum %d slots" % (2 ** 4, 2 ** 4 - 1)),
           Ex("Maximum distance in 1 Gbps CSMA/CD", "With a minimum frame size of 64 bytes at 1 Gbps and propagation speed 2 × 10⁸ m/s, what is the maximum network length?",
              ["Tt = 512 bits / 10⁹ = 0.512 µs; this must cover the round trip: Tp = 0.256 µs.", "Distance = 0.256 µs × 2×10⁸ m/s = **51.2 m** (hence carrier extension in practice)."],
              "**51.2 m**", verify=lambda: "%.1f m" % (512 / 1e9 / 2 * 2e8)),
       ],
       traps=[("Round trip", "Collision detection needs Tt ≥ 2·Tp, not Tp."),
              ("Switch learning", "Learns from the source address, forwards by the destination address."),
              ("Slot time vs frame time", "ALOHA's G is per frame time; Ethernet's slot is 512 bit times."),
              ("Collision domains", "Each switch port is separate; the whole switched LAN is still one broadcast domain.")],
       quick=[("Maximum efficiency of slotted ALOHA is", ["18.4 %", "36.8 %", "50 %", "100 %"], 1, "1/e."),
              ("Min frame size in CSMA/CD", ["Tp × R", "2 × Tp × R", "Tp / R", "R / Tp"], 1, "Round trip."),
              ("A switch learns addresses from", ["destination MAC", "source MAC", "IP address", "ARP"], 1, "Source."),
              ("Which Ethernet device has one collision domain for all ports?", ["switch", "router", "hub", "bridge"], 2, "Hub.")],
       summary=["Pure ALOHA 18.4 %, slotted 36.8 %.", "CSMA/CD: Tt ≥ 2Tp ⇒ minimum frame = 2·Tp·R (512 bits at 10 Mbps).", "Binary exponential backoff: K ∈ {0 … 2ⁿ−1}.", "Ethernet frame: 14-byte header, 46–1500 data, 4-byte FCS.",
                "Learning switch: source → table, destination → forward/flood; STP prevents loops.", "CSMA/CA for Wi-Fi; token ring has no collisions."])
