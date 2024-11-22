# DNS Proxy Server with Random Uppercase Modifications

This is a simple DNS proxy server built using Python and `dnspython`. It intercepts DNS queries, forwards them to an upstream DNS server, and modifies the responses for specific record types (`CNAME`, `NS`, and `SOA`) by randomly uppercasing some letters in the returned hostnames.

## Features

- Intercepts and processes DNS queries.
- Modifies `CNAME`, `NS`, and `SOA` records in responses.
- Randomly uppercases letters in the returned hostnames.
- Logs details of incoming queries, upstream responses, and modifications.

## Requirements

- Python 3.8 or higher
- `dnspython` library

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/dns-proxy.git
cd dns-proxy
```
# DNS Proxy Server with Random Uppercase Modifications

This is a simple DNS proxy server built using Python and `dnspython`. It intercepts DNS queries, forwards them to an upstream DNS server, and modifies the responses for specific record types (`CNAME`, `NS`, and `SOA`) by randomly uppercasing some letters in the returned hostnames.

## Features

- Intercepts and processes DNS queries.
- Modifies `CNAME`, `NS`, and `SOA` records in responses.
- Randomly uppercases letters in the returned hostnames.
- Logs details of incoming queries, upstream responses, and modifications.

## Requirements

- Python 3.8 or higher
- `dnspython` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dns-proxy.git
   cd dns-proxy

2. Build the container using docker-compose:
```bash
docker-compose build
```

3. Start the container using docker-compose:
```bash
docker-composte up -d
```

## Usage

```
bash
dig @127.0.0.1 example.com CNAME
dig @127.0.0.1 example.com NS
dig @127.0.0.1 example.com SOA
```

### Example Output

The server logs incoming queries, upstream responses, and modifications. Example:

```
2024-11-22 10:00:00 - DEBUG - Received query: example.com. (Type: CNAME) from ('127.0.0.1', 54021)
2024-11-22 10:00:01 - DEBUG - Modified CNAME Record: ns1.example.com -> Ns1.ExAMPle.CoM
2024-11-22 10:00:02 - DEBUG - Sent modified response to ('127.0.0.1', 54021)
```

### Modified Response

For a CNAME query:

```
Original Response: ns1.example.com
Modified Response: Ns1.ExAMPle.CoM
```
