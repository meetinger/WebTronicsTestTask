from core.utils.attachments import get_view_url
from schemas.reactions_schemas import ReactionTypes

default_post_value = {
    "id": 1,
    "text": "Post text",
    "user_id": 1,
    "reactions_count": None,
    "attachment_urls": [get_view_url(fn) for fn in ("attachment1.png", "attachment2.png")]
}

reactions_count_not_empty = {item.name: idx for idx, item in enumerate(ReactionTypes)}

create_post_responses_examples = {
    200: {
        "description": "Успешное создание поста",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Успешное создание поста",
                        "description": "Пример ответа при успешном создании поста",
                        "value": default_post_value
                    }
                }
            }
        }
    }
}
view_post_responses_examples = {
    200: {
        "description": "Успешное получение поста",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Успешное получение поста",
                        "description": "Пример ответа при успешном получении поста",
                        "value": default_post_value | {'reactions_count': reactions_count_not_empty}
                    }
                }
            }
        }
    },
    404: {
        "description": "Пост не найден",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Пост не найден",
                        "description": "Пример ответа когда пост не найден",
                        "value": {
                            "details": "Post not found"
                        }
                    }
                }
            }
        }
    }
}

edit_post_responses_examples = {
    200: {
        "description": "Успешное редактирование поста",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Успешное редактирование поста",
                        "description": "Пример ответа при успешном редактирование поста",
                        "value": default_post_value | {'reactions_count': reactions_count_not_empty}
                    }
                }
            }
        }
    },
    404: {
        "description": "Пост не найден",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Пост не найден",
                        "description": "Пример ответа когда пост не найден",
                        "value": {
                            "details": "Post not found"
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "Пост был создан другим пользователем",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Пост был создан другим пользователем",
                        "description": "Пример ответа когда пост был создан другим пользователем",
                        "value": {
                            "details": "This post was created by another user!"
                        }
                    }
                }
            }
        }
    }
}
