from flask import jsonify


def server_error(error):
    return jsonify({"error": str(error)}), 500

def status_msg(message: str, status_code: int = 401):
    return jsonify({"message":message}), status_code