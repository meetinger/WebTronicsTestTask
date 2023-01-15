from schemas.docs_examples.users_schemas_examples import user_full_examples

register_responses_examples = {
    200: {
        "description": "Успешная регистрация",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "Успешная регистрация",
                        "description": "Пример ответа при успешной регистрации",
                        "value": user_full_examples['default']['value']
                    }
                }
            }
        }
    },
    409: {
        "description": "Ошибка регистрации",
        "content": {
            "application/json": {
                "examples": {
                    "email_already_exists": {
                        "summary": "Email уже занят",
                        "description": "Уже существует пользователь с таким email",
                        "value": {"details": "This email already exist!"}
                    },
                    "username_already_exists": {
                        "summary": "Username уже занят",
                        "description": "Уже существует пользователь с таким username",
                        "value": {"details": "This username already exist!"}
                    }
                }
            }
        }
    }
}

get_token_responses_examples = {
    200: {
        "description": "Успешное получение токенов",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "Успешное получение токенов",
                        "description": "Пример ответа при успешной проверке пары username/пароль",
                        "value": {
                            "access_token": "AccessTokenStr",
                            "refresh_token": "RefreshTokenStr",
                            "token_type": "Bearer",
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Ошибка получения токенов",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_credentials": {
                        "summary": "Неправильные данные",
                        "description": "Пример ответа при неправильной паре username/пароль",
                        "value": {
                            "details": "Incorrect username or password"
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Ошибка сервера",
        "content": {
            "application/json": {
                "examples": {
                    "generation_error": {
                        "summary": "Ошибка создания токенов",
                        "description": "Внутренняя ошибка сервера",
                        "value": {
                            "details": "Error while token pair generation"
                        }
                    }
                }
            }
        }
    }
}
refresh_tokens_responses_examples = get_token_responses_examples | {403: {
        "description": "Ошибка получения токенов",
        "content": {
            "application/json": {
                "examples": {
                    "wrong_token_type": {
                        "summary": "Неправильный тип токена",
                        "description": "Пример ответа при неправильном типе токена",
                        "value": {
                            "details": "Wrong token type"
                        }
                    },
                    "token_expired": {
                        "summary": "Токен истёк",
                        "description": "Пример ответа при истёкшем токене",
                        "value": {
                            "details": "Token expired"
                        }
                    }
                }
            }
        }
    }}