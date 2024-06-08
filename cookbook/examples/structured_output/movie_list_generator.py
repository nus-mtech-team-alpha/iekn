from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint
from phi.assistant import Assistant


class MovieScript(BaseModel):
    setting: str = Field(..., description="Provide a nice setting for a blockbuster movie.")
    ending: str = Field(..., description="Ending of the movie. If not available, provide a happy ending.")
    genre: str = Field(..., description="Genre of the movie.")
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(..., description="3 sentence storyline for the movie. Make it exciting!")


class MovieScripts(BaseModel):
    items: List[MovieScript] = Field(..., description="List of movie scripts.")


movie_assistant = Assistant(
    description="You help people write movie ideas.",
    instructions=[
        "Given a setting by the user, respond with 3 movie script with different genres.",
    ],
    output_model=MovieScripts,
)

pprint(movie_assistant.run("New York"))
