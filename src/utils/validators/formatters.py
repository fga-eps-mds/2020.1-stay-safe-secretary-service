from flask import jsonify

def create_response(content, status=500):
    """
       The jsonify() function in flask returns a flask.Response()
       object that already has the appropriate content-type header
       'application/json' for use with json responses.
    """

    if isinstance(content, (dict, list)):
        return jsonify(content), status
    if isinstance(content, str):
        if status >= 400:
            content = {'error': content}
        else:
            content = {'msg': content}
    else:
        content = {'error': 'Internal server error!'}

    return jsonify(content), status


def get_row_dict(row):
    """
        Converts the model object into a dictionary
    """

    d = {}
    for column in row.__table__.columns:
        attr = getattr(row, column.name)
        d[column.name] = attr

    return d
