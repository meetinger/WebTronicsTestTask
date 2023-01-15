user_in_examples = {
    "default": {
        "summary": "Данные пользователя",
        "description": "Пример пользовательских данных",
        "value": {
            "username": "example_username",
            "name": "Example Name",
            "email": "examplemail@example.com",
            "password": "a_very_strong_password"
        }
    }
}
user_full_examples = {
    "default": {
        "summary": "Данные пользователя",
        "description": "Пример полных пользовательских данных",
        "value": {'id': 1} | {key: value for key, value in
                              user_in_examples['default']['value'].items() if key != 'password'}
    }
}

user_limited_examples = {
    "default": {
        "summary": "Данные пользователя",
        "description": "Пример ограниченных пользовательских данных",
        "value": {key: value for key, value in
                  user_full_examples['default']['value'].items() if key != 'email'}
    }
}
