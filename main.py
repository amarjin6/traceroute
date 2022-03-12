from scapy.layers.inet import traceroute

result, unans = traceroute('8.8.8.8', maxttl=30)
for snd, rcv in result:
    print(snd.ttl, rcv.src, snd.sent_time, rcv.time)
