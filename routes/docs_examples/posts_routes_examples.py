import schemas.docs_examples.posts_schemas_examples as posts_schemas_examples

create_post_responses_examples = {
    200: {
        "description": "Успешное создание поста",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Успешное создание поста",
                        "description": "Пример ответа при успешном создании поста",
                        "value": posts_schemas_examples.post_out_without_reaction_count_examples['default']['value']
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
                        "value": posts_schemas_examples.post_out_with_reaction_count_examples['default']['value']
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
                        "value": posts_schemas_examples.post_out_with_reaction_count_examples['default']['value']
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
