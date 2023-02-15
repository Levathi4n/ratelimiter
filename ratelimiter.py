import time
from collections import defaultdict

RATE_LIMIT = 100  # Maximum number of requests allowed per IP per minute
BLOCK_DURATION = 60 * 60  # Block IPs for 1 hour after reaching the rate limit
CLEANUP_INTERVAL = 60  # Check for expired IPs every minute

request_counts = defaultdict(int)
blocked_ips = {}

def is_request_allowed(ip):
    if ip in blocked_ips:
        # Check if the IP is still blocked
        if time.time() - blocked_ips[ip] > BLOCK_DURATION:
            # IP is no longer blocked, reset request count and remove from blocked IPs
            request_counts[ip] = 0
            del blocked_ips[ip]
        else:
            # IP is still blocked, deny request
            return False
    request_counts[ip] += 1
    if request_counts[ip] > RATE_LIMIT:
        # IP has reached rate limit, block IP
        blocked_ips[ip] = time.time()
        return False
    return True

# Periodically clean up request counts and blocked IPs
while True:
    for ip in list(request_counts.keys()):
        if time.time() - blocked_ips.get(ip, 0) > BLOCK_DURATION:
            del request_counts[ip]
    time.sleep(CLEANUP_INTERVAL)
