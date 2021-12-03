from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = template(['해당 유저를 찾을 수 없습니다.'], code=404)
USER_ALREADY_REGISTERED = template(['이미 등록된 유저입니다.'], code=422)
UNKNOWN_ERROR = template([], code=500)
POST_NOT_FOUND = template(['해당 ID로 찾을수 없습니다.'], code=404)
NO_AUTHORITY = template(['권한이 없습니다.'], code=422)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def post_not_found(cls):
        return cls(**POST_NOT_FOUND)

    @classmethod
    def no_authority(cls):
        return cls(**NO_AUTHORITY)