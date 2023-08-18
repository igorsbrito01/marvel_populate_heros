from comics.services import get_character_by_name, count_rows
from comics.models import Character

# add your code here to check any data at the database
# you can use any of the services already implemented
# Run this script at docker using the task_custom service of the docker compose
# check the readme for more informations
# print(get_character_by_name("Spectrum"))
print(count_rows(Character))
