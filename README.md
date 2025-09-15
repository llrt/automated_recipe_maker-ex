# automated_recipe_maker-ex
This is an experimental AI/agentic automated recipe maker, made with Elixir + Livebook + PythonX/Agno.

It is mostly a port of [my Agno one](https://github.com/llrt/agno_automated_recipe_maker), just learn Elixir, Livebook and try Python integration with PythonX.

The work is done by 4 agents:

- chef: the one that crafts the initial recipe, focusing in a beautiful and visually appealing dish
- food_critic: the one that critics the recipe, assessing if it is too complex or less tasteful
- nutritionist: the one that compiles the nutrition facts about the recipe, assessing if it is too fatty or caloric
- writer: the one that writes the final recipe, in the desired (natural) language

Note:

The recipes created consider only ingredients found in the given location
The recipes are created in the given (natural) language