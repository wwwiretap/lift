from scapy.all import *

class ssdp_scan:
	def active_scan(self, target):
  		req = 'M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nST:upnp:rootdevice\r\nMan:"ssdp:discover"\r\nMX:3\r\n\r\n'
		ip=IP(dst=target)
  		udp=UDP(sport=random.randint(49152,65536), dport=1900)
  		pck = ip/udp/req
  		try:
   			rep = sr1(pck, verbose=0)
   			results = rep[Raw].load
  		except Exception as e:
   			results = None
		return results

