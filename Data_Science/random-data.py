import random

# Ten iconic movie lines
movie_lines = [
    "Frankly, my dear, I don't give a damn. — Gone With the Wind (1939)",
    "I'm going to make him an offer he can't refuse. — The Godfather (1972)",
    "Here's looking at you, kid. — Casablanca (1942)",
    "May the Force be with you. — Star Wars (1977)",
    "You can't handle the truth! — A Few Good Men (1992)",
    "I'll be back. — The Terminator (1984)",
    "I see dead people. — The Sixth Sense (1999)",
    "Why so serious? — The Dark Knight (2008)",
    "There's no place like home. — The Wizard of Oz (1939)",
    "To infinity and beyond! — Toy Story (1995)"
]

# Randomly select and print one
selected_line = random.choice(movie_lines)
print(f"Movie Quote of the Moment:\n{selected_line}")