import json

from flask import Flask, request

from dal import Dal


def create_app():
    return Flask("PostsApp")


def http_error(msg, code):
    return json.dumps({msg: True}), code, {'ContentType': 'application/json'}


def get_post(id):
    dal = Dal()

    r = dal.get(id)
    response = {"date": r['date'], "post": r['post']}
    return json.dumps(response), 200, {'ContentType': 'application/json'}


def create_post(post_text):
    dal = Dal()
    if not dal.create(post_text):
        return http_error('error while inserting record to storage', 500)
    else:
        return http_error('success', 200)


def register_routes(app):
    @app.route('/v0/post', methods=['POST', 'GET'])
    def api_posts():
        post_id = request.args.get('id')

        if request.method == 'GET':
            if post_id is None:
                return http_error('No post id in args', 400)
            return get_post(post_id)

        content = request.get_json(silent=True)
        if request.data is None or type(content) is not dict:
            return http_error('empty or wrong type body (json body type?)', 400)
        post_text = content.get('post')
        if post_text is None:
            return http_error('post field not found in body', 400)

        if post_id is None:
            return create_post(post_text)
        else:
            dal = Dal()
            if not dal.update(post_id, post_text):
                return http_error('error while inserting record to storage', 500)

        return http_error('success', 200)

    @app.route('/v0/upvote', methods=['POST'])
    def api_up_vote():
        id = request.args.get('id', '')
        dal = Dal()
        dal.up_vote(id)
        return http_error('success', 200)

    @app.route('/v0/downvote', methods=['POST'])
    def api_down_vote():
        id = request.args.get('id', '')
        dal = Dal()
        dal.down_vote(id)
        return http_error('success', 200)

    @app.route('/v0/topstories', methods=['GET'])
    def api_top_list():
        dal = Dal()
        data_set = dal.top_list()
        if len(data_set) is 0:
            return "No posts in database"
        return json.dumps(data_set), 200, {'ContentType': 'application/json'}

    @app.route('/v0/h', methods=['GET'])
    def api_hello():
        return "\n\n<H>Hello, World!<H>\n\n"


if __name__ == '__main__':
    the_app = create_app()
    register_routes(the_app)
    the_app.run(debug=True, host='0.0.0.0')
