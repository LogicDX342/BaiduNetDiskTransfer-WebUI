from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()
if os.getenv('APP_ENV') == 'development':
    load_dotenv('.env.development', override=True)

def init():
    cookies = os.getenv('COOKIES', '')
    bduss = ''
    stoken = ''
    for cookie in cookies.split(';'):
        if 'BDUSS' in cookie:
            bduss = cookie.split('=')[1]
        if 'STOKEN' in cookie:
            stoken = cookie.split('=')[1]
    if not bduss or not stoken:
        raise Exception('BDUSS or STOKEN not found in cookies')
    download_dir = os.getenv('TRANSFER_DIR', '/PCS-Transfer')

    commands = [
        ['./BaiduPCS-Go', 'login', '--bduss', bduss, '--stoken', stoken],
        ['./BaiduPCS-Go', 'mkdir', download_dir],
        ['./BaiduPCS-Go', 'cd', download_dir]
    ]

    for command in commands:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            print(line)
        for line in process.stderr:
            print(line)

app = Flask(__name__)
with app.app_context():
    config_dir = os.getenv('BAIDUPCS_GO_CONFIG_DIR', os.path.join(os.getenv('HOME', '/root'), '.config/BaiduPCS-Go'))
    if not os.path.exists(config_dir) or not os.listdir(config_dir):
        init()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/transfer', methods=['GET'])
def transfer():
    share_link = request.args.get('share_link')
    token = request.args.get('token')
    if token != os.getenv('TOKEN'):
        return Response("Unauthorized", status=401)

    def generate():
        # TODO: '--collect' option might result in some issues. Waiting for PCS-Go to fix it.
        process = subprocess.Popen(['./BaiduPCS-Go', 'transfer', share_link], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            yield f"data:{line}\n\n"
        for line in process.stderr:
            yield f"data:{line}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)