import ast
from typing import Any
from .state import state

def serialize(interaction_identifier: str, *args: Any) -> str:
    packed = repr(args)

    return f"{interaction_identifier}:{packed}"
def deserialize(custom_id: str):
    try:
        if ':' not in custom_id:
            return None, (None,)
        interaction_identifier, raw = custom_id.split(":", 1)
        args = ast.literal_eval(raw)
        if not isinstance(args, tuple):
            args = (args,)

        return interaction_identifier, args

    except Exception as e:
        raise ValueError(f"Invalid serialized interaction: {e}") from e

async def ui_interaction(interaction):

    custom_id = interaction.data.get("custom_id", None)

    if not custom_id:
        return

    interaction_identifier, args = deserialize(custom_id)

    callback = state.interactions.get(interaction_identifier)

    if not callback:
        return

    return await callback(interaction, *args)