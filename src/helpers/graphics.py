import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header(title: str, description: str = ""):
    width = 66
    print("\n\n")
    print("╔" + "═" * width + "╗")
    print("║{:^{width}}║".format("", width=width))  # margem superior
    print("║{:^{width}}║".format(title, width=width - 1))
    if description:
        print("║{:^{width}}║".format(description, width=width))
    print("║{:^{width}}║".format("", width=width))  # margem inferior
    print("╠" + "═" * width + "╣")
    print("║{:^{width}}║".format("\\c para cancelar   \\v para voltar", width=width))
    print("╚" + "═" * width + "╝")
    print("\n\n")