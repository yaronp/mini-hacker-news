import json

from flask import Flask, request

from dal import Dal


def create_app():
    return Flask("PostsApp")


def http_error(msg, code):
    return json.dumps({msg: True}), code, {'ContentType': 'application/json'}


def register_routes(app):
    @app.route('/post', methods=['POST'])
    def api_posts():
        post_id = request.args.get('id')
        content = request.get_json(silent=True)
        if request.data is None or type(content) is not dict:
            return http_error('empty or wrong type body', 400)
        post_text = content.get('post')
        if post_text is None:
            return http_error('post field not found', 400)

        dal = Dal()
        if post_id is None:
            if not dal.create(post_text):
                return http_error('error while inserting record to storage', 500)
        else:
            if not dal.update(post_id, post_text):
                return http_error('error while inserting record to storage', 500)

        return http_error('success', 200)

    @app.route('/upvote', methods=['POST'])
    def api_up_vote():
        id = request.args.get('id', '')
        dal = Dal()
        dal.up_vote(id)
        return http_error('success', 200)

    @app.route('/downvote', methods=['POST'])
    def api_down_vote():
        id = request.args.get('id', '')
        dal = Dal()
        dal.down_vote(id)
        return http_error('success', 200)

    @app.route('/posts', methods=['GET'])
    def api_top_list():
        dal = Dal()
        data_set = dal.top_list()
        return json.dumps(data_set), 200, {'ContentType': 'application/json'}

    @app.route('/h', methods=['GET'])
    def api_hello():
        return "Hello, World!"


if __name__ == '__main__':
    app = create_app()
    register_routes(app)
    app.run(debug=True,host='0.0.0.0')
