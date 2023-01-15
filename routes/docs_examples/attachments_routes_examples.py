view_attachment_responses_examples = {
    200: {
        "description": "Успешное получение вложение",
        "content": {
            "application/octet-stream": {
                "examples": {
                    "default": {
                        "summary": "Успешное получение вложения",
                        "description": "Пример ответа при успешном получении поста",
                        "value": "<binary data>"
                    }
                }
            }
        }
    },
    404: {
        "description": "Вложение не найдено",
        "content": {
            "application/json": {
                "examples": {
                    "default": {
                        "summary": "Вложение не найдено",
                        "description": "Пример ответа когда вложение не найдено",
                        "value": {
                            "details": "Attachment not found"
                        }
                    }
                }
            }
        }
    }
}