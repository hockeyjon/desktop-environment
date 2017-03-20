
with open("bccStatement.txt") as f:
    content = f.readlines()
    
for line in content:
    if "Balance Forward" in line or "Payment" in line:
        continue
    elements = line.split("\t")
    date = elements[0]
    description = elements[3]
    amount = elements[8].rstrip('\r\n')
    print date + "\t: " + description + "\t: " + amount
