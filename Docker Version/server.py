from dnslib import DNSRecord, RR, QTYPE, A
from dnslib.server import DNSServer, BaseResolver
from collections import Counter

# List of domains we want to block
blocked_domains = []

with open("AdsBestKnownDomains.txt", "r") as f:
    for line in f:
        domain = line.split()[0]
        blocked_domains.append(domain)

g = open("ADblocker_Results.txt", "w")

actualBlockedDomains = []


class DNSAdBlock(BaseResolver):
    def resolve(self, request, handler):

        dns_record = request
        # print(dns_record)
        domain_name = str(dns_record.q.qname)  # Requested domain name
        # print(f"Request for: {domain_name}")

        # Check if the domain name is in the list of blocked domains
        if any([blocked_domain in domain_name for blocked_domain in blocked_domains]):
            # If the domain is blocked, return IP address 0.0.0.0
            reply = dns_record
            g.write(f"Request for: {domain_name}" + '\n')
            reply.add_answer(RR(domain_name, QTYPE.A, rdata=A('0.0.0.0')))
            # RR is the Resource Record and it's a tuple of the form (name, type, rclass, ttl, rdata)
            print('\n')
            print(f"Blocked Response: {reply} \n")
            print('')
            g.write('\n')
            g.write(f"Blocked Response: {reply} \n")
            g.write('\n')
            actualBlockedDomains.append(domain_name)
        else:
            # Send the request to DNS server 8.8.8.8 and receive the response
            response = DNSRecord.parse(request.send('8.8.8.8', 53))
            # Return the response to the client
            reply = request.reply()
            reply.rr = response.rr
            print(f"Response: {reply}")

        return reply


try:
    dns_server = DNSServer(resolver=DNSAdBlock(), port=53, address="127.0.0.1")
    dns_server.start()
except KeyboardInterrupt as e:
    dns_server.stop()
    gf = open("ADblocker_Statistics.txt", "w")
    print("\n \n \n \n")
    print('Server stopped!', flush=True)
    print('')
    print('Statistics: ')
    print('')
    gf.write('Statistics: ' + '\n')
    gf.write('\n')

    countGoogle = 0
    countFacebook = 0
    for domain in actualBlockedDomains:
        if 'google' in domain:
            countGoogle = countGoogle + 1
        elif 'facebook' in domain:
            countFacebook = countFacebook + 1
        elif 'fbcdn' in domain:
            countFacebook = countFacebook + 1
        elif 'fbsbx' in domain:
            countFacebook = countFacebook + 1

    print("Total number of blocked domains is: " + str(len(actualBlockedDomains)))
    print('')
    print("Number of blocked domains containing 'Facebook' is: " + str(countFacebook))
    print("Number of blocked domains containing 'Google' is: " + str(countGoogle))
    print('')
    print('')
    print('')
    print('Top occurrences: ')
    print('')
    gf.write("Total number of blocked domains is: " + str(len(actualBlockedDomains)) + '\n')
    gf.write('\n')
    gf.write("Number of blocked domains containing 'Facebook' is: " + str(countFacebook) + '\n')
    gf.write("Number of blocked domains containing 'Google' is: " + str(countGoogle) + '\n')
    gf.write('\n')
    gf.write('\n')
    gf.write('Top occurrences: ' + '\n')

    top_occurrences = Counter(actualBlockedDomains).most_common(10)
    i = 0
    k = 1
    while i < len(top_occurrences):
        print(f"{k}. {top_occurrences[i][0]} - {top_occurrences[i][1]} occurrences")
        gf.write(f"{k}. {top_occurrences[i][0]} - {top_occurrences[i][1]} occurrences" + '\n')
        i = i + 1
        k = k + 1

    g.close()
