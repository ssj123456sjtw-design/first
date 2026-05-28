from flask import Blueprint, render_template, jsonify, request, redirect, url_for
import platform
import sys
import time
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

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


# ── Feature 3: AWS S3 Bucket 管理中心 ──────────────────────────────
# 驗證方式：EC2 IAM Instance Profile（程式碼中無任何金鑰）
S3_BUCKET = 'ckc101-10'


def _get_file_icon(key):
    """Return an emoji icon based on file extension."""
    ext = key.rsplit('.', 1)[-1].lower() if '.' in key else ''
    icons = {
        'pdf': '📄', 'doc': '📝', 'docx': '📝', 'txt': '📃',
        'xls': '📊', 'xlsx': '📊', 'csv': '📊',
        'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️', 'gif': '🖼️', 'svg': '🖼️',
        'mp4': '🎬', 'mov': '🎬', 'avi': '🎬',
        'mp3': '🎵', 'wav': '🎵',
        'zip': '🗜️', 'tar': '🗜️', 'gz': '🗜️',
        'py': '🐍', 'js': '📜', 'html': '🌐', 'css': '🎨', 'json': '⚙️',
        'sh': '⚡', 'yml': '⚙️', 'yaml': '⚙️',
    }
    return icons.get(ext, '📁')


def _format_size(size_bytes):
    """Format file size in human-readable units."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024**2:.1f} MB"
    else:
        return f"{size_bytes / 1024**3:.1f} GB"


@bp.route('/feature3')
def feature3():
    """Renders the AWS S3 Bucket management page.
    
    Authentication: EC2 IAM Instance Profile (no credentials in code).
    boto3 automatically resolves credentials via the instance metadata service.
    """
    s3 = boto3.client('s3')  # Uses EC2 IAM Instance Profile automatically
    objects = []
    error = None
    flash_message = request.args.get('msg')
    total_bytes = 0

    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=S3_BUCKET):
            for obj in page.get('Contents', []):
                obj['icon'] = _get_file_icon(obj['Key'])
                obj['size_display'] = _format_size(obj['Size'])
                total_bytes += obj['Size']
                objects.append(obj)
    except NoCredentialsError:
        error = '找不到 AWS 憑證。請確認 EC2 已綁定具有 S3 存取權限的 IAM Role。'
    except ClientError as e:
        error = f"S3 存取錯誤：{e.response['Error']['Code']} — {e.response['Error']['Message']}"

    return render_template(
        'feature3.html',
        objects=objects,
        bucket_name=S3_BUCKET,
        error=error,
        flash_message=flash_message,
        total_size=_format_size(total_bytes),
    )


@bp.route('/feature3/upload', methods=['POST'])
def feature3_upload():
    """Upload a file to the S3 bucket.
    
    Authentication: EC2 IAM Instance Profile (no credentials in code).
    """
    uploaded_file = request.files.get('file')
    if not uploaded_file or uploaded_file.filename == '':
        return redirect(url_for('main.feature3', msg='請選擇要上傳的檔案'))

    s3 = boto3.client('s3')  # Uses EC2 IAM Instance Profile automatically
    try:
        s3.upload_fileobj(
            uploaded_file,
            S3_BUCKET,
            uploaded_file.filename,
        )
        return redirect(url_for('main.feature3', msg=f'✅ 成功上傳：{uploaded_file.filename}'))
    except NoCredentialsError:
        return redirect(url_for('main.feature3', msg='錯誤：找不到 AWS 憑證，請確認 IAM Role 設定'))
    except ClientError as e:
        code = e.response['Error']['Code']
        return redirect(url_for('main.feature3', msg=f'上傳失敗：{code}'))


@bp.route('/feature3/download/<path:key>')
def feature3_download(key):
    """Generate a presigned URL for downloading a file from S3.
    
    Authentication: EC2 IAM Instance Profile (no credentials in code).
    Presigned URL expires in 5 minutes (300 seconds).
    """
    s3 = boto3.client('s3')  # Uses EC2 IAM Instance Profile automatically
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': key},
            ExpiresIn=300,
        )
        return redirect(url)
    except (NoCredentialsError, ClientError) as e:
        return redirect(url_for('main.feature3', msg=f'下載失敗：{str(e)}'))


@bp.route('/feature3/delete/<path:key>', methods=['POST'])
def feature3_delete(key):
    """Delete an object from the S3 bucket.
    
    Authentication: EC2 IAM Instance Profile (no credentials in code).
    """
    s3 = boto3.client('s3')  # Uses EC2 IAM Instance Profile automatically
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=key)
        return redirect(url_for('main.feature3', msg=f'🗑 已刪除：{key}'))
    except (NoCredentialsError, ClientError) as e:
        return redirect(url_for('main.feature3', msg=f'刪除失敗：{str(e)}'))
