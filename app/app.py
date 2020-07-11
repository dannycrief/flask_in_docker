from flask import Flask, jsonify
import redis

r = redis.Redis(host='redis', port=6379)
app = Flask(__name__)


def get_fibonacci(number):
    if (number == 0) or (number == 1):
        return number
    return get_fibonacci(number - 1) + get_fibonacci(number - 2)


@app.route('/')
def hello():
    return 'Hello'


@app.route("/<number>", methods=['GET'])
def get_fibonacci_api(number):
    number = int(number)
    stored_value = r.get(number)
    if stored_value:
        # logger.info("For %s stored value is used" % number)
        return jsonify({number: stored_value.decode()}), 200
    new_value = get_fibonacci(number)
    # logger.info("For %s new value is calculated" % number)
    r.set(number, new_value)
    return jsonify({number: new_value}), 200
