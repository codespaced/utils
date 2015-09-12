import os

removed = []
for file in os.listdir('.'):
    if os.stat(file).st_size == 0:
        removed.append(file)

print "Removing", len(removed), "files..."
for file in removed:
    try:
        os.remove(file)
    except:
        print "Could not remove", file
