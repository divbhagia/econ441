"""Copy the rendered site from the build dir into docs/, and verify it landed.

Dropbox restores files it has already synced after `rm -rf docs`, so a plain
copy can silently leave stale pages behind -- it has twice, most recently
keeping week-old slide decks while every other file updated. This copies,
compares every file byte for byte, and re-copies the stragglers until they
match (or gives up loudly rather than pretending the publish worked).
"""
import filecmp, hashlib, pathlib, shutil, sys, time

src = pathlib.Path(sys.argv[1]).resolve()
dst = pathlib.Path("docs").resolve()

def differing():
    out = []
    for f in src.rglob("*"):
        if not f.is_file():
            continue
        o = dst / f.relative_to(src)
        if not o.exists() or not filecmp.cmp(f, o, shallow=False):
            out.append(f.relative_to(src))
    return out

for attempt in range(1, 6):
    for rel in (differing() if attempt > 1 else [f.relative_to(src) for f in src.rglob("*") if f.is_file()]):
        o = dst / rel
        o.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / rel, o)
    time.sleep(6 * attempt)          # let Dropbox do its reverting, then look
    left = differing()
    if not left:
        print(f"    docs/ verified against the build ({attempt} pass{'es' if attempt > 1 else ''})")
        break
    print(f"    pass {attempt}: {len(left)} file(s) still stale, retrying")
else:
    print("    NOT PUBLISHED -- these files never took:", file=sys.stderr)
    for rel in left:
        print("      " + str(rel), file=sys.stderr)
    sys.exit(1)

# files docs/ has that the build does not (left over from an earlier render)
extra = [f for f in dst.rglob("*") if f.is_file()
         and not (src / f.relative_to(dst)).exists()]
for f in extra:
    f.unlink()
if extra:
    print(f"    removed {len(extra)} file(s) left over from an earlier build")
