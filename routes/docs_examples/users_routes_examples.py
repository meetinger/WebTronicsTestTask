import schemas.docs_examples.posts_schemas_examples as posts_schemas_examples
import schemas.docs_examples.users_schemas_examples as users_schemas_examples

info_current_user_responses_examples = {
    200: {
        "description": "Успешное получение информации пользователя",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Полная информация пользователя",
                        "description": "Пример ответа при успешном получении информации пользователя",
                        "value": users_schemas_examples.user_full_examples['default']['value']
                    }
                }
            }
        }
    },
}

info_user_by_id_responses_examples = {
    200: {
        "description": "Успешное получение информации пользователя",
        "content": {
            "application/json": {
                "examples": {
                    "user_full": {
                        "summary": "Полная информация пользователя",
                        "description": "Пример ответа при успешном получении информации пользователя, если user_id совпадает с id текущего пользователя",
                        "value": users_schemas_examples.user_full_examples['default']['value']
                    },
                    "user_limited": {
                        "summary": "Ограниченная информация пользователя",
                        "description": "Пример ответа при успешном получении информации пользователя, если user_id не совпадает с id текущего пользователя",
                        "value": users_schemas_examples.user_limited_examples['default']['value']
                    }
                }
            }
        }
    },
    404: {
        "description": "Не найдено",
        "content": {
            "application/json": {
                "examples": {
                    "user_full": {
                        "summary": "Пользователь не найден",
                        "description": "Пример ответа если пользователь не найден",
                        "value": {
                            "details": "User not found"
                        }
                    },
                }
            }
        }
    }
}

posts_responses_examples = {
    200: {
        "description": "Успешное получение постов пользователя",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Посты пользователя",
                        "description": "Пример ответа при успешном получении постов пользователя",
                        "value": [
                            posts_schemas_examples.post_out_without_reaction_count_examples['default']['value'] | {
                                'id': i} for i in range(1, 3)]
                    }
                }
            }
        }
    },
}
