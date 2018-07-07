import re

m = '12平米'

x = re.findall(r'\d+',m)
print(x)