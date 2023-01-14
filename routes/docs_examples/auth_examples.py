from schemas.docs_examples.users_examples import user_in_examples

register_responses_examples = {
    200: {
        "description": "Успешная регистрация",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "Успешная регистрация",
                        "description": "Пример ответа при успешной регистрации",
                        "value": {'id': 1} | {key: value for key, value in
                                  user_in_examples['default']['value'].items() if key != 'password'}
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

get_token_examples = {
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