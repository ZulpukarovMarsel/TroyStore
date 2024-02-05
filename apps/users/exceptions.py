from rest_framework.exceptions import APIException

class AlreadyInFavoritesError(APIException):
    status_code = 400
    default_detail = 'Продукт уже добавлено в избранное. Вы не можете добавить его снова.'
    default_code = 'already_in_favorites'


class ProductNotFoundError(APIException):
    status_code = 404
    default_detail = 'Продукт не найдено. Пожалуйста, убедитесь, что событие существует.'
    default_code = 'event_not_found'
