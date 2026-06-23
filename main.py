import asyncio

from game.loop import run

# we use asyncio.run to run the main game loop so it works with pygbag in wasm
asyncio.run(run())
