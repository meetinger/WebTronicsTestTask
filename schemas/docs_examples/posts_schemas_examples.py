import copy

from core.utils.attachments import get_view_url
from schemas.reactions_schemas import ReactionTypes

post_out_without_reaction_count_examples = {
    "default": {
        "summary": "Данные поста",
        "description": "Пример данных поста",
        "value": {
            "id": 1,
            "text": "Post text",
            "user_id": 1,
            "reactions_count": None,
            "attachment_urls": [get_view_url(fn) for fn in ("attachment1.png", "attachment2.png")]}
    }
}

_reactions_count_not_empty = {item.name: idx for idx, item in enumerate(ReactionTypes)}

post_out_with_reaction_count_examples = copy.deepcopy(post_out_without_reaction_count_examples)
post_out_with_reaction_count_examples['default']['value']['reactions_count'] = _reactions_count_not_empty
