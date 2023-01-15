set_reaction_responses_examples = {
    200: {
        "description": "Успешный запрос",
        "content": {
            "application/json": {
                "examples": {
                    "set_reaction": {
                        "summary": "Успешная установка реакции",
                        "description": "Пример ответа при успешной установке реакции",
                        "value": {
                            "entity_id": 1,
                            "entity_type": "post",
                            "user_id": 1,
                            "reaction_type": "like",
                            "is_deleted": False
                        }
                    },
                    "unset_reaction": {
                        "summary": "Успешное удаление реакции",
                        "description": "Пример ответа при успешном удалении реакции",
                        "value": {
                            "entity_id": 1,
                            "entity_type": "post",
                            "user_id": 1,
                            "reaction_type": "like",
                            "is_deleted": True
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Неправильные параметры",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Неправильные параметры",
                        "description": "Пример ответа при неправильных параметрах",
                        "value": {
                            "details": "Invalid reaction parameters!"
                        }
                    },
                }
            }
        }
    },
404: {
        "description": "Не найдено",
        "content": {
            "application/json": {
                "examples": {
                    "entity_not_found": {
                        "summary": "Сущность не найдена",
                        "description": "Пример ответа если не найдена сущность с таким типом и id",
                        "value": {
                            "details": "Entity not found!"
                        }
                    },
                    "reaction_not_found": {
                        "summary": "Реакция не найдена",
                        "description": "Пример ответа при попытке удалить несуществующую реакцию",
                        "value": {
                            "details": "Reaction not found!"
                        }
                    },
                }
            }
        }
    },
409: {
        "description": "Конфликт",
        "content": {
            "application/json": {
                "examples": {
                    "self_reaction": {
                        "summary": "Попытка установить реакцию на свою сущность",
                        "description": "Пример ответа если попытаться установить реакцию на свою сущность",
                        "value": {
                            "details": "You can not put a reaction on your <reaction_type>!"
                        }
                    },
                    "reaction_already_exists": {
                        "summary": "Попытка установить реакцию если она уже существует",
                        "description": "Пример ответа если попытаться установить реакцию если она уже существует",
                        "value": {
                            "details": "Reaction with current parameters already set!"
                        }
                    },
                }
            }
        }
    }
}