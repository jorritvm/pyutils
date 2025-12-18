"""
This module will test argument parsing using Pydantic and argparse.
The user has to define an pydantic model with the applications parameters, default values, types and descriptions.
Example:
    from pydantic import BaseModel, Field
    import smartargs

    class Arguments(BaseModel):
        name: str = "myname"
        age: int = 30
        color: str = Field(default="red", description="Color of the item")

The user also has to call get_config with the model as argument at the start of the application.
    config = smartargs.get_config(Arguments)

This module will make sure all arguments can be passed via command line arguments.
Arguments that were not passed will take the default value from the model.

Example usage:
> smartargs.py
Arguments(name='myname', age=30, color='red')

> smartargs.py --name override
Arguments(name='override', age=30, color='red')

> smartargs.py --name qsdf --age six
usage: smartargs.py [-h] [--name NAME] [--age AGE] [--color COLOR]
smartargs.py: error: argument --age: invalid int value: 'six'
"""

import argparse

__all__ = ["get_config"]

def add_model(parser, model):
    "Add Pydantic model to an ArgumentParser"
    fields = model.model_fields
    for name, field in fields.items():
        parser.add_argument(
            f"--{name}",
            dest=name,
            type=field.annotation,
            default=field.default,
            help=field.description,
        )

def get_config(pydantic_model):
    parser = argparse.ArgumentParser()
    add_model(parser, pydantic_model)
    args = parser.parse_args()
    config = pydantic_model(**vars(args))
    return config

if __name__ == "__main__":
    from pydantic import BaseModel, Field

    class Arguments(BaseModel):
        name: str = "myname"
        age: int = 30
        color: str = Field(default="red", description="Color of the item")

    config = get_config(Arguments)
    print(repr(config))
    print(config.name)