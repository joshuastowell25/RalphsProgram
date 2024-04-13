

def enum(**named_values):
    return type('Enum', (), named_values)

def clearTerminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')