'''
Ref:

https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

http://www.mso.anu.edu.au/~ralph/OPTED/
'''

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_celery import make_celery
import tasks_request as tr
from datetime import datetime

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://35.165.238.44:6379',
    CELERY_BACKEND='redis://35.165.238.44:6379'
)

celery = make_celery(app)

reqs = [
    {
        'id': 1,
        'type': u'a001',
        'load': u'Aback (adv.) Behind; in the rear.', 
        'done': False,
        'result': None
    },
    {
        'id': 2,
        'type': u'a001',
        'load': u'Abbreviating (p. pr. & vb. n.) of Abbreviate', 
        'done': False,
        'result': None
    }
]

results = [
    {
        'id': 1,
        'req_id': 1,
        'mod': datetime.utcnow(), 
        'status': False,
        'result': None
    }
]

'''
GET METHODS
'''
@app.route('/todo/api/v1.0/reqs', methods=['GET'])
def get_reqs():
    return jsonify({'reqs': [make_public_req(req) for req in reqs]})

@app.route('/todo/api/v1.0/reqs/<int:req_id>', methods=['GET'])
def get_req(req_id):
    req = [req for req in reqs if req['id'] == req_id]
    if len(req) == 0:
        abort(404)
    return jsonify({'req': req[0]})


@app.route('/todo/api/v1.0/results/<int:req_id>', methods=['GET'])
def get_results(req_id):
    req = [req for req in results if req['id'] == req_id]
    if len(req) == 0:
        abort(404)
    return jsonify({'req': req[0]})

'''
POST METHODS
'''
@app.route('/todo/api/v1.0/reqs', methods=['POST'])
def create_req():
    if not request.json or not 'type' in request.json:
        abort(400)
    req = {
        'id': reqs[-1]['id'] + 1,
        'type': request.json['type'],
        'load': request.json.get('load', ""),
        'done': False,
        'result': None
    }
    reqs.append(req)
    return jsonify({'req': req}), 201

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'type' in request.json:
        abort(400)
    res = add_task(request.json['type'], request.json.get('load', ""))
    return jsonify({'status': res}), 201

'''
Put Methods
'''
@app.route('/todo/api/v1.0/reqs/<int:req_id>', methods=['PUT'])
def update_req(req_id):
    req = [req for req in reqs if req['id'] == req_id]
    if len(req) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'type' in request.json and type(request.json['type']) != unicode:
        abort(400)
    if 'load' in request.json and type(request.json['load']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    req[0]['type'] = request.json.get('type', req[0]['type'])
    req[0]['load'] = request.json.get('load', req[0]['load'])
    req[0]['done'] = request.json.get('done', req[0]['done'])
    return jsonify({'req': req[0]})

'''
Delete Methods
'''

@app.route('/todo/api/v1.0/reqs/<int:req_id>', methods=['DELETE'])
def delete_req(req_id):
    req = [req for req in reqs if req['id'] == req_id]
    if len(req) == 0:
        abort(404)
    reqs.remove(req[0])
    return jsonify({'result': True})


'''
Helper Functions
'''
def add_task(req_type, req_load):
    req = {
        'id': reqs[-1]['id'] + 1,
        'type': req_type,
        'load': req_load,
        'done': False,
        'result': None,
        'created': datetime.utcnow()
    }
    async_res = tr.a001_get_file.delay('https://cdnjs.cloudflare.com/ajax/libs/1140/2.0/1140.min.css')
    return 0



def make_public_req(req):
    new_req = {}
    for field in req:
        if field == 'id':
            new_req['uri'] = url_for('get_req', req_id=req['id'], _external=True)
        else:
            new_req[field] = req[field]
    return new_req



'''
Error Handling
'''
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)