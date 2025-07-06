def colorText(text, color):
    colors = {
        "rouge": "\033[91m",
        "vert_fonce": "\033[32;1m",
        "jaune": "\033[93m",
        "bleu": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "orange": "\033[38;5;208m"
    }
    return colors[color] + text + "\033[0m"

# print(colorText("Ce texte est vert foncé et gras", "vert_fonce"))