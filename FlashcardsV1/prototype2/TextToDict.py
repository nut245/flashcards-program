dictionary = {}
count = 0
with open("KeyTerms.txt") as file:
    for line in file:
        try:
            (key, val) = line.split(' : ')
        except ValueError:
            print(f"was unable to unpack line {count+1} : '{line[:-1]}'", end='\n\n')
        dictionary[key] = val[:-1]
        count += 1