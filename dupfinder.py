# feito por: maquinzz
import argparse, hashlib, json, os, sys
from collections import defaultdict

MAX_FILE = 256 * 1024 * 1024
CHUNK = 1024 * 1024

def sha1_file(path: str) -> str | None:
    h = hashlib.sha1()
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(CHUNK)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()
    except OSError:
        return None

def scan(root: str, min_size: int = 1) -> list[dict]:
    by_size: dict[int, list[str]] = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                if not os.path.isfile(full) or os.path.islink(full):
                    continue
                st = os.stat(full)
                if st.st_size < min_size or st.st_size > MAX_FILE:
                    continue
                by_size[st.st_size].append(full)
            except OSError:
                continue
    groups: dict[str, list[str]] = defaultdict(list)
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        for p in paths:
            dg = sha1_file(p)
            if dg:
                groups[dg].append(p)
    dups = []
    for digest, paths in groups.items():
        if len(paths) >= 2:
            dups.append({"size": os.stat(paths[0]).st_size, "sha1": digest, "paths": sorted(paths)})
    dups.sort(key=lambda d: (-d["size"], d["sha1"]))
    return dups

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, help="directory to scan")
    p.add_argument("--out", help="output json file")
    p.add_argument("--min-size", type=int, default=1, help="min file size to consider")
    a = p.parse_args()
    if not os.path.isdir(a.root):
        print("bad_root", file=sys.stderr); sys.exit(1)
    if a.min_size < 0:
        print("bad_min_size", file=sys.stderr); sys.exit(1)
    dups = scan(a.root, a.min_size)
    payload = json.dumps({"root": a.root, "groups": dups, "total_dups": sum(len(d["paths"]) for d in dups)}, indent=2, ensure_ascii=False)
    if a.out:
        try:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(payload + "\n")
        except OSError as e:
            print(f"write_failed: {e}", file=sys.stderr); sys.exit(2)
    else:
        print(payload)
    sys.exit(0)

if __name__ == "__main__":
    main()
