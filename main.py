from agents.coguser import *
from agents.frequencies import *

f1 = RadioFrequency(1, 107.9)
f2 = RadioFrequency(2, 103.5)
f3 = RadioFrequency(3, 99.9)
print(f1)
print(f2)
print(f3)

sp = RadioFrequencySpectrum(f1, f2, f3)
c = CognitiveUser(1, -3, 4)
print(c, f"located at {c.position}")
a = AuthorizedUser(2, 2, -2, sp)
print(a, f"located at {a.position}")
c.set_frequency(f1)
print(c)
a.grant_frequency(f3, c)
print(c)

f4 = RadioFrequency(4, 87.9)
assert c.activeFrequency is f3
try:
    a.grant_frequency(f4, c)
except IndexError:
    print("Good!  This call was SUPPOSED to fail.")
else:
    raise IndexError("Something's wrong, I can feel it!")