import json

from flask import Flask, request

from dal import Dal


def create_app():
    return Flask("PostsApp")


def http_error(msg, code):
    return json.dumps({msg: True}), code, {'ContentType': 'application/json'}


def register_routes(app):
    @app.route('/posts', methods=['POST'])
    def api_posts():
        content = request.get_json(silent=True)
        if request.data is None or type(content) is not dict:
            return http_error('empty or wrong type body', 400)
        if content.get('post') is None:
            return http_error('post field not found', 400)

        dal = Dal()
        if not dal.create(content.get('post')):
            return http_error('error while inserting record to storage', 500)

        return http_error('success', 200)

    @app.route('/upvote', methods=['POST'])
    def api_up_vote():
        id = request.args.get('id', '')
        print id
        pass

    @app.route('/downvote', methods=['POST'])
    def api_down_vote():
        id = request.args.get('id', '')
        print id
        pass

    @app.route('/posts', methods=['GET'])
    def api_top_list():
        pass


if __name__ == '__main__':
    app = create_app()
    register_routes(app)
    app.run(debug=True)
