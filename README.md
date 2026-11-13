# Cab Pool Matcher

Command line app to put BITS students into shared cabs to Delhi / Jaipur. Seniors get seats first.

## Running

```
pip install -r requirements.txt
python main.py
```

Menu: add request, see waiting + cabs, find matches (preview), dispatch a cab, quit. Esc goes back / quits.

## Cab file (cabs.csv)

```
driver_name,seats,destination,time_slot
Ramesh Kumar,4,Delhi,Morning
```

seats is 1 to 4, destination is Delhi or Jaipur, time_slot is Morning/Afternoon/Evening/Night. Bad rows are skipped with a message. Cabs are used in the order they appear in the file.

## Saving

State is saved to `state.json` after every change (and on quit), so Ctrl+C loses nothing. I used JSON because it is readable and can be opened/edited by hand, pickle is not readable and can run code when loaded. The file is written to a temp file and then renamed so a crash while saving can't break the old save. Every request keeps a sequence number so people keep their place in line after a restart. If the file is missing, broken, or doesn't match cabs.csv, the app starts fresh and says so.

## Tricky situations

1. **Half-empty cab**: the user can dispatch any open cab. It just leaves with whoever is waiting (shown as e.g. 2/4). The empty seats are lost, the cab can't be used again.
2. **No cabs left**: the request is still accepted and stays in the queue for its trip, with a message that there is no open cab right now. Nobody is removed from the queue unless they get into a cab.
3. **Same year**: each queue is a heap of `(-year, time requested, sequence number, request)`. Same year means the earlier time wins, and the sequence number breaks exact ties, so the RideRequest objects are never compared.
4. **1000 requests waiting** (n = waiting in a trip):
   - add one request: O(log n) heap push. All 1000: O(n log n).
   - dispatch one cab (up to 4 students): O(k log n) with k <= 4, so O(log n). The cab is taken from the front of a deque in O(1).
   - find open cab for a trip: O(1), open cabs are kept in a dict keyed by (destination, time) with a deque per trip.
   - preview is O(m log n) for m open seats of a trip, it only reads the heap.
