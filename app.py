from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()
if os.getenv('APP_ENV', 'development') == 'development':
    load_dotenv('.env.development', override=True)

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        yield f"data:{line}\n\n"
    for line in process.stderr:
        yield f"data:{line}\n\n"

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
        ['./BaiduPCS-Go', 'mkdir', download_dir]
    ]

    for command in commands:
        for output in run_command(command):
            print(output)

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
    
    if request.headers.get('Accept') == 'text/event-stream':
        def generate():
            download_dir = os.getenv('TRANSFER_DIR', '/PCS-Transfer')
            for output in run_command(['./BaiduPCS-Go', 'cd', download_dir]):
                print(output)
            yield from run_command(['./BaiduPCS-Go', 'transfer', share_link])

        return Response(generate(), mimetype='text/event-stream')
    else:
        return Response("Token validated", status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)