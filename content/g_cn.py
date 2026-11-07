"""Computer Networks — parametric generators."""
import heapq
import ipaddress
import math

from content.kit import *

S = "CN"
LY, DL, MC, IP, RT, TP, AP = ("Layering & Physical Layer", "Data Link & Error Control", "MAC & Ethernet", "IP Addressing & Subnetting", "Routing", "Transport Layer (TCP/UDP)", "Application Layer & Security")


# ---------------- layering / physical ----------------
@gen(S, LY, "Capacity & delay", n=120, diff="medium")
def ly_cap(r):
    kind = r.choice(["nyq", "shan", "snr", "tx", "e2e", "bdp", "pipe", "levels", "overhead", "util"])
    B = r.choice([1, 2, 3, 4, 5, 10]) * 1000
    L = r.choice([2, 4, 8, 16, 32])
    if kind == "nyq": return nat(r, "A noiseless channel has bandwidth %d Hz and the signal uses %d discrete levels. Maximum data rate (bps) by Nyquist?" % (B, L), int(2 * B * math.log2(L)), "C = 2B·log₂L.")
    if kind == "shan":
        snr = r.choice([3, 7, 15, 31, 63, 127, 255])
        return nat(r, "A channel has bandwidth %d Hz and signal-to-noise ratio %d (a ratio, not dB). Shannon capacity in bps?" % (B, snr), int(B * math.log2(1 + snr)), "C = B·log₂(1 + S/N).")
    if kind == "snr":
        db = r.choice([10, 20, 30])
        return nat(r, "A telephone line with bandwidth %d Hz has SNR %d dB. Using Shannon's formula (take 10^(dB/10) exactly), capacity in bps, rounded to the nearest integer?" % (B, db), round(B * math.log2(1 + 10 ** (db / 10))), "SNR ratio = %d ⇒ C = B log₂(1 + SNR)." % 10 ** (db // 10), tol=1)
    if kind == "tx":
        pkt, rate = r.choice([1000, 1500, 4000, 12000]), r.choice([1, 10, 100]) * 10 ** 6
        return nat(r, "A %d-bit packet is sent on a %d Mbps link. Transmission delay in microseconds?" % (pkt, rate // 10 ** 6), round(pkt / rate * 1e6, 2), "L/R.", tol=0.01)
    if kind == "e2e":
        n, pkt, rate, d = r.randint(2, 5), r.choice([1000, 2000, 8000]), r.choice([1, 2, 10]) * 10 ** 6, r.choice([1, 2, 5])
        t = n * (pkt / rate * 1000) + n * d
        return nat(r, "A single %d-bit packet crosses %d identical store-and-forward links, each of rate %d Mbps and propagation delay %d ms (ignore queuing and processing). End-to-end delay in ms? (up to 2 decimals)" % (pkt, n, rate // 10 ** 6, d), round(t, 2), "n·(L/R + d).", tol=0.01)
    if kind == "bdp":
        rate, rtt = r.choice([1, 10, 100, 1000]), r.choice([10, 20, 50, 100, 200])
        return nat(r, "A link has bandwidth %d Mbps and round-trip time %d ms. Bandwidth-delay product in kilobits?" % (rate, rtt), rate * rtt, "Mbps × ms = kb.")
    if kind == "pipe":
        n, pk, pkt, rate = r.randint(2, 4), r.randint(3, 10), 1000, 10 ** 6
        return nat(r, "%d packets of %d bits are sent back-to-back over %d store-and-forward links of rate 1 Mbps each (zero propagation delay). Time (ms) until the LAST packet is fully received at the destination?" % (pk, pkt, n), (n + pk - 1) * pkt / rate * 1000, "(links + packets − 1) × transmission time.")
    if kind == "levels": return nat(r, "A signal with %d levels carries how many bits per signal element?" % (2 ** int(math.log2(L))), math.log2(L), "log₂ L.")
    if kind == "overhead":
        pay, hdr = r.choice([1000, 1460, 512]), r.choice([40, 58, 20])
        return nat(r, "A packet carries %d bytes of payload with %d bytes of headers. Protocol efficiency in percent? (up to 2 decimals)" % (pay, hdr), round(pay / (pay + hdr) * 100, 2), "payload / total.", tol=0.01)
    rate = r.choice([1, 2, 10]) * 10 ** 6
    return nat(r, "A source sends 1000-bit frames over a %d Mbps link with one-way propagation delay 5 ms using stop-and-wait (ack time negligible). Link utilisation in percent? (up to 2 decimals)" % (rate // 10 ** 6), round((1000 / rate) / (1000 / rate + 2 * 0.005) * 100, 2), "U = Tt / (Tt + 2·Tp).", tol=0.01)


# ---------------- data link ----------------
def crc_rem(data, gen):
    d = list(map(int, data + "0" * (len(gen) - 1)))
    g = list(map(int, gen))
    for i in range(len(data)):
        if d[i]:
            for j in range(len(g)): d[i + j] ^= g[j]
    return "".join(map(str, d[-(len(gen) - 1):]))


@gen(S, DL, "CRC", n=100, diff="medium", marks=2)
def dl_crc(r):
    gens = ["1011", "10011", "1101", "100101", "11001"]
    g = r.choice(gens)
    data = "".join(r.choice("01") for _ in range(r.randint(6, 11)))
    rem = crc_rem(data, g)
    kind = r.choice(["rem", "frame", "bits"])
    if kind == "rem": return mcq(r, "A CRC uses generator polynomial bits %s. The data word is %s. The CRC remainder (check bits) appended is" % (g, data), rem, [format((int(rem, 2) + k) % 2 ** len(rem), "0%db" % len(rem)) for k in (1, 2, 3, 5)] + [rem[::-1]], "Append %d zeros and divide modulo 2." % (len(g) - 1))
    if kind == "frame": return mcq(r, "Data %s is sent with a CRC using generator %s. The transmitted frame is" % (data, g), data + rem, [data + format((int(rem, 2) + 1) % 2 ** len(rem), "0%db" % len(rem)), data + rem[::-1], rem + data, data + "0" * len(rem)], "Frame = data followed by remainder.")
    return nat(r, "A CRC generator polynomial has degree %d. How many check bits are appended to the frame?" % (len(g) - 1), len(g) - 1, "Degree of the generator.")


@gen(S, DL, "Error detection & Hamming", n=90, diff="medium")
def dl_err(r):
    kind = r.choice(["hamming_r", "dist_det", "dist_cor", "parity", "ham_cw", "min_dist", "checksum"])
    m = r.choice([4, 7, 8, 11, 16, 26, 32, 57, 64])
    d = r.randint(3, 11)
    if kind == "hamming_r":
        rr = 1
        while 2 ** rr < m + rr + 1: rr += 1
        return nat(r, "Minimum number of check bits needed in a single-error-correcting Hamming code for %d data bits?" % m, rr, "Smallest r with 2^r ≥ m + r + 1.")
    if kind == "dist_det": return nat(r, "A code has minimum Hamming distance %d. Maximum number of bit errors it is GUARANTEED to detect?" % d, d - 1, "d − 1.")
    if kind == "dist_cor": return nat(r, "A code has minimum Hamming distance %d. Maximum number of bit errors it is GUARANTEED to correct?" % d, (d - 1) // 2, "⌊(d − 1)/2⌋.")
    if kind == "parity":
        v = r.randint(1, 255)
        return nat(r, "Even parity is used on the 8-bit data %s. What parity bit (0 or 1) is appended?" % format(v, "08b"), bin(v).count("1") % 2, "The parity bit makes the total number of 1s even.")
    if kind == "ham_cw":
        a, b = r.randint(0, 255), r.randint(0, 255)
        return nat(r, "Hamming distance between the bit patterns %s and %s?" % (format(a, "08b"), format(b, "08b")), bin(a ^ b).count("1"), "Number of differing positions.")
    if kind == "min_dist":
        words = r.sample(range(0, 64), 4)
        return nat(r, "Codewords: %s. What is the minimum Hamming distance of the code?" % [format(w, "06b") for w in words], min(bin(a ^ b).count("1") for i, a in enumerate(words) for b in words[i + 1:]), "Check all pairs.")
    words = [r.randint(0x1000, 0xFFFF) for _ in range(r.randint(2, 3))]
    s = 0
    for w in words:
        s += w
        s = (s & 0xFFFF) + (s >> 16)
    return nat(r, "Internet checksum: 16-bit words %s (hex). What is the 16-bit ones'-complement checksum, as a decimal number?" % [format(w, "04X") for w in words], (~s) & 0xFFFF, "Ones'-complement sum = %04X; checksum = its complement." % s)


@gen(S, DL, "Sliding window", n=110, diff="medium")
def dl_win(r):
    kind = r.choice(["gbn", "sr", "seqbits", "opt", "util", "sw_eff", "gbn_re"])
    k = r.randint(2, 8)
    a = r.choice([1, 2, 4, 9, 19, 49])
    if kind == "gbn": return nat(r, "Go-Back-N ARQ uses %d-bit sequence numbers. Maximum sender window size?" % k, 2 ** k - 1, "2^k − 1.")
    if kind == "sr": return nat(r, "Selective Repeat ARQ uses %d-bit sequence numbers. Maximum sender window size?" % k, 2 ** (k - 1), "2^(k−1).")
    if kind == "seqbits":
        w = r.choice([7, 15, 31, 63, 127])
        return nat(r, "Go-Back-N with a window of %d frames needs at least how many bits for the sequence number?" % w, math.ceil(math.log2(w + 1)), "Need 2^k ≥ W + 1.")
    if kind == "opt":
        tt, tp = r.choice([1, 2, 5]), r.choice([5, 10, 20, 50])
        return nat(r, "Frame transmission time is %d ms, one-way propagation delay %d ms (ack time negligible). Minimum window size (frames) to keep the sender busy continuously?" % (tt, tp), 1 + math.ceil(2 * tp / tt), "W = 1 + 2·Tp/Tt.")
    if kind == "util":
        w = r.choice([1, 2, 4, 8, 16, 32])
        return nat(r, "A sliding-window protocol has window size %d and a ratio a = Tp/Tt = %d. Channel utilisation in percent? (up to 2 decimals; cap at 100)" % (w, a), round(min(1, w / (1 + 2 * a)) * 100, 2), "U = min(1, W/(1 + 2a)).", tol=0.01)
    if kind == "sw_eff":
        tt, tp = r.choice([1, 2, 4]), r.choice([5, 10, 20])
        return nat(r, "Stop-and-wait: Tt = %d ms, one-way Tp = %d ms. Efficiency in percent? (up to 2 decimals)" % (tt, tp), round(tt / (tt + 2 * tp) * 100, 2), "Tt / (Tt + 2Tp).", tol=0.01)
    n = r.randint(8, 30)
    return nat(r, "In Go-Back-N with window size %d, frame number %d is lost while frames up to %d were already sent. How many frames are retransmitted in total (frame %d onward up to frame %d)?" % (r.choice([4, 7, 8]), n, n + 3, n, n + 3), 4, "Frames n … n+3 are all resent.")


@gen(S, DL, "Framing", n=60, diff="easy")
def dl_frame(r):
    kind = r.choice(["stuff", "charstuff"])
    bits = "".join(r.choice("0111") for _ in range(r.randint(10, 22)))
    out, run = "", 0
    for b in bits:
        out += b
        run = run + 1 if b == "1" else 0
        if run == 5: out += "0"; run = 0
    return nat(r, "Bit stuffing inserts a 0 after every five consecutive 1s in the data. The data bits are %s. What is the length of the stuffed data (bits)?" % bits, len(out), "Stuffed: %s." % out)


# ---------------- MAC ----------------
@gen(S, MC, "Ethernet & ALOHA", n=110, diff="medium")
def mc_eth(r):
    kind = r.choice(["minframe", "slot", "pure", "slotted", "maxpure", "backoff", "eff", "tokens", "collision"])
    rate, d, v = r.choice([10, 100, 1000]), r.choice([500, 1000, 2000, 2500]), 2 * 10 ** 8
    if kind == "minframe":
        return nat(r, "CSMA/CD on a %d Mbps LAN with maximum distance %d m between stations and signal speed 2×10^8 m/s (ignore jam and repeater delays). Minimum frame size in bits?" % (rate, d), round(2 * d / v * rate * 10 ** 6), "L_min = 2·Tp·R.", tol=1)
    if kind == "slot": return nat(r, "Round-trip propagation time (slot time) in µs for a segment of %d m with signal speed 2×10^8 m/s? (up to 2 decimals)" % d, round(2 * d / v * 1e6, 2), "2d/v.", tol=0.01)
    G = r.choice([0.25, 0.5, 1.0, 1.5])
    if kind == "pure": return nat(r, "Pure ALOHA: offered load G = %g frames per frame-time. Throughput S = G·e^(−2G). (up to 4 decimals)" % G, round(G * math.exp(-2 * G), 4), "Substitute G.", tol=0.0006)
    if kind == "slotted": return nat(r, "Slotted ALOHA: offered load G = %g. Throughput S = G·e^(−G). (up to 4 decimals)" % G, round(G * math.exp(-G), 4), "Substitute G.", tol=0.0006)
    if kind == "maxpure": return mcq(r, "Maximum throughput (efficiency) of pure ALOHA and slotted ALOHA respectively is approximately", "18.4% and 36.8%", ["36.8% and 18.4%", "50% and 100%", "25% and 50%"], "Pure: 1/(2e); slotted: 1/e.")
    if kind == "backoff":
        n = r.randint(1, 6)
        return nat(r, "In Ethernet's binary exponential backoff, after the %d-th consecutive collision a station picks a random number from 0 to 2^%d − 1. How many different values can it pick?" % (n, n), 2 ** n, "2^n choices.")
    if kind == "eff":
        a = r.choice([0.1, 0.2, 0.5])
        return nat(r, "CSMA/CD efficiency can be approximated as 1/(1 + 6.44a) where a = Tp/Tt. For a = %g the efficiency in percent is (up to 2 decimals)" % a, round(100 / (1 + 6.44 * a), 2), "Substitute a.", tol=0.01)
    if kind == "tokens":
        n, a = r.randint(5, 20), r.choice([0.1, 0.5, 2])
        return nat(r, "A token ring has %d stations. A station may send one frame per token capture. Frame transmission time 1 unit, ring latency %g units (one token pass per station is negligible). Maximum efficiency with delayed token release is 1/(1 + a) in percent? (a = %g, up to 2 decimals)" % (n, a, a), round(100 / (1 + a), 2), "1/(1 + a).", tol=0.01)
    return nat(r, "In Ethernet, a frame has a 14-byte header, 4-byte FCS and a 46-byte minimum payload. Minimum Ethernet frame length in bytes (excluding preamble)?", 64, "14 + 46 + 4.")


@gen(S, MC, "LAN facts", n=40, diff="easy")
def mc_facts(r):
    return r.choice([
        mcq(r, "A switch operating at the data link layer forwards frames using", "MAC addresses", ["IP addresses", "port numbers", "DNS names"], "Layer-2 devices use MAC addresses."),
        mcq(r, "The number of collision domains created by an N-port switch (each port connected to one host) is", "N", ["1", "N − 1", "2"], "Each switch port is its own collision domain."),
        mcq(r, "A hub operates at which layer of the OSI model?", "Physical layer", ["Data link layer", "Network layer", "Transport layer"], "Hubs just regenerate bits."),
        mcq(r, "The size of an Ethernet MAC address is", "48 bits", ["32 bits", "64 bits", "128 bits"], "6 bytes."),
        mcq(r, "CSMA/CA (used in 802.11) differs from CSMA/CD mainly because wireless stations", "cannot reliably detect collisions while transmitting", ["do not use carrier sensing", "use token passing", "transmit with higher power"], "Collision avoidance is used instead."),
        mcq(r, "A bridge learns the location of hosts by examining the", "source MAC address of incoming frames", ["destination IP address", "TTL field", "TCP port"], "Backward learning."),
    ])


# ---------------- IP ----------------
@gen(S, IP, "Subnetting", n=150, diff="easy")
def ip_sub(r):
    prefix = r.choice([8, 12, 16, 20, 22, 24, 25, 26, 27, 28, 29, 30])
    ip = ".".join(str(r.randint(1, 223)) for _ in range(4))
    net = ipaddress.ip_network("%s/%d" % (ip, prefix), strict=False)
    kind = r.choice(["hosts", "mask", "netaddr", "bcast", "nsub", "same", "lastoctet", "firsthost"])
    if kind == "hosts": return nat(r, "How many usable host addresses are there in a /%d IPv4 subnet?" % prefix, 2 ** (32 - prefix) - 2, "2^(32−%d) − 2." % prefix)
    if kind == "mask":
        m = str(net.netmask)
        octets = [x for x in m.split(".")]
        return mcq(r, "The dotted-decimal subnet mask for prefix length /%d is" % prefix, m, [str(ipaddress.ip_network("0.0.0.0/%d" % p).netmask) for p in (prefix - 1, prefix + 1, prefix + 2, prefix - 2) if 1 <= p <= 31], "First %d bits are 1." % prefix)
    if kind == "netaddr": return mcq(r, "The network address of host %s/%d is" % (ip, prefix), str(net.network_address), [str(ipaddress.ip_address(int(net.network_address) + d)) for d in (1, 2 ** (32 - prefix) // 2 if prefix < 31 else 1, -(2 ** (32 - prefix)) if int(net.network_address) > 2 ** (32 - prefix) else 4)] + [ip], "AND the address with the mask.")
    if kind == "bcast": return mcq(r, "The broadcast address of the subnet containing %s/%d is" % (ip, prefix), str(net.broadcast_address), [str(net.network_address), str(ipaddress.ip_address(int(net.broadcast_address) - 1)), str(ipaddress.ip_address(int(net.broadcast_address) + 1)), ip], "Set all host bits to 1.")
    if kind == "nsub":
        b = r.randint(1, 5)
        base = r.choice([16, 20, 24])
        return nat(r, "A /%d network is split into equal subnets by borrowing %d additional bits. How many subnets (counting all subnets, including all-zeros/all-ones)?" % (base, b), 2 ** b, "2^b.")
    if kind == "same":
        a = int(net.network_address) + r.randint(1, max(1, 2 ** (32 - prefix) - 2))
        other = a ^ (1 << r.randint(0, 31))
        same = ipaddress.ip_address(other) in net
        return mcq(r, "Are hosts %s and %s in the same subnet when the mask is /%d?" % (ipaddress.ip_address(a), ipaddress.ip_address(other), prefix), "Yes" if ipaddress.ip_address(a) in net and same else "No", ["No" if same else "Yes", "Only if they have the same class", "Only through a router"], "Compare network prefixes.") if (ipaddress.ip_address(a) in net) else (_ for _ in ()).throw(Skip())
    if kind == "lastoctet":
        host = int(net.broadcast_address) % 256
        return nat(r, "The last octet of the broadcast address of %s/%d is" % (ip, prefix), host, "Broadcast = %s." % net.broadcast_address)
    return mcq(r, "The first usable host address in the subnet of %s/%d is" % (ip, prefix), str(net.network_address + 1), [str(net.network_address), str(net.network_address + 2), str(net.broadcast_address), ip], "Network address + 1.")


@gen(S, IP, "CIDR & VLSM", n=100, diff="hard", marks=2)
def ip_cidr(r):
    kind = r.choice(["agg", "count", "vlsm", "class", "supernet", "route"])
    if kind == "agg":
        k = r.choice([2, 4, 8, 16])
        third, a_, b_ = r.randrange(0, 256, k), r.randint(10, 200), r.randint(0, 255)
        blocks = [ipaddress.ip_network("%d.%d.%d.0/24" % (a_, b_, third + i)) for i in range(k)]
        agg = list(ipaddress.collapse_addresses(blocks))
        return nat(r, "The %d contiguous /24 networks %s … %s are aggregated into a single summary route. What is its prefix length?" % (k, blocks[0], blocks[-1]), agg[0].prefixlen, "Summary route: %s." % agg[0])
    if kind == "count":
        p, q = r.choice([16, 20, 22]), r.choice([24, 26, 28, 30])
        return nat(r, "How many /%d subnets fit into a /%d block?" % (q, p), 2 ** (q - p), "2^(q−p).")
    if kind == "vlsm":
        hosts = sorted([r.choice([2, 5, 10, 20, 30, 50, 60, 100, 120]) for _ in range(r.randint(3, 4))], reverse=True)
        need = sum(2 ** math.ceil(math.log2(h + 2)) for h in hosts)
        return nat(r, "Using VLSM, subnets are needed for LANs with %s hosts. What is the minimum total number of IP addresses consumed (each subnet sized to the next power of two that holds hosts + 2)?" % hosts, need, "Sum of 2^⌈log₂(h + 2)⌉.")
    if kind == "class":
        o = r.randint(1, 255)
        c = "A" if o < 128 else "B" if o < 192 else "C" if o < 224 else "D" if o < 240 else "E"
        return mcq(r, "An IPv4 address begins with the first octet %d. It belongs to class" % o, c, [x for x in "ABCDE" if x != c][:3], "Class by leading bits: A < 128, B < 192, C < 224, D < 240.")
    if kind == "supernet":
        k = r.randint(2, 6)
        return nat(r, "A company needs %d Class C-sized (/24) networks as one contiguous CIDR block. What is the smallest number of /24 networks that block must contain (a power of two)?" % (2 ** k - 1), 2 ** k, "Round up to a power of two.")
    routes = [("0.0.0.0/0", "R0"), ("10.0.0.0/8", "R1"), ("10.1.0.0/16", "R2"), ("10.1.2.0/24", "R3"), ("10.1.2.128/25", "R4")]
    dst = r.choice(["10.1.2.200", "10.1.2.5", "10.1.9.1", "10.9.9.9", "11.1.1.1"])
    best = max((ipaddress.ip_network(n) for n, _ in routes if ipaddress.ip_address(dst) in ipaddress.ip_network(n)), key=lambda x: x.prefixlen)
    nh = dict(routes)[str(best)]
    return mcq(r, "A router has routes: " + ", ".join("%s → %s" % x for x in routes) + ". A packet for %s is forwarded to (longest-prefix match)" % dst, nh, [v for _, v in routes if v != nh][:3], "Match: %s." % best)


@gen(S, IP, "Fragmentation", n=100, diff="medium", marks=2)
def ip_frag(r):
    pay, mtu = r.choice([1000, 2000, 3000, 4000, 5000, 6000, 8000]), r.choice([576, 1000, 1500])
    per = (mtu - 20) // 8 * 8
    n = math.ceil(pay / per)
    kind = r.choice(["n", "last", "offset", "total"])
    ctx = "An IP datagram has a 20-byte header and %d bytes of data and must cross a link with MTU %d bytes." % (pay, mtu)
    if kind == "n": return nat(r, ctx + " Number of fragments produced?", n, "Each fragment carries ⌊(MTU − 20)/8⌋·8 = %d data bytes ⇒ ⌈%d/%d⌉." % (per, pay, per))
    if kind == "last": return nat(r, ctx + " Size (header + data, in bytes) of the LAST fragment?", 20 + pay - (n - 1) * per, "Remaining data %d + 20 header." % (pay - (n - 1) * per))
    if kind == "offset": return nat(r, ctx + " What is the fragment-offset field value (in units of 8 bytes) of the last fragment?", (n - 1) * per // 8, "Offset = bytes before it / 8.")
    return nat(r, ctx + " Total bytes transmitted on the link including all headers?", pay + 20 * n, "data + 20 per fragment.")


@gen(S, IP, "Protocol facts", n=50, diff="easy")
def ip_facts(r):
    return r.choice([
        mcq(r, "The size of an IPv6 address is", "128 bits", ["32 bits", "64 bits", "256 bits"], "IPv6 uses 128-bit addresses."),
        mcq(r, "ARP is used to map a", "IP address to a MAC address", ["MAC address to an IP address", "domain name to an IP address", "port number to a process"], "Address Resolution Protocol."),
        mcq(r, "DHCP uses which transport protocol and server port?", "UDP port 67", ["TCP port 67", "UDP port 53", "TCP port 80"], "DHCP server listens on UDP/67 (client on 68)."),
        mcq(r, "The TTL field in an IPv4 header is decremented by", "each router that forwards the packet", ["each switch", "the sender every second", "the receiver on delivery"], "Prevents infinite loops."),
        mcq(r, "ICMP is used for", "error reporting and diagnostics (e.g., ping)", ["address assignment", "name resolution", "reliable delivery"], "Internet Control Message Protocol."),
        mcq(r, "Network Address Translation (NAT) primarily helps to", "share one public IPv4 address among many private hosts", ["encrypt traffic", "speed up routing", "assign MAC addresses"], "Port address translation."),
        mcq(r, "The minimum size of an IPv4 header (no options) is", "20 bytes", ["8 bytes", "40 bytes", "60 bytes"], "IHL = 5 words."),
        mcq(r, "Private IPv4 address ranges include", "10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16", ["1.0.0.0/8, 100.0.0.0/8", "11.0.0.0/8, 172.0.0.0/8", "169.254.0.0/16 only"], "RFC 1918."),
    ])


# ---------------- routing ----------------
def rt_graph(r, n):
    e = {}
    nodes = list(range(n)); r.shuffle(nodes)
    for i in range(1, n): e[tuple(sorted((nodes[i], nodes[r.randrange(i)])))] = r.randint(1, 9)
    for _ in range(r.randint(2, 4)):
        a, b = r.sample(range(n), 2); e.setdefault(tuple(sorted((a, b))), r.randint(1, 9))
    return [(a, b, w) for (a, b), w in sorted(e.items())]


def dijk(n, edges, s):
    adj = {i: [] for i in range(n)}
    for a, b, w in edges: adj[a].append((b, w)); adj[b].append((a, w))
    d, pq = {s: 0}, [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]: continue
        for v, w in adj[u]:
            if du + w < d.get(v, 10 ** 9): d[v] = du + w; heapq.heappush(pq, (d[v], v))
    return d


def dv_rounds(n, edges):
    INF = 10 ** 9
    D = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges: D[a][b] = D[b][a] = w
    rounds, ch = 0, True
    while ch:
        ch = False
        new = [row[:] for row in D]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if D[i][k] < INF and D[k][j] < INF and D[i][k] + D[k][j] < new[i][j] and (D[i][k] == next((w for a, b, w in edges if {a, b} == {i, k}), -1)):
                        new[i][j] = D[i][k] + D[k][j]; ch = True
        D = new
        if ch: rounds += 1
    return rounds, D


@gen(S, RT, "Shortest paths", n=100, diff="medium")
def rt_ls(r):
    n = r.randint(5, 6)
    e = rt_graph(r, n)
    d = dijk(n, e, 0)
    t = r.randint(2, n - 1)
    es = ", ".join("%s%s:%d" % (chr(65 + a), chr(65 + b), w) for a, b, w in e)
    kind = r.choice(["cost", "sum"])
    ctx = "A network has routers A–%s and links (cost): %s. Link-state routing computes shortest paths from A with Dijkstra." % (chr(64 + n), es)
    if kind == "cost": return nat(r, ctx + " Cost of the least-cost path from A to %s?" % chr(65 + t), d[t], "Dijkstra from A: %s." % {chr(65 + k): v for k, v in sorted(d.items())})
    return nat(r, ctx + " Sum of the least costs from A to all other routers?", sum(v for k, v in d.items() if k != 0), "Distances: %s." % {chr(65 + k): v for k, v in sorted(d.items())})


@gen(S, RT, "Distance vector", n=60, diff="hard", marks=2)
def rt_dv(r):
    n = r.randint(4, 6)
    e = rt_graph(r, n)
    kind = r.choice(["bf", "inf", "rip", "msgs"])
    if kind == "bf":
        k = r.randint(1, 3)
        INF = 10 ** 9
        dist = [INF] * n; dist[0] = 0
        for _ in range(k):
            nd = list(dist)
            for a, b, w in e:
                if dist[a] + w < nd[b]: nd[b] = dist[a] + w
                if dist[b] + w < nd[a]: nd[a] = dist[b] + w
            dist = nd
        t = r.randint(1, n - 1)
        if dist[t] >= INF: raise Skip()
        es = ", ".join("%s%s:%d" % (chr(65 + a), chr(65 + b), w) for a, b, w in e)
        return nat(r, "Bellman–Ford / distance-vector computation toward destination A runs synchronously. Links: %s. Initially only A knows distance 0 to itself. After %d round(s) of exchanges (each node updates using neighbours' previous-round values), what distance does node %s hold to A?" % (es, k, chr(65 + t)), dist[t], "Each round extends paths by one hop.")
    if kind == "inf":
        s0, st = r.choice([1, 2, 3]), r.choice([2, 3, 4, 5])
        return nat(r, "In a count-to-infinity scenario each exchange raises a bogus route metric by %d, starting from %d. With infinity defined as 16, after how many exchanges does the metric first reach or exceed 16?" % (st, s0), math.ceil((16 - s0) / st), "⌈(16 − start)/step⌉.")
    if kind == "rip": return mcq(r, "RIP uses which metric and what is its maximum valid value?", "Hop count, 15", ["Bandwidth, 255", "Delay, 1024", "Hop count, 255"], "Hop count with infinity = 16.")
    m, deg = r.randint(4, 12), r.randint(2, 5)
    return nat(r, "In a network with %d routers each directly connected to %d neighbours, every router sends its full distance vector to each neighbour once per update round. How many vector messages are sent in one round?" % (m, deg), m * deg, "routers × neighbours.")


# ---------------- transport ----------------
def tcp_cwnd(ssthresh, rtts, loss_at=None):
    cw, ss, hist = 1, ssthresh, []
    for t in range(1, rtts + 1):
        hist.append(cw)
        if loss_at and t == loss_at:
            ss = max(cw // 2, 2); cw = 1
        else:
            cw = min(cw * 2, ss) if cw < ss else cw + 1
    return hist


@gen(S, TP, "TCP congestion control", n=120, diff="hard", marks=2)
def tp_cc(r):
    ss = r.choice([8, 16, 32, 64])
    n = r.randint(6, 14)
    loss = r.choice([None, None, r.randint(4, n - 1)])
    h = tcp_cwnd(ss, n, loss)
    q = r.choice(["at", "sum"])
    desc = "TCP Tahoe: initial cwnd = 1 MSS, ssthresh = %d MSS. Slow start doubles cwnd each RTT until it reaches ssthresh, then congestion avoidance adds 1 MSS per RTT.%s" % (ss, " At the end of RTT %d a timeout occurs: ssthresh = max(cwnd/2, 2) and cwnd = 1." % loss if loss else "")
    if q == "at": return nat(r, desc + " Transmission round numbering starts at 1 (cwnd = 1 in round 1). What is cwnd (in MSS) during transmission round %d?" % n, h[-1], "cwnd per round: %s." % h)
    return nat(r, desc + " Total segments sent in the first %d rounds (one cwnd's worth per round)?" % n, sum(h), "cwnd per round: %s." % h)


@gen(S, TP, "TCP performance", n=100, diff="medium")
def tp_perf(r):
    kind = r.choice(["rtt", "window", "wrap", "seg", "eff", "tput", "isn"])
    if kind == "rtt":
        est, samp = r.choice([100, 120, 200]), r.choice([140, 160, 200, 240, 80])
        return nat(r, "TCP's EstimatedRTT is updated as EstimatedRTT = 0.875·EstimatedRTT + 0.125·SampleRTT. If EstimatedRTT = %d ms and a new SampleRTT of %d ms arrives, the new EstimatedRTT in ms is (up to 3 decimals)" % (est, samp), round(0.875 * est + 0.125 * samp, 3), "Weighted average.", tol=0.001)
    if kind == "window":
        rate, rtt = r.choice([10, 100, 1000]), r.choice([10, 20, 50, 100])
        return nat(r, "A TCP connection runs over a %d Mbps path with RTT %d ms. Minimum window size (in kilobytes, 1 KB = 1000 B) to keep the pipe full? (up to 2 decimals)" % (rate, rtt), round(rate * 10 ** 6 / 8 * rtt / 1000 / 1000, 2), "W = bandwidth × RTT.", tol=0.01)
    if kind == "wrap":
        rate = r.choice([10, 100, 1000])
        return nat(r, "TCP sequence numbers are 32 bits and count bytes. A sender transmits at %d Mbps continuously. Time (in seconds) for the sequence space to wrap around? (up to 2 decimals)" % rate, round(2 ** 32 * 8 / (rate * 10 ** 6), 2), "2^32 bytes ÷ rate.", tol=0.01)
    if kind == "seg":
        f, mss = r.choice([10 ** 6, 5 * 10 ** 5, 2 * 10 ** 6]), r.choice([500, 1000, 1460])
        return nat(r, "A %d-byte file is sent over TCP with an MSS of %d bytes. Number of segments needed?" % (f, mss), math.ceil(f / mss), "⌈file/MSS⌉.")
    if kind == "eff":
        pay, hdr = r.choice([1000, 1460, 500]), 40
        return nat(r, "TCP segments carry %d bytes of data with 20-byte TCP and 20-byte IP headers. Header overhead as a percentage of the packet? (up to 2 decimals)" % pay, round(hdr / (pay + hdr) * 100, 2), "40/(data + 40).", tol=0.01)
    if kind == "tput":
        w, rtt, link = r.choice([16, 32, 64, 128]), r.choice([10, 20, 50, 100]), r.choice([10, 100, 1000])
        return nat(r, "A TCP sender has a fixed window of %d KB (1 KB = 1024 B), RTT %d ms and the link is %d Mbps. Maximum throughput in Mbps? (up to 2 decimals)" % (w, rtt, link), round(min(link, w * 1024 * 8 / (rtt / 1000) / 1e6), 2), "min(W/RTT, link rate).", tol=0.01)
    return mcq(r, "The TCP three-way handshake consists of", "SYN, SYN+ACK, ACK", ["SYN, ACK, FIN", "SYN, SYN, ACK", "ACK, SYN+ACK, FIN"], "Connection establishment.")


@gen(S, TP, "UDP & ports", n=30, diff="easy")
def tp_udp(r):
    return r.choice([
        mcq(r, "The UDP header is", "8 bytes long", ["20 bytes long", "12 bytes long", "40 bytes long"], "Source port, destination port, length, checksum (2 bytes each)."),
        mcq(r, "Which of these services typically uses UDP?", "DNS queries", ["SMTP", "HTTP/1.1", "FTP control"], "DNS queries use UDP/53."),
        mcq(r, "A socket address consists of", "IP address and port number", ["MAC address and IP address", "protocol and MAC address", "hostname and MTU"], "Endpoint identification."),
        (lambda L: nat(r, "A UDP datagram has a length field value of %d bytes (header + data). How many bytes of application data does it carry?" % L, L - 8, "Subtract the 8-byte header."))(r.randint(20, 1500)),
        mcq(r, "TCP provides flow control using", "the receiver's advertised window", ["the sender's congestion window only", "ICMP source quench", "IP fragmentation"], "rwnd."),
        mcq(r, "The size of a TCP port number field is", "16 bits", ["8 bits", "32 bits", "12 bits"], "Ports range from 0 to 65535."),
    ])


# ---------------- application & security ----------------
@gen(S, AP, "HTTP response time", n=80, diff="medium")
def ap_http(r):
    rtt, n, tt = r.choice([20, 50, 100]), r.randint(2, 10), r.choice([0, 5, 10])
    kind = r.choice(["nonpers", "pers", "pers_pipe", "parallel"])
    if kind == "nonpers": return nat(r, "A web page has 1 base HTML file and %d small embedded objects on the same server. HTTP/1.0 non-persistent, no parallel connections. RTT = %d ms; object transmission time is negligible. Total time (ms) to fetch everything?" % (n, rtt), (n + 1) * 2 * rtt, "Each object: 1 RTT for TCP setup + 1 RTT for request/response.")
    if kind == "pers": return nat(r, "Same page (base + %d objects) with HTTP/1.1 persistent connections WITHOUT pipelining, RTT = %d ms, negligible transmission times. Total time (ms)?" % (n, rtt), rtt + (n + 1) * rtt, "1 RTT handshake + 1 RTT per object.")
    if kind == "pers_pipe": return nat(r, "Same page (base + %d objects) with HTTP/1.1 persistent connections WITH pipelining (all embedded requests sent together after the base file arrives), RTT = %d ms, negligible transmission times. Total time (ms)?" % (n, rtt), rtt + rtt + rtt, "Handshake + base file + one RTT for all embedded objects.")
    k = r.choice([2, 3, 4, 5])
    return nat(r, "A page has 1 base file and %d embedded objects. Non-persistent HTTP with up to %d parallel connections for embedded objects (RTT = %d ms, negligible transmission). Total time (ms)?" % (n, k, rtt), 2 * rtt + 2 * rtt * math.ceil(n / k), "Base: 2 RTT; then ⌈n/k⌉ batches of 2 RTT.")


@gen(S, AP, "Cryptography arithmetic", n=120, diff="hard", marks=2)
def ap_crypto(r):
    primes = [3, 5, 7, 11, 13, 17, 19, 23]
    kind = r.choice(["rsa_d", "rsa_enc", "rsa_n", "dh", "keys", "caesar", "rsa_phi"])
    if kind in ("rsa_d", "rsa_enc", "rsa_n", "rsa_phi"):
        p, q = r.sample(primes, 2)
        n, ph = p * q, (p - 1) * (q - 1)
        es = [e for e in range(3, ph) if math.gcd(e, ph) == 1]
        e = r.choice(es[:6])
        d = pow(e, -1, ph)
        m = r.randint(2, n - 1)
        if kind == "rsa_phi": return nat(r, "In RSA, p = %d and q = %d. What is φ(n)?" % (p, q), ph, "(p−1)(q−1).")
        if kind == "rsa_n": return nat(r, "In RSA, p = %d, q = %d. What is the modulus n?" % (p, q), n, "n = p·q.")
        if kind == "rsa_d": return nat(r, "In RSA with p = %d, q = %d and public exponent e = %d, the private exponent d (with 1 < d < φ(n)) is" % (p, q, e), d, "d = e⁻¹ mod φ(n) = %d." % d)
        return nat(r, "RSA public key (e = %d, n = %d). Encrypt the plaintext m = %d: ciphertext c = m^e mod n =" % (e, n, m), pow(m, e, n), "Modular exponentiation.")
    if kind == "dh":
        p, g = r.choice([(23, 5), (19, 2), (17, 3), (11, 2), (13, 2)])
        a, b = r.randint(2, 9), r.randint(2, 9)
        return nat(r, "Diffie–Hellman with public prime p = %d and generator g = %d. Alice's secret is a = %d and Bob's is b = %d. The shared secret key is" % (p, g, a, b), pow(pow(g, a, p), b, p), "g^(ab) mod p.")
    if kind == "keys":
        n = r.randint(5, 60)
        return nat(r, "In a network of %d users, every pair needs a distinct shared secret key (symmetric cryptography). How many keys are required in total?" % n, n * (n - 1) // 2, "n(n−1)/2.")
    k, m = r.randint(1, 25), r.choice(["GATE", "CODE", "HELLO", "CRYPTO", "TRAIN"])
    c = "".join(chr((ord(x) - 65 + k) % 26 + 65) for x in m)
    return mcq(r, "A Caesar cipher shifts every letter forward by %d. The ciphertext of %s is" % (k, m), c, ["".join(chr((ord(x) - 65 - k) % 26 + 65) for x in m), "".join(chr((ord(x) - 65 + k + 1) % 26 + 65) for x in m), m[::-1], "".join(chr((ord(x) - 65 + 2 * k) % 26 + 65) for x in m)], "Shift each letter by %d modulo 26." % k)


@gen(S, AP, "Protocol facts", n=60, diff="easy")
def ap_facts(r):
    return r.choice([
        mcq(r, "Which port does HTTPS use by default?", "443", ["80", "25", "8080"], "TLS over TCP/443."),
        mcq(r, "SMTP is used to", "send (push) email between mail servers", ["download email to a client", "resolve domain names", "transfer web pages"], "POP3/IMAP retrieve mail."),
        mcq(r, "The default port numbers for HTTP, SMTP and DNS are respectively", "80, 25, 53", ["25, 80, 53", "80, 110, 53", "443, 25, 53"], "Well-known ports."),
        mcq(r, "A DNS resolver asks the root, then the TLD, then the authoritative server in turn. This type of query is", "iterative", ["recursive", "broadcast", "multicast"], "Each server returns a referral."),
        mcq(r, "FTP uses two TCP connections: a control connection and a data connection. The control connection uses port", "21", ["20", "22", "23"], "FTP control: 21; active-mode data: 20."),
        mcq(r, "A digital signature provides", "authentication, integrity and non-repudiation", ["confidentiality only", "availability", "compression"], "Signing with the private key."),
        mcq(r, "A cryptographic hash function should be", "one-way and collision resistant", ["reversible with the key", "always produce 128 bits irrespective of input", "slow to compute for attackers only"], "Pre-image and collision resistance."),
        mcq(r, "In the TCP/IP model, DNS operates at the", "application layer", ["transport layer", "network layer", "link layer"], "DNS is an application-layer protocol."),
        mcq(r, "Which protocol retrieves email and keeps messages synchronised across devices on the server?", "IMAP", ["POP3", "SMTP", "FTP"], "IMAP stores mail on the server."),
        mcq(r, "A firewall that inspects only packet headers (addresses, ports) is called a", "packet-filtering firewall", ["proxy gateway", "application-level firewall", "honeypot"], "Stateless filter."),
    ])
