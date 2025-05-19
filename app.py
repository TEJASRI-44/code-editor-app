from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    user_input = data.get("input", "")

    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code:
            temp_code.write(code.encode())
            temp_code.flush()

            result = subprocess.run(
                ['python3', temp_code.name],
                input=user_input.encode(),
                capture_output=True,
                timeout=5
            )
            output = result.stdout.decode()
            error = result.stderr.decode()

        os.remove(temp_code.name)
        return jsonify({"output": output, "error": error})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "", "error": "Execution Timed Out"})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
