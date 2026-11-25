import os, sys, zipfile
src, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for dp, dn, fn in os.walk(src):
        dn.sort()
        for f in sorted(fn):
            full = os.path.join(dp, f)
            arc = "Noorjahan-WebUI/" + os.path.relpath(full, src).replace(os.sep, "/")
            z.write(full, arc)
