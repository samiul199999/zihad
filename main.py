import threading
import time
import requests
from datetime import datetime

# --- Logic Configuration ---
def run_single(name, url, interval, timeout=None):
    # Logic from JS: timeout calculation
    if not timeout:
        # Math.min(Math.max(interval * 0.8, 500), 10000)
        calc_timeout = max(interval * 0.8, 500)
        timeout = min(calc_timeout, 10000) / 1000.0 # Convert ms to seconds for Python requests
    else:
        timeout = timeout / 1000.0

    # Logic from JS: nextCall initialization
    next_call = time.time() * 1000 # Use ms for calculation to match JS logic

    while True:
        start = time.time()
        try:
            # Python requests timeout is in seconds
            res = requests.get(url, timeout=timeout)
            
            took = time.time() - start
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{name}] {url} -> {res.status_code} ({took:.2f}s)")
            
        except Exception as e:
            took = time.time() - start
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{name}] Error: {str(e)} ({took:.2f}s)")

        # Logic from JS: nextCall += interval * 700
        next_call += (interval * 700)
        
        current_time_ms = time.time() * 1000
        sleep_time_ms = next_call - current_time_ms
        
        # If sleep time is positive, sleep. 
        if sleep_time_ms > 0:
            time.sleep(sleep_time_ms / 1000.0) # Convert back to seconds for sleep
        else:
            # If we are behind schedule, reset next_call (mirroring JS logic)
            next_call = time.time() * 1000

# --- URL Groups ---
bot1_urls = [
    "https://siyamahmmed.shop/zihadnr.php",
    "https://siyamahmmed.shop/jihadnr.php",
    "https://siyamahmmed.shop/isahaknr.php",
]

bot2_urls = [
    "https://siyamahmmed.shop/jihadr.php",
    "https://siyamahmmed.shop/samiulrr.php",
    "https://siyamahmmed.shop/zihadur.php",
]

bot3_urls = [f"https://zihadbd.shop/clientbot{i+1}.php" for i in range(17)]
bot4_urls = [f"https://zihadbd.shop/clientbotn{i+1}.php" for i in range(7)]
hadiji_url = ["https://siyamahmmed.shop/hadiji.php"]
jimkar_url = ["https://siyamahmmed.shop/jimkar.php"]

# --- Thread Starter Helper ---
def start_threads(urls, interval, prefix):
    for i, url in enumerate(urls):
        name = f"{prefix}-{i + 1}"
        t = threading.Thread(target=run_single, args=(name, url, interval))
        t.daemon = True # Daemon threads exit when the main program exits
        t.start()

# --- Execution ---
if __name__ == "__main__":
    start_threads(bot1_urls, 16, "bot1")
    start_threads(bot2_urls, 6, "bot2")      # Changed from 10 -> 6
    start_threads(bot3_urls, 6, "clientbot") # Changed from 10 -> 6
    start_threads(bot4_urls, 16, "clientbotn")
    start_threads(hadiji_url, 5, "hadiji")
    start_threads(jimkar_url, 2, "jimkar")

    # Keep main thread alive
    while True:
        time.sleep(60)
