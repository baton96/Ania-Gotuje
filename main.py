import re
import spacy

nlp = spacy.load("en_core_web_lg")

with open("food.txt", "r") as f:
    ingredients = f.read().splitlines() + ["broth", "olive oil"]
    ingredients = list(nlp.pipe(ingredients))

recipe = [
    "1 cup long-grain white rice - 240 g (dry weight)",
    "a little over 1.5 cups of broth, e.g., chicken stock - 400 ml",
    "half a cup of tomato puree, e.g., passata - 125 ml",
    "40 g onion or 3 small shallots (can be omitted)",
    "2 cloves of garlic - about 10 g (or a flat tablespoon of dried garlic)",
    "2 tablespoons of olive oil or other oil for frying",
    "spices: half a teaspoon of chili powder or a piece of fresh pepper, optionally salt and pepper",
    "600 g ground beef - e.g., shoulder or neck",
    "2 tablespoons of olive oil or other oil for frying",
    "1 can of whole or diced tomatoes - about 400 g",
    "1 can of red kidney beans - about 200 g pickles",
    "3 cloves of garlic - about 15 g",
    "1 medium onion - about 150 g",
    "Spices: 2 teaspoons of oregano; 1 teaspoon of chili powder; ½ teaspoon each of ground cumin, salt, and pepper",
    "8 large tortillas - preferably 30 cm in diameter",
    "80 g of yellow cheese, cubed mozzarella, or cheddar cheese",
    "2 large, ripe avocados - can be omitted",
    "To serve: sour cream; pickled jalapeños; fresh lime juice; a handful of fresh cilantro",
]
lines = []
for line in recipe:
    if ":" in line:
        lines.extend(
            arg
            for arg in re.split(r"(,|;|and) ", line.replace("and ", "").split(": ")[1])
            if arg not in (";", ",", "and")
        )
    # elif " or " in line: lines.append(line.split(" or ")[1])
    else:
        lines.append(line)
texts = []
for line in lines:
    line = line.removeprefix("a little over ")
    line = (
        line.lstrip("½0123456789/-,. ")
        .removeprefix("g ")
        .removeprefix("ml ")
        .removeprefix("kg ")
        .replace(", ", " ")
    )
    line = line.split(" -")[0]
    line = re.sub(r"(whole|fresh|pickled|diced|grated|ripe|powder) ?", "", line)
    line = re.sub(
        r"(level )?(glass|litre|cup|can|tablespoon|teaspoon|clove|stalk|handful|each)s? ?",
        "",
        line,
    )
    line = line.replace("of ", "")
    if line.startswith("or "):
        line = line.split("or ")[1]
    line = line.split(" or ")[0]
    line = re.sub(
        r"(no more than|full|half|flat|whole|small|large|medium-sized|medium) ",
        "",
        line,
    )
    line = line.removeprefix("a ")
    line = re.sub(r"e\.g\..*", "", line)
    texts += [line]

texts = list(nlp.pipe(texts))
for text in texts:
    print(text, "|", max(ingredients, key=text.similarity))
