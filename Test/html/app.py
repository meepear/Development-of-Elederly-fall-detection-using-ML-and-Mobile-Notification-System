from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # ข้อมูลตัวอย่างที่ส่งกลับไปยัง JavaScript
    response = {
        'message': 'Hello from Python!',
        'number': 42
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
