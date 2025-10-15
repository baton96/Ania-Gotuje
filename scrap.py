import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

NUMBER_OF_PAGES = 53


async def get_recipe_names():
    recipe_names = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, NUMBER_OF_PAGES):
            async with session.get(
                f"https://aniagotuje.pl/pomysl-na/obiad/strona/{i}"
            ) as response:
                soup = BeautifulSoup(await response.text(), "lxml")
                articles = soup.find_all("article")
                for article in articles:
                    recipe_names += [article.find("a")["href"].split("/")[-1]]
    return recipe_names


async def scrap():
    prefix2name = {
        "Wartość energetyczna": "energy",
        "Węglowodany": "carbs",
        "- W tym cukry": "sugar",
        "Białko": "protein",
        "Tłuszcze": "fat",
    }
    recipes = {}
    recipe_names = await get_recipe_names()
    async with aiohttp.ClientSession() as session:
        for recipe_name in recipe_names:
            async with session.get(
                f"https://aniagotuje.pl/przepis/{recipe_name}"
            ) as response:
                print(recipe_name)
                soup = BeautifulSoup(await response.text(), "lxml")
                ingredients_pl = [
                    ingredient.text
                    for ingredient in soup.find_all(
                        "span", {"itemprop": "recipeIngredient"}
                    )
                ]
                ingredients = (
                    GoogleTranslator(source="pl", target="en")
                    .translate("\n".join(ingredients_pl))
                    .splitlines()
                )

                nutrition = {}
                for span in soup.find_all("span", {"class": "nutrition-item"}):
                    span = span.text.strip().replace("\n", " ")
                    for prefix in [
                        "Wartość energetyczna",
                        "Węglowodany",
                        "- W tym cukry",
                        "Białko",
                        "Tłuszcze",
                    ]:
                        if span.startswith(prefix):
                            nutrition_name = prefix2name[prefix]
                            nutrition[nutrition_name] = span.split()[-2]
                if nutrition:
                    recipes[recipe_name] = {
                        "ingredients": ingredients,
                        "nutrition": nutrition,
                    }
                else:
                    recipes[recipe_name] = {"ingredients": ingredients}
        with open("recipes.json", "w") as f:
            json.dump(recipes, f, indent=1, ensure_ascii=False)


asyncio.run(scrap())
