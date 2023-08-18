from comics.services import count_rows
from comics.models import Character
from task import populate_character_and_assosiations

populate_character_and_assosiations("Spectrum")
num_characters = count_rows(Character)

print(" ")
print(f"There are {num_characters} rows at the character table")
print(" ")