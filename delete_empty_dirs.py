"""Delete empty folders inside a directory tree."""

import os, sys

def find_empties(rootdir):

    removed = []
    one = []

    for root, dirs, files in os.walk(rootdir, topdown=False):
        for name in dirs:
            target = os.path.join(root, name)
            try:
                f = os.listdir(target)
            except:
                continue
            if not f:
                os.rmdir(target)
                removed.append(target)
            elif len(f) == 1:
                if f[0] == ".picasa.ini":
                    os.remove(os.path.join(target, f[0]))
                    os.rmdir(target)
                    removed.append(os.path.join(target, f[0]))
            elif len(f) < 5:
                one.append((target, len(f)))

    print "Removed:"
    print "\n".join(removed)

    print "Nearly Empty:"
    for d in one:
        print d[1], d[0]


if __name__ == '__main__':

    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "."

    find_empties(root)