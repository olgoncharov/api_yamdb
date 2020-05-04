# api_yamdb
## Проект по реализации API

Создано с помощью Django REST Framework

### Описание:
реализация REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.

### Установка:
Для установки ПО необходимо установить зависимости

*pip install -r requirement.txt*

### Доступные методы:
метод                                                         | GET | POST | PUT | PATCH | DEL |
--------------------------------------------------------------|-----|------|-----|-------|-----|
/api/v1/auth/email/ | - | V | - | - | - |
/api/v1/auth/token/| - | V | - | - | - |
/api/v1/token/refresh/ | - | V | - | - | - |
/api/v1/users/me/| V | - | - | V | - |
/api/v1/titles/ | V | V | - | - | - |
/api/v1/titles/{titles_id}/ | V | - | - | V | V |
/api/v1/titles/{title_id}/reviews/  | V | V | - | - | - |
/api/v1/titles/{title_id}/reviews/{review_id}/ | V | - | - | V | V |
/api/v1/titles/{title_id}/reviews/{review_id}/comments/ | V | V | - | - | - |
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ | V | - | - | V | V |
/api/v1/users/ | V | V | - | - | - |
/api/v1/users/{username}/ | V | - | - | V | V |
/api/v1/categories/ | V | V | - | - | - |
/api/v1/categories/{slug}/ | - | - | - | - | V |
/api/v1/genres/ | V | V | - | - | - |
/api/v1/genres/{slug}/ | - | - | - | - | V |
