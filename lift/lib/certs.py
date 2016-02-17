from socket import socket
import ssl
import argparse
import time
import sys

def getcertinfo(certreq):
	certs = { """-----BEGIN CERTIFICATE-----
MIICrTCCAhYCCQC6Ffdh27eytzANBgkqhkiG9w0BAQUFADCBmjELMAkGA1UEBhMC
VVMxCzAJBgNVBAgTAkNBMREwDwYDVQQHEwhTYW4gSm9zZTEfMB0GA1UEChMWVWJp
cXVpdGkgTmV0d29ya3MgSW5jLjEaMBgGA1UECxMRVGVjaG5pY2FsIFN1cHBvcnQx
DTALBgNVBAMTBFVCTlQxHzAdBgkqhkiG9w0BCQEWEHN1cHBvcnRAdWJudC5jb20w
HhcNMTEwNjAyMDgzNTAyWhcNMjAwMTAxMDgzNTAyWjCBmjELMAkGA1UEBhMCVVMx
CzAJBgNVBAgTAkNBMREwDwYDVQQHEwhTYW4gSm9zZTEfMB0GA1UEChMWVWJpcXVp
dGkgTmV0d29ya3MgSW5jLjEaMBgGA1UECxMRVGVjaG5pY2FsIFN1cHBvcnQxDTAL
BgNVBAMTBFVCTlQxHzAdBgkqhkiG9w0BCQEWEHN1cHBvcnRAdWJudC5jb20wgZ8w
DQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAL4JnxQ69+7lisl2siYXAHsMhRyUjr1/
9aGlbQosZMx/eLwR7tzZ5irL4Z7YF6acNaraxcE6pUjcr7yZN1l+iDws07vnYG3j
GflOGExMOv1eNW+jULlQwI6L+qDuxJbFuk7t2PEYBTaJVMLcJ+t1dBy+mkzI5c7+
R0SWp68QB+sVAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAAFoxgToVbTCVjQORR6oj
4rTALtQBzdUha2lePHEnEBz1h9QoGRfCPew2/e6TB48LMGUOKDVsJZ7YJBaFZSna
R98wCYQzLLS0+vAkQLnuHvAcM8PhBnAua/6g0KqBb88bcGdDATKg2ryMqJHzy7GX
MATyxnfoiZcs0x/PA/H8Nvo=
-----END CERTIFICATE-----
""":'ubiquiti',"""-----BEGIN CERTIFICATE-----
MIIErTCCA5WgAwIBAgIJAOpFqhFiNn8rMA0GCSqGSIb3DQEBBQUAMIGVMQswCQYD
VQQGEwJUVzEPMA0GA1UECBMGVGFpd2FuMQ8wDQYDVQQHEwZUYWlwZWkxGzAZBgNV
BAoTElFOQVAgU3lzdGVtcywgSW5jLjEMMAoGA1UECxMDTkFTMRYwFAYDVQQDEw1U
UyBTZXJpZXMgTkFTMSEwHwYJKoZIhvcNAQkBFhJxX3N1cHBvcnRAcW5hcC5jb20w
HhcNMTEwNzA4MTAwOTQ1WhcNMjEwNzA1MTAwOTQ1WjCBlTELMAkGA1UEBhMCVFcx
DzANBgNVBAgTBlRhaXdhbjEPMA0GA1UEBxMGVGFpcGVpMRswGQYDVQQKExJRTkFQ
IFN5c3RlbXMsIEluYy4xDDAKBgNVBAsTA05BUzEWMBQGA1UEAxMNVFMgU2VyaWVz
IE5BUzEhMB8GCSqGSIb3DQEJARYScV9zdXBwb3J0QHFuYXAuY29tMIIBIjANBgkq
hkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAngIqhFfRtB3lv/DmPYp+rMTt6xRQMtv3
aQYczHhgAVQD9XPOZfEfSxNreFnXGaeWRKTCvH0iVhAUFLaFLH4hncrrI027r7D4
l323S4KWy12UrY3JHcLEwNp4uMlMd713dkSnh967ZY1Coml34f68+KijLe57vlxZ
jpK8A0KCdBwwGDojFoR0hoNmjVZJard8xvvSv9WXIIKH/2CaZuyHpfcKzmLHHvTy
pslRGt7//2zx7waFVfdmDglQ7NmyDg3GIeSQ/HJpdcIJ0EDP2Jtclr5RTp4fbBkb
tkDPL+/b+bkSv0/WG2GFjfvJwMcKJzaCcHexGgrWP8HfFQ7G6qoXQQIDAQABo4H9
MIH6MB0GA1UdDgQWBBRwrCSV/ZYWDC5lqMJa6I7P1IcPijCBygYDVR0jBIHCMIG/
gBRwrCSV/ZYWDC5lqMJa6I7P1IcPiqGBm6SBmDCBlTELMAkGA1UEBhMCVFcxDzAN
BgNVBAgTBlRhaXdhbjEPMA0GA1UEBxMGVGFpcGVpMRswGQYDVQQKExJRTkFQIFN5
c3RlbXMsIEluYy4xDDAKBgNVBAsTA05BUzEWMBQGA1UEAxMNVFMgU2VyaWVzIE5B
UzEhMB8GCSqGSIb3DQEJARYScV9zdXBwb3J0QHFuYXAuY29tggkA6kWqEWI2fysw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAk2YxaeY69q9/b/maNuOB
IXgnKzyagOzXAOiDoFtgCRiDvdgt8jcvFG0okkL+d/j3J2DdGUyLWBamiXmpQogc
Q7H/4DIK+2DbpFq1WOpERwasZ02My1RUSZt223ECHJM+59eCxx7en81XzIysDbTs
/NOVSCnioDmg0Kbi+UIA2A4/SMC1nzsIWQ3vUS1GXnbik1f/14yUIBhz1WXABKt2
HzEkDuDvlP0eSzjPQVXHgEj8MDERpKPbBhzvC6g5yRq5581/NggUEKISU8DjWiWG
q1Oz4jxpF9v4OK6C3Hd1/c1o8k97bnieeeq1sU38N7+L5TeCQg1Jok6Zj5U5lTkn
wg==
-----END CERTIFICATE-----
""": 'qnap_1',"""-----BEGIN CERTIFICATE-----
MIIEqjCCA5KgAwIBAgIJAKv0LMrGDh0OMA0GCSqGSIb3DQEBBQUAMIGUMQswCQYD
VQQGEwJUVzEPMA0GA1UECBMGVGFpd2FuMQ8wDQYDVQQHEwZUYWlwZWkxGjAYBgNV
BAoTEVFOQVAgU3lzdGVtcyBJbmMuMQwwCgYDVQQLEwNOQVMxFjAUBgNVBAMTDVRT
IFNlcmllcyBOQVMxITAfBgkqhkiG9w0BCQEWEnFfc3VwcG9ydEBxbmFwLmNvbTAe
Fw0xMTA3MTIwNDIwMTNaFw0yMTA3MDkwNDIwMTNaMIGUMQswCQYDVQQGEwJUVzEP
MA0GA1UECBMGVGFpd2FuMQ8wDQYDVQQHEwZUYWlwZWkxGjAYBgNVBAoTEVFOQVAg
U3lzdGVtcyBJbmMuMQwwCgYDVQQLEwNOQVMxFjAUBgNVBAMTDVRTIFNlcmllcyBO
QVMxITAfBgkqhkiG9w0BCQEWEnFfc3VwcG9ydEBxbmFwLmNvbTCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAOsbzy0QgE0EZtGas6TNxTqeXfSHGIf59DCy
WcCd7Vsnojm4SGBR1rqLDucuC/r/xL+DuGt2s+gYDr8LEXbDIk23grcq2rzD1l9j
aqKTcB4A4EjxOtY7ZMSEOvSJbrZd2WYan8yaoE6UH9I5eUlSg+KLFqoIqAnxhyfg
rOT5lmV38NIR/6YG+tAKgBSFMmdyeVS1vYoQwJ1QyjwW3ngfNzl+UTTLwHeAnfQ5
619Ms0dWtGNDc2v2W579p/9AEeVG69vaTjDRbmJkskZPSd56DtHf/wGCnpl4OvHL
M8O8NiVOGVlVRO30FLh1enT5B0T8V2+iCZw1mKh2GGubqpcOAlUCAwEAAaOB/DCB
+TAdBgNVHQ4EFgQUBxg6/iUyXScgk6BpjJyw87nUe6QwgckGA1UdIwSBwTCBvoAU
Bxg6/iUyXScgk6BpjJyw87nUe6ShgZqkgZcwgZQxCzAJBgNVBAYTAlRXMQ8wDQYD
VQQIEwZUYWl3YW4xDzANBgNVBAcTBlRhaXBlaTEaMBgGA1UEChMRUU5BUCBTeXN0
ZW1zIEluYy4xDDAKBgNVBAsTA05BUzEWMBQGA1UEAxMNVFMgU2VyaWVzIE5BUzEh
MB8GCSqGSIb3DQEJARYScV9zdXBwb3J0QHFuYXAuY29tggkAq/QsysYOHQ4wDAYD
VR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEA3z2detMLGyiMlWUrNT3neU6f
/Qj2dMmf3Y+g05aHMDzYt7w5fRuWiZRYFRMS9W8NHvhwWfOPk584gGJQi/mhehXa
AYJkiKVMBjJUWpAGdoLP4U1mXTLexVG3OYpRNsEUpHyEMyDBFhLnMPbem8n2x4Y/
b4jGaL66TKIRXc2d79imFjgS6AaXHlQ+wPd61phDqu01YaBXeOUpQcD6YSHAnct5
dcZ4YAw3HzRC9N11LlFooYhL9K51+wa+cbwvRWlvH72eL9AB5rzHHGLf41Pz9V0p
mHrBMGh5AqGF6Cgx/kz1/Mcb6kgHUS4eO4RoHeiYyZk/YNBt7y8Va73GGbMviA==
-----END CERTIFICATE-----
""": 'qnap_2',"""-----BEGIN CERTIFICATE-----
MIIErTCCA5WgAwIBAgIJAOpFqhFiNn8rMA0GCSqGSIb3DQEBBQUAMIGVMQswCQYD
VQQGEwJUVzEPMA0GA1UECBMGVGFpd2FuMQ8wDQYDVQQHEwZUYWlwZWkxGzAZBgNV
BAoTElFOQVAgU3lzdGVtcywgSW5jLjEMMAoGA1UECxMDTkFTMRYwFAYDVQQDEw1U
UyBTZXJpZXMgTkFTMSEwHwYJKoZIhvcNAQkBFhJxX3N1cHBvcnRAcW5hcC5jb20w
HhcNMTEwNzA4MTAwOTQ1WhcNMjEwNzA1MTAwOTQ1WjCBlTELMAkGA1UEBhMCVFcx
DzANBgNVBAgTBlRhaXdhbjEPMA0GA1UEBxMGVGFpcGVpMRswGQYDVQQKExJRTkFQ
IFN5c3RlbXMsIEluYy4xDDAKBgNVBAsTA05BUzEWMBQGA1UEAxMNVFMgU2VyaWVz
IE5BUzEhMB8GCSqGSIb3DQEJARYScV9zdXBwb3J0QHFuYXAuY29tMIIBIjANBgkq
hkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAngIqhFfRtB3lv/DmPYp+rMTt6xRQMtv3
aQYczHhgAVQD9XPOZfEfSxNreFnXGaeWRKTCvH0iVhAUFLaFLH4hncrrI027r7D4
l323S4KWy12UrY3JHcLEwNp4uMlMd713dkSnh967ZY1Coml34f68+KijLe57vlxZ
jpK8A0KCdBwwGDojFoR0hoNmjVZJard8xvvSv9WXIIKH/2CaZuyHpfcKzmLHHvTy
pslRGt7//2zx7waFVfdmDglQ7NmyDg3GIeSQ/HJpdcIJ0EDP2Jtclr5RTp4fbBkb
tkDPL+/b+bkSv0/WG2GFjfvJwMcKJzaCcHexGgrWP8HfFQ7G6qoXQQIDAQABo4H9
MIH6MB0GA1UdDgQWBBRwrCSV/ZYWDC5lqMJa6I7P1IcPijCBygYDVR0jBIHCMIG/
gBRwrCSV/ZYWDC5lqMJa6I7P1IcPiqGBm6SBmDCBlTELMAkGA1UEBhMCVFcxDzAN
BgNVBAgTBlRhaXdhbjEPMA0GA1UEBxMGVGFpcGVpMRswGQYDVQQKExJRTkFQIFN5
c3RlbXMsIEluYy4xDDAKBgNVBAsTA05BUzEWMBQGA1UEAxMNVFMgU2VyaWVzIE5B
UzEhMB8GCSqGSIb3DQEJARYScV9zdXBwb3J0QHFuYXAuY29tggkA6kWqEWI2fysw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAk2YxaeY69q9/b/maNuOB
IXgnKzyagOzXAOiDoFtgCRiDvdgt8jcvFG0okkL+d/j3J2DdGUyLWBamiXmpQogc
Q7H/4DIK+2DbpFq1WOpERwasZ02My1RUSZt223ECHJM+59eCxx7en81XzIysDbTs
/NOVSCnioDmg0Kbi+UIA2A4/SMC1nzsIWQ3vUS1GXnbik1f/14yUIBhz1WXABKt2
HzEkDuDvlP0eSzjPQVXHgEj8MDERpKPbBhzvC6g5yRq5581/NggUEKISU8DjWiWG
q1Oz4jxpF9v4OK6C3Hd1/c1o8k97bnieeeq1sU38N7+L5TeCQg1Jok6Zj5U5lTkn
wg==
-----END CERTIFICATE-----
""": 'qnap_3',"""-----BEGIN CERTIFICATE-----
MIIEqjCCA5KgAwIBAgIJAKv0LMrGDh0OMA0GCSqGSIb3DQEBBQUAMIGUMQswCQYD
VQQGEwJUVzEPMA0GA1UECBMGVGFpd2FuMQ8wDQYDVQQHEwZUYWlwZWkxGjAYBgNV
BAoTEVFOQVAgU3lzdGVtcyBJbmMuMQwwCgYDVQQLEwNOQVMxFjAUBgNVBAMTDVRT
IFNlcmllcyBOQVMxITAfBgkqhkiG9w0BCQEWEnFfc3VwcG9ydEBxbmFwLmNvbTAe
Fw0xMTA3MTIwNDIwMTNaFw0yMTA3MDkwNDIwMTNaMIGUMQswCQYDVQQGEwJUVzEP
MA0GA1UECBMGVGFpd2FuMQ8wDQYDVQQHEwZUYWlwZWkxGjAYBgNVBAoTEVFOQVAg
U3lzdGVtcyBJbmMuMQwwCgYDVQQLEwNOQVMxFjAUBgNVBAMTDVRTIFNlcmllcyBO
QVMxITAfBgkqhkiG9w0BCQEWEnFfc3VwcG9ydEBxbmFwLmNvbTCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAOsbzy0QgE0EZtGas6TNxTqeXfSHGIf59DCy
WcCd7Vsnojm4SGBR1rqLDucuC/r/xL+DuGt2s+gYDr8LEXbDIk23grcq2rzD1l9j
aqKTcB4A4EjxOtY7ZMSEOvSJbrZd2WYan8yaoE6UH9I5eUlSg+KLFqoIqAnxhyfg
rOT5lmV38NIR/6YG+tAKgBSFMmdyeVS1vYoQwJ1QyjwW3ngfNzl+UTTLwHeAnfQ5
619Ms0dWtGNDc2v2W579p/9AEeVG69vaTjDRbmJkskZPSd56DtHf/wGCnpl4OvHL
M8O8NiVOGVlVRO30FLh1enT5B0T8V2+iCZw1mKh2GGubqpcOAlUCAwEAAaOB/DCB
+TAdBgNVHQ4EFgQUBxg6/iUyXScgk6BpjJyw87nUe6QwgckGA1UdIwSBwTCBvoAU
Bxg6/iUyXScgk6BpjJyw87nUe6ShgZqkgZcwgZQxCzAJBgNVBAYTAlRXMQ8wDQYD
VQQIEwZUYWl3YW4xDzANBgNVBAcTBlRhaXBlaTEaMBgGA1UEChMRUU5BUCBTeXN0
ZW1zIEluYy4xDDAKBgNVBAsTA05BUzEWMBQGA1UEAxMNVFMgU2VyaWVzIE5BUzEh
MB8GCSqGSIb3DQEJARYScV9zdXBwb3J0QHFuYXAuY29tggkAq/QsysYOHQ4wDAYD
VR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEA3z2detMLGyiMlWUrNT3neU6f
/Qj2dMmf3Y+g05aHMDzYt7w5fRuWiZRYFRMS9W8NHvhwWfOPk584gGJQi/mhehXa
AYJkiKVMBjJUWpAGdoLP4U1mXTLexVG3OYpRNsEUpHyEMyDBFhLnMPbem8n2x4Y/
b4jGaL66TKIRXc2d79imFjgS6AaXHlQ+wPd61phDqu01YaBXeOUpQcD6YSHAnct5
dcZ4YAw3HzRC9N11LlFooYhL9K51+wa+cbwvRWlvH72eL9AB5rzHHGLf41Pz9V0p
mHrBMGh5AqGF6Cgx/kz1/Mcb6kgHUS4eO4RoHeiYyZk/YNBt7y8Va73GGbMviA==
-----END CERTIFICATE-----
""": 'qnap_4',"""-----BEGIN CERTIFICATE-----
MIICDjCCAXegAwIBAwIBAjANBgkqhkiG9w0BAQUFADBNMRUwEwYDVQQDEwwwMDMw
QUIwMDAwMDIxDzANBgNVBAsTBlNBNTIwVzEWMBQGA1UEChMNQ2lzY28gU3lzdGVt
czELMAkGA1UEBhMCVVMwHhcNMDgwNzA0MDAwMDEzWhcNMTgwNzAyMDAwMDEzWjBN
MRUwEwYDVQQDEwwwMDMwQUIwMDAwMDIxDzANBgNVBAsTBlNBNTIwVzEWMBQGA1UE
ChMNQ2lzY28gU3lzdGVtczELMAkGA1UEBhMCVVMwgZ8wDQYJKoZIhvcNAQEBBQAD
gY0AMIGJAoGBAO0G6eYbKgiqYVGH6dD0Go1KThsmvZcQudLs8fkfAmQiE2XJuxqM
9DiRwiN3w5kUs5zcrlG9TE9Q50ugYhGzkvqKRPaU8LmVZBBJhZbnq97rU1VTb12m
iPhW7/lk3ObPZX7aROuPhIaqXTa65tqoJ6+zOZCLecY8W3qHtLZpEym9AgMBAAEw
DQYJKoZIhvcNAQEFBQADgYEAdeMHmEVCf1pCT5sgkR/mm9ZNyEoj/e7hStHLbDwj
75KBhtu087VcvjjyFGX7RuIWPJymAPoxg1H+PbUONC1K/wS9ZxhMlJWtJWEt5cQJ
qJBKMXM9l1+toVhiArsf/nGgCOfmmGrjk6bxvk7oj4/uKt7cifP0uYIV/wC40J5L
+Js=
-----END CERTIFICATE-----
""": 'cisco_sa450g',"""-----BEGIN CERTIFICATE-----
MIIC4jCCAcoCAQIwDQYJKoZIhvcNAQEEBQAweTEPMA0GA1UECBMGU3VycmV5MQsw
CQYDVQQGEwJHQjEiMCAGCSqGSIb3DQEJARYTY29udGFjdEBzYW1zdW5nLmNvbTEV
MBMGA1UEChMMU2Ftc3VuZyBTRVJJMQwwCgYDVQQLEwNEVFYxEDAOBgNVBAMTB0NB
IHJvb3QwHhcNNzAwMTAxMDAwMDAwWhcNMzAwMTAxMDAwMDAwWjB5MQ8wDQYDVQQI
EwZTdXJyZXkxCzAJBgNVBAYTAkdCMSIwIAYJKoZIhvcNAQkBFhNjb250YWN0QHNh
bXN1bmcuY29tMRUwEwYDVQQKEwxTYW1zdW5nIFNFUkkxDDAKBgNVBAsTA0RUVjEQ
MA4GA1UEAxMHc2VydmVyMTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA1+pv
QRm2S/CAeTge+veVhOicFfWkKc7SB2PAk+dAotgAMR4Zup+PoYlKhibC/Y96in/H
bRdvTvFA5aV2JC3rMVDYhqWVzOjlx9HYPXtyXAVQvkPeLTDc5lL8WV4/3hhLfej7
tcHGefOA6N0ZzB+n73jE5AxLzW/DSiIvbkRzpuECAwEAATANBgkqhkiG9w0BAQQF
AAOCAQEAOrabmYo+Uby/P1JhScSN2e6e3uq/owzyO59Y8fEdK1mPilP6ylxcJ3pS
1QuGfzS+hUy64SlEAeB4rPAbPmpoBQBNgSGm079IfHY/anr4f6q+5Gt0NEcxvdy5
h1UdKgPViZNf6fj3UO0FYQqJqHnt8gmqPH7AfMKZ6N3bAcadu+7xM7PoRRq/BxtO
r1hby9qrqeloQGyPRanz1IzUnpyZGcYMiLJMeRSbBlmlIooMT0koplzG7NbxCkFv
MEAojkO/hcwiE0uvwY62hAriSqopnoVw7keUEiC6ibL5qJMmIfj1jgOrk6BnlXGG
Q5Hb2g3MCxhT0JuZA4pr4tI42/ai/Q==
-----END CERTIFICATE-----
""": 'samsung_device_1',"""-----BEGIN CERTIFICATE-----
MIIC5TCCAc0CAQIwDQYJKoZIhvcNAQEEBQAweTEPMA0GA1UECBMGU3VycmV5MQsw
CQYDVQQGEwJHQjEiMCAGCSqGSIb3DQEJARYTY29udGFjdEBzYW1zdW5nLmNvbTEV
MBMGA1UEChMMU2Ftc3VuZyBTRVJJMQwwCgYDVQQLEwNEVFYxEDAOBgNVBAMTB1Jv
b3QgQ0EwHhcNNzAwMTAxMDAwMDAwWhcNMzAwMTAxMDAwMDAwWjB8MQ8wDQYDVQQI
EwZTdXJyZXkxCzAJBgNVBAYTAkdCMSIwIAYJKoZIhvcNAQkBFhNjb250YWN0QHNh
bXN1bmcuY29tMRUwEwYDVQQKEwxTYW1zdW5nIFNFUkkxDDAKBgNVBAsTA0RUVjET
MBEGA1UEAxMKMTA2LjEuOS4zOTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA
psK9tMo/6/GQ5Z6777bWixAi+/eYL6EPWAgym+ybAYCHmVAEDr1ln87wkuiAP4Uc
92CMYW5hBRJsmHjAAn6zf0uSEyzKE1QmFXPxUbT1PD8G0u0mTdcKALjzN0eW8KGQ
2sQXcRghQWTZQcrz3Nhyu35hFY5/EtzxoElYu7Jv25sCAwEAATANBgkqhkiG9w0B
AQQFAAOCAQEAcJS0XVzSpfTLh5G9psdSLGPbb0pyJPYwwcYBBAykvBorrf66+CYz
yqzgkWxsUMlPfvZhwWHoRZFx7GcKoT2scUeU3ULtuzP2WyslKUndjD49UzacgKcj
IbHv2R1l278ewviQ7mri22O9PXNbfTstbtSvetrAD376zF6xuBwPdCpbqtiT35gS
obDNXrOTV1+sRg17Uamb1ujEnYQZC2lXckrYYkNOhCAbVprVRRA4EfHaUMhHWG4X
U+/n5bF/ZHRbzFu44OXRgwr3XPLY7ZjXGVV5Yw6rVkVNTv6yfGYWwBdyyO7oy9wi
+BJ8yq8XYnqpz4k7KkQyb+kjjAV2XzRpOQ==
-----END CERTIFICATE-----
""":'samsung_device_2',"""-----BEGIN CERTIFICATE-----
MIICAjCCAWsCAQIwDQYJKoZIhvcNAQEEBQAwcjELMAkGA1UEBhMCQ0ExEDAOBgNV
BAgTB09udGFyaW8xDzANBgNVBAcTBk90dGF3YTEYMBYGA1UEChMPQmVsYWlyIE5l
dHdvcmtzMSYwJAYJKoZIhvcNAQkBFhdpbmZvQGJlbGFpcm5ldHdvcmtzLmNvbTAe
Fw0wNDA0MjgxNTEzMzNaFw0yOTA0MjIxNTEzMzNaMCExHzAdBgNVBAMTFnd3dy5i
ZWxhaXJuZXR3b3Jrcy5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBANh7
5dJ6d3Iei+bpMLrPhPgNoGMd+O/OF+2DGWasVC63Q00XDbMo5n6a5REoY+ehSUAT
x50HSuu5eTtuzBr3dVaM7o1Yp/NEOxdVsxebcgH9p6DKQSsZRv3j3EgBkbfSEzPj
rDGzIxMnLWJ8oFJP0DTzOfi/bbd1frraXPsYuNLpAgMBAAEwDQYJKoZIhvcNAQEE
BQADgYEAM4ev1OFW+bY59VwChDip2w/p8MgYkOSBRvYlsvA8thfa0B9lbE9i0MJX
ZeYYxt1fq8Doe3ZesQfKgO4dFl4v/kI97lYd/XKSFObnTDbpWVRCPwrYp8jdTGAs
PcCplNnHaZQiPaOwIOK/KsICONduutXgmBiY7y8S1HNLxmRd29g=
-----END CERTIFICATE-----
""": 'belair_1',"""-----BEGIN CERTIFICATE-----  
MIICIjCCAYugAwIBAgIQfmSHT6LezY9GuZTTXVlTfjANBgkqhkiG9w0BAQsFADAb
MRkwFwYDVQQDExBBdmlnaWxvbiBHYXRld2F5MCAXDTAwMDEwMTA3MDAwMFoYDzIw
NTAwMTAxMDcwMDAwWjAbMRkwFwYDVQQDExBBdmlnaWxvbiBHYXRld2F5MIGfMA0G
CSqGSIb3DQEBAQUAA4GNADCBiQKBgQDJn/mXOOhpcYuBu9oFw1Qi4rvztsGF60u1
VYZTmHPMbLZEtygWC1WuVGeWefvYrnPl1yXl2c5++WnN0FwphBPZEnhwjn2Y8w73
OZWJjtotUCScbuZJm1ufRNlt5wsP9SJjl4fKmxbJekQ4xn1VX3Lr9OZ/tTNyL5lq
kAQwaQu6swIDAQABo2UwYzATBgNVHSUEDDAKBggrBgEFBQcDATBMBgNVHQEERTBD
eYIQfmSHT6LezY9GuZTTXVlTfjANBgkqhkiG9w0BAQsFAAOBgQCbkIglmPoDg83a
J8Txgu46COLhVDeksEaNemFM1mkHrzPIV3oxgYb1UUjeoa9X0PMujSxzvMwOImvt
D6bLOfC0banGlfN6pLT3/tYirLwerK2Xmb/UfRaTK9ogopTcxgw0/ATquiotTlJy
u5qy23Pc32MmsD3nxHHjKsf2FU5bng==
-----END CERTIFICATE-----
""": 'avigilon',"""-----BEGIN CERTIFICATE-----
MIIDBjCCAm+gAwIBAgIJAJXnvRDyazyBMA0GCSqGSIb3DQEBBAUAMIGbMQswCQYD
VQQGEwJDTjERMA8GA1UECAwIWmhlSmlhbmcxETAPBgNVBAcMCEhhbmdaaG91MRIw
EAYDVQQKDAlISUtWSVNJT04xDzANBgNVBAsMBkRWUk5WUjEaMBgGA1UEAwwRd3d3
Lmhpa3Zpc2lvbi5jb20xJTAjBgkqhkiG9w0BCQEWFm1lbmdob25nQGhpa3Zpc2lv
bi5jb20wHhcNMTIxMTIzMDU1NTE1WhcNMTUwODIwMDU1NTE1WjCBmzELMAkGA1UE
BhMCQ04xETAPBgNVBAgMCFpoZUppYW5nMREwDwYDVQQHDAhIYW5nWmhvdTESMBAG
A1UECgwJSElLVklTSU9OMQ8wDQYDVQQLDAZEVlJOVlIxGjAYBgNVBAMMEXd3dy5o
aWt2aXNpb24uY29tMSUwIwYJKoZIhvcNAQkBFhZtZW5naG9uZ0BoaWt2aXNpb24u
Y29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDWDboSDAm2WPEBgt1wzDV
nDfELEPcvIdtLyHjae7VQNbcTM3n0xlB9S8ptWTOJzI2+eb3U97wMTAH3u24Stii
wU5bqKi3PlPNCHpwB6wz7jkcjP+/6ZTZ3rc2l99hKgmuxV7XTsrrKzExRY42YTWO
aekgWMp9L1UU0aqkBroheQIDAQABo1AwTjAdBgNVHQ4EFgQUSWUSK752hniMZvoC
jykG9jGdOegwHwYDVR0jBBgwFoAUSWUSK752hniMZvoCjykG9jGdOegwDAYDVR0T
BAUwAwEB/zANBgkqhkiG9w0BAQQFAAOBgQC1GHVqLN5mLN5lMxcjNG43MNlWHNtb
lvjQzw6h2iuRYxQRo8EdBC9l0J1tbVZZHUNXSYma6eZ3k/QMhCefiCfxQn4vIrGC
tNDihITTgAiH1HPlmiI9HUhZ+QFj7uUmhAz/3Se5DbfDup70BpsvxSJT/w5hEB+u
dd7a3UvS/6S3jw==
-----END CERTIFICATE----
""": 'hikvision',"""-----BEGIN CERTIFICATE-----
MIID1jCCAz+gAwIBAgIBAjANBgkqhkiG9w0BAQQFADCBmDELMAkGA1UEBhMCVVMx
EDAOBgNVBAgTB0Zsb3JpZGExEzARBgNVBAcTCkNsZWFyd2F0ZXIxETAPBgNVBAoT
CFZlcmlGb25lMRYwFAYDVQQLEw1QZXRyby9DLVN0b3JlMREwDwYDVQQDEwhzYXBw
aGlyZTEkMCIGCSqGSIb3DQEJARYVaGVscGRlc2tAdmVyaWZvbmUuY29tMB4XDTA1
MTEwOTIyMzYxOFoXDTE3MTEwNjIyMzYxOFowgZgxCzAJBgNVBAYTAlVTMRAwDgYD
VQQIEwdGbG9yaWRhMRMwEQYDVQQHEwpDbGVhcndhdGVyMREwDwYDVQQKEwhWZXJp
Rm9uZTEWMBQGA1UECxMNUGV0cm8vQy1TdG9yZTERMA8GA1UEAxMIc2FwcGhpcmUx
JDAiBgkqhkiG9w0BCQEWFWhlbHBkZXNrQHZlcmlmb25lLmNvbTCBnzANBgkqhkiG
9w0BAQEFAAOBjQAwgYkCgYEAx7zhVrDRNGd5r9Bue5vZBVsKVGQ886qmpZppSs/Q
O0mJd7or4KX5FmKqRsohfyjC5FTpXowm6T6XhNSKzVMryKdaYsDuXx1S9iSFJUAd
/GrAd/UnaN90Vagj0Qxq80Watel0ijIVXdRNgBD54hlIN26JVIWCBXpqeVJvyaZb
e9sCAwEAAaOCASwwggEoMAkGA1UdEwQCMAAwLAYJYIZIAYb4QgENBB8WHU9wZW5T
U0wgR2VuZXJhdGVkIENlcnRpZmljYXRlMB0GA1UdDgQWBBRKuXAmBhDAfd78nvWt
rg2UFziWdTCBzQYDVR0jBIHFMIHCgBSYm79NCg0ifKM4p+XHeH7pBXySbKGBnqSB
mzCBmDELMAkGA1UEBhMCVVMxEDAOBgNVBAgTB0Zsb3JpZGExEzARBgNVBAcTCkNs
ZWFyd2F0ZXIxETAPBgNVBAoTCFZlcmlGb25lMRYwFAYDVQQLEw1QZXRyby9DLVN0
b3JlMREwDwYDVQQDEwhzYXBwaGlyZTEkMCIGCSqGSIb3DQEJARYVaGVscGRlc2tA
dmVyaWZvbmUuY29tggkAohLS7ZPZzhcwDQYJKoZIhvcNAQEEBQADgYEAWWWiJhPB
b26AgDmzRCyaXL3XOdgZN9knepJMx7m+tFjUwe+XXuZgK70Mick2iY0yYP3RV/4A
nZRR9o1WHWJPhKnFCXBY9ujrrs3+v+M0MwDqcLsQI4aODjyme6v46urKsWw1HgLX
8eloLP7yBmkCpBY4X0H0wvzrLLCsbeIxFts=
-----END CERTIFICATE-----
""":'Verifone_Sapphire',"""-----BEGIN CERTIFICATE-----
MIIDaTCCAlGgAwIBAgIBATANBgkqhkiG9w0BAQsFADB4MQswCQYDVQQGEwJUVzEQ
MA4GA1UECBMHSHNpbkNodTEOMAwGA1UEBxMFSHVLb3UxFjAUBgNVBAoTDURyYXlU
ZWsgQ29ycC4xGDAWBgNVBAsTD0RyYXlUZWsgU3VwcG9ydDEVMBMGA1UEAxMMVmln
b3IgUm91dGVyMB4XDTE0MDUxNDA2MDUwMFoXDTM5MDUxNDA2MDUwMFoweDELMAkG
A1UEBhMCVFcxEDAOBgNVBAgTB0hzaW5DaHUxDjAMBgNVBAcTBUh1S291MRYwFAYD
VQQKEw1EcmF5VGVrIENvcnAuMRgwFgYDVQQLEw9EcmF5VGVrIFN1cHBvcnQxFTAT
BgNVBAMTDFZpZ29yIFJvdXRlcjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
ggEBAJMUaTRB0d/DF4YwqS60XT9UOeZWaNsrZwprgRivBjX6e491Q/PUzVxVlGPH
5qJFIjXn0I19Vgi3dRHaicW3yxkevtQILa/yj3OtFVqLsvMXQoJ22vo39EHkDo5T
uyZZ75xJuvSMCWKshVE5KT/fwY6t7lwz1yYK8oo53l9aUEGNZxuZh0HLWDq7VJqk
TvF2NqysSmHuly1b/xMUUJWwoi0oAC4pzBX1v0VrWPxRgQ0kKQUJlzRjesjuJNcY
uRgif3vDGSsbRPSPOgai6CmSjrSrXOm/nRocjFfa60PbGbpOL0B4G+koPPV9rPko
53O6L7P7sc1uQuuEu8QvbQ3MHMcCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAEg4n
m/P7y+jkA9c2flwRJCAx9eCK6l4V/VK3ZKLHsyhFd9buLM1/P+69VDpXfYo51oxZ
wqUifoanbcvTD1nLQReHCEs25hEubJGT/M5oqiDr7ubBgdgSETQjczavxwkUIe8v
j6z7Ad5H355g4bkKrBSHCnOIrNRPm9i22NRyEurIv01Y5LdIXKEVw6gtdWGKDfOA
dJJyS2bUiD4u2jbl+0xBKQKOAtbsQryKrY+TeXBvjFEl1APBAzFZkC4jnu6fyG8g
HjaxcayxLxHNwjAphu4/nMNt/YCNmDrx95VikIn6W8LadtP1qfAD8YXCJ6uo1VuM
e+teFGQTJ0udsxQsTA==
-----END CERTIFICATE-----
""":"Vigor_1","""-----BEGIN CERTIFICATE-----
MIIDPDCCAqWgAwIBAgIBADANBgkqhkiG9w0BAQQFADB4MQswCQYDVQQGEwJUVzEQ
MA4GA1UECBMHSHNpbkNodTEOMAwGA1UEBxMFSHVLb3UxFjAUBgNVBAoTDURyYXlU
ZWsgQ29ycC4xGDAWBgNVBAsTD0RyYXlUZWsgU3VwcG9ydDEVMBMGA1UEAxMMVmln
b3IgUm91dGVyMB4XDTA0MDcyNzA4MzAyOVoXDTI5MDMxODA4MzAyOVoweDELMAkG
A1UEBhMCVFcxEDAOBgNVBAgTB0hzaW5DaHUxDjAMBgNVBAcTBUh1S291MRYwFAYD
VQQKEw1EcmF5VGVrIENvcnAuMRgwFgYDVQQLEw9EcmF5VGVrIFN1cHBvcnQxFTAT
BgNVBAMTDFZpZ29yIFJvdXRlcjCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA
v9mcIae/fk+xZVb3S76eEGtiuRiyEEPdf0piWurMr4QqWWYpBs1gocQ/uw1VNFbt
A32zJM0pblAHuy7J1rj6n/Y2xYDuGksp3C9xxYbzc1CUoUoyqH/6q5dlAxdEPCgi
RfgE4ZH7rYMWBOsxfsujApu/I7iCI6l8PcMUWatwGrkCAwEAAaOB1TCB0jAdBgNV
HQ4EFgQUm4k9jGeEtSEGKxixoaC25//QJTEwgaIGA1UdIwSBmjCBl4AUm4k9jGeE
tSEGKxixoaC25//QJTGhfKR6MHgxCzAJBgNVBAYTAlRXMRAwDgYDVQQIEwdIc2lu
Q2h1MQ4wDAYDVQQHEwVIdUtvdTEWMBQGA1UEChMNRHJheVRlayBDb3JwLjEYMBYG
A1UECxMPRHJheVRlayBTdXBwb3J0MRUwEwYDVQQDEwxWaWdvciBSb3V0ZXKCAQAw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQQFAAOBgQCl66hKfBd0jG6PRYjGcETc
5NmJ1oa/5xOAoO5EtH4aF+GNPC/zFTKowfAj5t9zaQf5LwvA4W0BshmixeKpzr+d
dA2kCvhT7TXT3KTDcfkw/0V6VPC4aGAvY3q9455OWynpxpqrjbuQO7G0650XeGkN
/N3J4VygwqqngAgE2hO/kg==
-----END CERTIFICATE-----
""":"Vigor_2","""-----BEGIN CERTIFICATE-----
MIICgDCCAekCAQMwDQYJKoZIhvcNAQEEBQAwgaIxJjAkBgNVBAoTHUxpZmVTaXpl
IENvbW11bmljYXRpb25zLCBJbmMuMQswCQYDVQQLEwJJVDEmMCQGCSqGSIb3DQEJ
ARYXaG9zdG1hc3RlckBsaWZlc2l6ZS5jb20xDzANBgNVBAcTBkF1c3RpbjEOMAwG
A1UECBMFVGV4YXMxCzAJBgNVBAYTAlVTMRUwEwYDVQQDEwxsaWZlc2l6ZS5jb20w
HhcNMDYxMTIxMjAyNjM5WhcNMTYxMTE4MjAyNjM5WjBuMQswCQYDVQQGEwJVUzEO
MAwGA1UECBMFVGV4YXMxJjAkBgNVBAoTHUxpZmVTaXplIENvbW11bmljYXRpb25z
LCBJbmMuMQswCQYDVQQLEwJJVDEaMBgGA1UEAxQRQV9MaWZlU2l6ZV9TeXN0ZW0w
gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAOTG/rVqWK6UDA9B/bFSXBx3Txwp
3caV31LfDzl4h1ZmOcoL7JFvWAG2OkBBDqmHYbseB/y9S83X6RCpyKUeP8A85Fmg
45DOuIGzNaInDOAkDNHNtRc6GkTJISe1Xh3bIsps8w4T51pFX99rtCEklMC/v0PN
rhkhhvikLH9fRH8nAgMBAAEwDQYJKoZIhvcNAQEEBQADgYEAaGCMOb3DmKVe79gn
GfLzTMowoNsbxxKgDAGtYaRa8iyDitOJBUka98yxYbWHXu0V0dZZImy4Rgez+1G7
l9M/CEaV86EUD5NhRFa5hqsqD5T9E4yRFlZZfKlBiePp62yCuUIbyNU8a64dsBCV
bHQeQfAiLVM+XGhriPvwCyJJNM8=
-----END CERTIFICATE-----
""": 'lifesize_1', """-----BEGIN CERTIFICATE-----
MIID5TCCA06gAwIBAgIBAzANBgkqhkiG9w0BAQ0FADB2MQswCQYDVQQGEwJVUzET
MBEGA1UECBMKQ2FsaWZvcm5pYTEUMBIGA1UEBxMLU2FudGEgQ2xhcmExGDAWBgNV
BAoTD0ZpbGVtYWtlciwgSW5jLjEiMCAGA1UEAxMZRk1JIENlcnRpZmljYXRlIEF1
dGhvcml0eTAeFw0xNDA0MTYxODEzMDFaFw0zNzEyMzEwMDAwMDBaMHYxCzAJBgNV
BAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRQwEgYDVQQHEwtTYW50YSBDbGFy
YTEYMBYGA1UEChMPRmlsZW1ha2VyLCBJbmMuMSIwIAYDVQQDExlGTUkgQ2VydGlm
aWNhdGUgQXV0aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
rzsAd7A87IvOxgGH3IXSs99q8zyjDMaCOUf1v10PlWkZU83hutAKX/hDvqB0hZXN
M1P66RNPWEKtQjAea9N/jahiF3cW78gSO4+vFxJ1gqWRJhj3pSplLw0JvM9yW0dY
ZPKuL4i/gyve9r3zolRSD/MX7N66z9bpDYeSE1cSOgi8w8zGHqnaAFeQWj8Nxwmz
GcchoC0o/r+243tm/NJejkQMUsxAAuE0Iz72SWGCoIe3T0xS6ACjak2ur39DKzzv
oTN4ZFmZQ2gfIq9IfFGn/2gau/ZSoHPGrldde+P6NyQI+BHOdFgi+SGr+s5Abdyh
ozW5Ne+QI5raiWcwr2WHWwIDAQABo4H+MIH7MAkGA1UdEwQCMAAwLAYJYIZIAYb4
QgENBB8WHU9wZW5TU0wgR2VuZXJhdGVkIENlcnRpZmljYXRlMB0GA1UdDgQWBBQD
T74RIpxey0GiF9vtnVEbvEwRmTCBoAYDVR0jBIGYMIGVgBSXpeniC+6YdKXNRz1B
lWHSRcUAIqF6pHgwdjELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWEx
FDASBgNVBAcTC1NhbnRhIENsYXJhMRgwFgYDVQQKEw9GaWxlbWFrZXIsIEluYy4x
IjAgBgNVBAMTGUZNSSBDZXJ0aWZpY2F0ZSBBdXRob3JpdHmCAQEwDQYJKoZIhvcN
AQENBQADgYEAGvylbllBys38X+OoZV6VNelvvILM/5cc8BvcpSnzNT6lWhqUWIvU
eJnPJOo1Ewma8ZkxsTO7D3BW1AHF+cXCiPHW4m9KnPwgiMR5o7o94Fb8FKPlLjnH
8cmvKdK3eKnAuUhwt4YAQlX3IiM2XNgnhKfqcdLmv1qHCPgkLbNceAs=
-----END CERTIFICATE-----
""": 'filemaker_1', """-----BEGIN CERTIFICATE-----
MIIClTCCAf6gAwIBAgIBADANBgkqhkiG9w0BAQQFADA7MQswCQYDVQQGEwJVUzEs
MCoGA1UEAxQjT1JuYW1lX0p1bmdvOiBPcGVuUkcgUHJvZHVjdHMgR3JvdXAwHhcN
MDQwNjAzMTExMTQzWhcNMjQwNTI5MTExMTQzWjA7MQswCQYDVQQGEwJVUzEsMCoG
A1UEAxQjT1JuYW1lX0p1bmdvOiBPcGVuUkcgUHJvZHVjdHMgR3JvdXAwgZ8wDQYJ
KoZIhvcNAQEBBQADgY0AMIGJAoGBAM49r7D/ajki5azd5XYxVcSnKoth9lJxvI+m
vaZjzORt0oLoMWrMbpwFjtLTqqhtWNeY6BAyShWg7yKFsPU0HpX/jHIOAzAkny5J
+loH8nLN596g3P0ZyD6z7Ckqgbzg9MfJ9XLrExMLBn6oLboksY+q67+5zASWMfLR
ZVg+Zv1VAgMBAAGjgagwgaUwDwYDVR0TBAgwBgEB/wIBBTALBgNVHQ8EBAMCAvQw
MQYDVR0lBCowKAYIKwYBBQUHAwIGCCsGAQUFBwMDBggrBgEFBQcDBAYIKwYBBQUH
AwEwPwYJYIZIAYb4QgENBDIWMEp1bmdvIE9wZW5SRyBQcm9kdWN0cyBHcm91cCBz
dGFuZGFyZCBjZXJ0aWZpY2F0ZTARBglghkgBhvhCAQEEBAMCAsQwDQYJKoZIhvcN
AQEEBQADgYEAntbWzY/kUhqtd5lN+ZEY2gYSkt9fWoiLZod9hgMs14I+JGRWuRD1
re93wvlF1FFvxJOkz2MLc0dkR0z0/W36z7Tw7ypJU/81dynta9yIWLSywdn1/Y6A
7V6BwyQFRuJlg2/nDP+tUltc6cXbUe8GdTm2IATAzER8OKGRbBMtXqs=
-----END CERTIFICATE-----
""": 'verizon_jungo',"""-----BEGIN CERTIFICATE-----
MIIBojCCAQugAwIBAgIBADANBgkqhkiG9w0BAQUFADAXMRUwEwYDVQQDEwxDYW5v
biBpUi1BRFYwHhcNMTIwMTAxMDAwMDAwWhcNMzcxMjMxMjM1OTU5WjAXMRUwEwYD
VQQDEwxDYW5vbiBpUi1BRFYwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAK8O
j7zVinxF+pCuvSBP2CCarHOjfR1MtaMHCECgU+UdQZZ0CBd4XZgwI79DuJRtVjJE
ilkJ+vtbqF5sqz9LL/7nJaQTVk3cQUzMdSa02XVtRFx565VJU4JmViGncaSnDkgD
i8s2PT8tdXR4qf4eotcXGngFsJPdetPqXj1YCnnTAgMBAAEwDQYJKoZIhvcNAQEF
BQADgYEABmV7HdodJhSYVrdAz+Afl7PasUJrWOa4RZZWBk9Fo9Q2abdNz2BYMVTa
alGwXOBJ7XjpodjQDHgCI2NvZKCqsQ8Z2+t6b4h6lJvDPsH+9cX0VDnVZX1oFdhi
GJGXcLwzkVttHIxN37u15FQun+cGZwD61H+yYJVibbhhTvGvCXc=
-----END CERTIFICATE-----
""": 'canon_iradv', """-----BEGIN CERTIFICATE-----
MIIEADCCA2mgAwIBAgIBADANBgkqhkiG9w0BAQUFADCBtzELMAkGA1UEBhMCQ0Ex
DzANBgNVBAgTBlF1ZWJlYzEOMAwGA1UEBxMFTGF2YWwxHzAdBgNVBAoTFkNvbHVi
cmlzIE5ldHdvcmtzIEluYy4xITAfBgNVBAsTGFdpcmVsZXNzIE5ldHdvcmsgRGV2
aWNlczEeMBwGA1UEAxMVd2lyZWxlc3MuY29sdWJyaXMuY29tMSMwIQYJKoZIhvcN
AQkBFhRzdXBwb3J0QGNvbHVicmlzLmNvbTAeFw0wNDAxMTUyMDQ1NDNaFw0yNDAx
MTAyMDQ1NDNaMIG3MQswCQYDVQQGEwJDQTEPMA0GA1UECBMGUXVlYmVjMQ4wDAYD
VQQHEwVMYXZhbDEfMB0GA1UEChMWQ29sdWJyaXMgTmV0d29ya3MgSW5jLjEhMB8G
A1UECxMYV2lyZWxlc3MgTmV0d29yayBEZXZpY2VzMR4wHAYDVQQDExV3aXJlbGVz
cy5jb2x1YnJpcy5jb20xIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAY29sdWJyaXMu
Y29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdKvLHHTeKRGxhSS+tloIB
ed8Nf+oLv51vJGhkcELX5CD3+01UDHYYE6qgS+ksC2nyCnFoP1E1VG+0xenNfhgt
jBzzjleZN8gDyGhJkhj577MSI+km/pE/9r+3QEthFNkArSrtaMKsefH4cDD2p/mQ
rIkLudcuhx9q+tQrwU1MtQIDAQABo4IBGDCCARQwHQYDVR0OBBYEFLz/h1qgE9Fi
teKUawOvUVsZcIvuMIHkBgNVHSMEgdwwgdmAFLz/h1qgE9FiteKUawOvUVsZcIvu
oYG9pIG6MIG3MQswCQYDVQQGEwJDQTEPMA0GA1UECBMGUXVlYmVjMQ4wDAYDVQQH
EwVMYXZhbDEfMB0GA1UEChMWQ29sdWJyaXMgTmV0d29ya3MgSW5jLjEhMB8GA1UE
CxMYV2lyZWxlc3MgTmV0d29yayBEZXZpY2VzMR4wHAYDVQQDExV3aXJlbGVzcy5j
b2x1YnJpcy5jb20xIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAY29sdWJyaXMuY29t
ggEAMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEATyCdakxIjA7ZuhL4
4pta6W3eXS+h0KHwaFrwNQ1KgG/RAS+LqK/5fqvHp9zKTW/k8b5OvpohMtCPGl4x
r2g8lllWxQlNawCTpwTxT0x8603y1WPhGmp1QJvt+6/9pvshykLqusTo6mPdv0Mr
vU2H3FkERj3HmOlybgW2KHIrRAM=
-----END CERTIFICATE-----
""": 'colubris', """-----BEGIN CERTIFICATE-----
MIIDrjCCAxegAwIBAgIDA8TjMA0GCSqGSIb3DQEBBQUAMIGbMQswCQYDVQQGEwJV
UzESMBAGA1UECBMJTWlubmVzb3RhMRQwEgYDVQQHEwtNaW5uZWFwb2xpczEXMBUG
A1UEChMOQXN0cm9jb20gQ29ycC4xEjAQBgNVBAsTCVBvd2VyTGluazESMBAGA1UE
AxMJUG93ZXJMaW5rMSEwHwYJKoZIhvcNAQkBFhJoZWxwQGFzdHJvY29ycC5jb20w
HhcNMDkwNTIxMTYxMTI4WhcNMzYxMDA1MTYxMTI4WjCBmzELMAkGA1UEBhMCVVMx
EjAQBgNVBAgTCU1pbm5lc290YTEUMBIGA1UEBxMLTWlubmVhcG9saXMxFzAVBgNV
BAoTDkFzdHJvY29tIENvcnAuMRIwEAYDVQQLEwlQb3dlckxpbmsxEjAQBgNVBAMT
CVBvd2VyTGluazEhMB8GCSqGSIb3DQEJARYSaGVscEBhc3Ryb2NvcnAuY29tMIGf
MA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDFRS3TuJ/tFF2RdtF2r3kcKvYDLW9g
R2mFNHyrKtZomGJTQSaVifpeZAtUnD6L7l259lNHC+l+xjf5gzCsxHVVE7Cm69uc
U9VucAbAKtV1H9XnzV184pZLRrsj4NKTA9Y//DLV7JIrg5fzoR8EpVS5QjlH1jw0
v+WXFQrkHY9OMQIDAQABo4H9MIH6MB0GA1UdDgQWBBSsdQb8zq0OA2/lyWf8ck7h
8HvBoTCBygYDVR0jBIHCMIG/gBSsdQb8zq0OA2/lyWf8ck7h8HvBoaGBoaSBnjCB
mzELMAkGA1UEBhMCVVMxEjAQBgNVBAgTCU1pbm5lc290YTEUMBIGA1UEBxMLTWlu
bmVhcG9saXMxFzAVBgNVBAoTDkFzdHJvY29tIENvcnAuMRIwEAYDVQQLEwlQb3dl
ckxpbmsxEjAQBgNVBAMTCVBvd2VyTGluazEhMB8GCSqGSIb3DQEJARYSaGVscEBh
c3Ryb2NvcnAuY29tggMDxOMwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOB
gQB288lTyAfBWtgQUXw0I//TMN+S5QcMtPZvizXpbWaENytySC8qgEY0vi7SZs3G
7OnUmwJbaNDSOOa+ayfubr4mhXglCcp/dZWw0HLJUDxNYhDHYydhOUE9BdT3ZT+w
5tn1J2q0nJT8lEu0hRX4gN5ou8DXqgzg0IUVyxNDyQXtww==
-----END CERTIFICATE-----
""":"ecessa"}
	device_info = certs.get(certreq)

	return(device_info)
