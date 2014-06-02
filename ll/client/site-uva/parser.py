import sys

def logparser():
    for line in sys.stdin:
        try:
            parts = line.split()
            if not parts: continue
            tm = " ".join(parts[0:2])
            url = parts[10]
            ref = parts[11][1:-1]
            yield tm, url, ref
        except:
            continue
