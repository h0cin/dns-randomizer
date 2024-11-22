import socket
import threading
import random
import dns.message
import dns.query
import dns.name
import dns.rdatatype
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("dns-proxy")

# Configuration
UPSTREAM_DNS = "8.8.8.8"  # Upstream DNS server (e.g., Google DNS)
LISTEN_ADDRESS = "0.0.0.0"
LISTEN_PORT = 5354


def randomly_uppercase(text):
    """
    Randomly uppercases some letters in a string.
    Args:
        text (str): The input string (e.g., DNS hostname).
    Returns:
        str: The string with random letters uppercased.
    """
    return ''.join(char.upper() if random.choice([True, False]) else char for char in text)


def modify_response(response):
    """
    Modify specific DNS record types in the response.
    Args:
        response (dns.message.Message): The DNS response object.
    Returns:
        dns.message.Message: The modified DNS response object.
    """
    logger.debug("Modifying response if applicable...")
    modified_answers = []
    for rrset in response.answer:
        if rrset.rdtype in [dns.rdatatype.CNAME, dns.rdatatype.NS, dns.rdatatype.SOA]:
            new_rrset = dns.rrset.RRset(rrset.name, rrset.rdclass, rrset.rdtype)
            for rdata in rrset:
                if rrset.rdtype == dns.rdatatype.CNAME:
                    # Randomly uppercase letters in CNAME target
                    original = str(rdata.target)
                    modified_target = dns.name.from_text(randomly_uppercase(original))
                    new_rrset.add(dns.rdata.from_text(rrset.rdclass, rrset.rdtype, str(modified_target)))
                    logger.debug(f"Modified CNAME Record: {original} -> {modified_target}")
                elif rrset.rdtype == dns.rdatatype.NS:
                    # Randomly uppercase letters in NS target
                    original = str(rdata.target)
                    modified_target = dns.name.from_text(randomly_uppercase(original))
                    new_rrset.add(dns.rdata.from_text(rrset.rdclass, rrset.rdtype, str(modified_target)))
                    logger.debug(f"Modified NS Record: {original} -> {modified_target}")
                elif rrset.rdtype == dns.rdatatype.SOA:
                    # Randomly uppercase letters in SOA primary name server
                    original_mname = str(rdata.mname)
                    modified_mname = dns.name.from_text(randomly_uppercase(original_mname))
                    new_rdata = dns.rdata.from_text(
                        rrset.rdclass,
                        rrset.rdtype,
                        f"{modified_mname} {rdata.rname} {rdata.serial} {rdata.refresh} {rdata.retry} {rdata.expire} {rdata.minimum}",
                    )
                    new_rrset.add(new_rdata)
                    logger.debug(f"Modified SOA Record: {original_mname} -> {modified_mname}")
            modified_answers.append(new_rrset)
        else:
            # Keep unmodified records
            modified_answers.append(rrset)

    # Replace answer section
    response.answer.clear()
    response.answer.extend(modified_answers)
    return response


def handle_dns_query(data, addr, server_socket):
    """
    Handle an incoming DNS query and send a response.
    Args:
        data (bytes): The raw DNS query.
        addr (tuple): The address of the client.
        server_socket (socket.socket): The server socket.
    """
    try:
        # Parse the DNS query
        request = dns.message.from_wire(data)
        query_name = request.question[0].name
        query_type = dns.rdatatype.to_text(request.question[0].rdtype)
        logger.debug(f"Received query: {query_name} (Type: {query_type}) from {addr}")

        # Forward the query to the upstream DNS server
        logger.debug(f"Forwarding query to upstream DNS: {UPSTREAM_DNS}")
        upstream_response = dns.query.udp(request, UPSTREAM_DNS)
        logger.debug(f"Received upstream response: {upstream_response}")

        # Modify the response if it contains specific record types
        if query_type in ["CNAME", "NS", "SOA"]:
            upstream_response = modify_response(upstream_response)

        # Send the modified response back to the client
        server_socket.sendto(upstream_response.to_wire(), addr)
        logger.debug(f"Sent modified response to {addr}")

    except Exception as e:
        logger.error(f"Error handling query from {addr}: {e}")


def start_dns_server():
    """
    Start the DNS proxy server.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((LISTEN_ADDRESS, LISTEN_PORT))
    logger.info(f"DNS proxy server listening on {LISTEN_ADDRESS}:{LISTEN_PORT}")

    while True:
        try:
            # Receive DNS query
            data, addr = server_socket.recvfrom(512)
            # Handle the query in a new thread
            threading.Thread(target=handle_dns_query, args=(data, addr, server_socket)).start()
        except KeyboardInterrupt:
            logger.info("Shutting down the DNS proxy server.")
            break
        except Exception as e:
            logger.error(f"Error: {e}")

    server_socket.close()


if __name__ == "__main__":
    start_dns_server()
