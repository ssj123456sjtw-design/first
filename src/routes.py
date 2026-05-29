from flask import Blueprint, render_template, jsonify
import platform
import sys
import time

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Renders the developer dashboard home page."""
    system_info = {
        'os': platform.system(),
        'os_release': platform.release(),
        'python_version': sys.version.split()[0],
        'flask_port': 19191,
        'server_time': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return render_template('index.html', system_info=system_info)

@bp.route('/api/health')
def health():
    """API health status endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask server is running on port 19191',
        'python_version': sys.version.split()[0],
        'timestamp': time.time()
    })

@bp.route('/feature1')
def feature1():
    """Renders the Morning Stock Dashboard."""
    stocks = [
        {'symbol': '2330.TW', 'name': '台積電', 'price': 915.0, 'change': '+2.8%', 'trend': 'up'},
        {'symbol': '2317.TW', 'name': '鴻海', 'price': 186.5, 'change': '+1.6%', 'trend': 'up'},
        {'symbol': '2454.TW', 'name': '聯發科', 'price': 1220.0, 'change': '-0.8%', 'trend': 'down'},
        {'symbol': 'NVDA', 'name': '輝達', 'price': 1064.2, 'change': '+4.5%', 'trend': 'up'},
    ]
    return render_template('feature1.html', stocks=stocks)

@bp.route('/feature2')
def feature2():
    """Renders the Afternoon Corporate Portal Page."""
    company_info = {
        'name': 'CKC_101 智慧科技集團',
        'english_name': 'CKC_101 IntelTech Group',
        'motto': '智慧創新，引領未來 (Innovation Powers the Future)',
        'afternoon_announcement': '下午 3 點於第一會議室召開跨部門代碼重構與單元測試對齊會議，請相關同仁準時出席。',
        'address': '台北市信義區研發園區大樓 A 棟 12 樓',
        'shift_time': '下午半日班 13:30 - 18:00'
    }
    return render_template('feature2.html', company_info=company_info)


