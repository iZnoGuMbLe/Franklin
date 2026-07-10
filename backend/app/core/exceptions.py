
class AppException(Exception):
    ...


class NotFoundException(AppException):

    def __init__(self, entity: str, entity_id):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f'{entity} with {entity_id} is not found')