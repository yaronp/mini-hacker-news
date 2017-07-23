from flask import Flask, request

app = Flask(__name__)


@app.route('/posts/<id>', methods=['POST'])
def api_posts(id=None):
    print post_id
    if request.method == 'POST':
        pass
    else:
        pass


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
    app.run(debug=True)
