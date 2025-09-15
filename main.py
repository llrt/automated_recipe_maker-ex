from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.utils.pprint import pprint_run_response
import asyncio
import os

# Agno expects to be a gen AI key set as os env var..
# Retrieving from Elixir's external context, decoding as normal str (from Elixir it comes as a byte string) and setting artificially as an os env var
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY.decode('utf-8')  
print("Env vars loaded..")

# Define LLM model
MODEL_ID = "gemini-2.5-flash"

# parameters
print('Setting up parameters..')
dish_type="Chicken and Salad"
location="Rio de Janeiro/Brazil"
family_size=4
team_size=2
language="Portuguese"

print('Setting up agents..')
chef = Agent(
    model=Gemini(id=MODEL_ID),
    name="Chef",
    role="The Renowned Chef",
    description=f"""
      As a veteran chef, you've worked in many tasteful recipes. You are
      very talented and love to create special recipes for your clients,
      delivering remarkable experiences.
      Your goal is to craft beautiful and visually appealing {dish_type} recipes for a family of {family_size} people, focusing in delivering a great and tasteful experience.
      Your meals are easy to understand and make, even for a small team of {team_size} cuisine workers.
      You provide the list of needed ingredients and step-by-step directions to make the recipe.
    """,
    instructions=f"""
      Create a {dish_type} recipe for a family of {family_size} people.
    """,
    expected_output=f"""
      A detailed recipe, with a list of ingredients and step-by-step directions, an estimated number of servings, and estimated time of preparation.    
    """,
    markdown=True,
)

food_critique = Agent(
    model=Gemini(id=MODEL_ID),
    name="Food Critique",
    role="Food Critic Specialist",
    description=f"""
      You are a renowned food critique, who has appraised many dishes, provided many valuable insights
      that were used to perfect the recipes. You are very pragmatic and has a keen eye for recipes
      that are too long or difficult for a team of {team_size} workers to make.

      Your goal is to critique a {dish_type} recipe, informing if it is too complex or less tasteful. You provide valueable insights for the chef, indicating if the provided recipe could be simpler,
      use more ingredients commonly found in {location} or demand less time to make. 
      You also take a good look at the recipe and evaluate if the number of servings is 
      sufficient for a family of {family_size} people. If you consider the current recipe 
      is not good yet, please send the recipe back for the Chef for adjustments. If you approve the recipe, please send the recipe for the nutritionist to assess its calories and nutrition facts.
    """,
    instructions=f"""
      Thoroughly evaluate the provided recipe, identifying if it is too complex or less tasteful.
    """,
    expected_output=f"""
      A detailed critique, indicating CLEARLY if the recipe is approved or not. If not approved, insights and recommendations MUST be provided.
    """,
    markdown=True,
)

nutritionist = Agent(
    model=Gemini(id=MODEL_ID),
    name="Nutritionist",
    role="Nutritionist",
    description=f"""
      You are a passionate nutritionist that has worked together with chefs in making
      healthy and delicious meals.
      Your goal is to assess a recipe's table of nutrition facts, including calories and other
      important facts (carbs, fat, etc). If you find out the recipe is too fatty or
      caloric, please send the recipe back to the Chef and ask for a adjustment, focusing
      in healthy recipes.
    """,
    instructions=f"""
      Evaluate the provided recipe, identifying its nutrition facts.
    """,
    expected_output=f"""
      A detailed table of nutrition facts, including calories, carbs, fat, vitamins, etc.
    """,
    markdown=True,
)

writer = Agent(
    model=Gemini(id=MODEL_ID),
    name="Writer",
    role="Recipe Writer",
    description=f"""
      You are a writer specialized in recipe writing, who knows how to write good recipes in {language}.
      Your goal is to compile a final recipe with all the information received from Chef and 
      Nutritionist. Be careful to use simple language, easy to understand, do not use special terms,
      only common ones. Also, do write the final recipe in the language {language}.
    """,
    instructions=f"""
      Write the final recipe in {language}. You MUST use simple language. Do not use special terms, only common ones.
    """,
    expected_output=f"""
      A detailed recipe, containing sections for ingredients, servings, directions and nutrition facts, in this order. The recipe MUST be written in {language}. 
    """,
    markdown=True,
)

print('Setting up team..')
team = Team(
  name="Cooking Team",
  model=Gemini(id=MODEL_ID), 
  members=[
    chef,
    food_critique,
    nutritionist,
    writer
  ],
  instructions=[
    "You are a discussion master.",
    "You have to stop the discussion when you think the team has reached a consensus.",
  ],
  show_members_responses=True,
  markdown=True
)

print('Running actual work..')
response = team.run(
  input=f"Please craft a {dish_type} in {language} for a family of {family_size}. Respond with only the recipe, do not make an introduction."
)

# Print the response in markdown format
pprint_run_response(response, markdown=True)

response.content