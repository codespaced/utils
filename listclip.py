import subprocess
import clipboard

data = clipboard.paste().split()
txt = "('" + ("','").join(data) + "')"
clipboard.copy(txt)

print(txt)