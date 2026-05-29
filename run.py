import os
from src import create_app

app = create_app()

if __name__ == '__main__':
    port = app.config.get('PORT', 19191)
    debug = app.config.get('DEBUG', True)
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    
    print(f"\n" + "="*55)
    print(f" [*] Flask Application is starting up...")
    print(f" [*] Running on: http://{host}:{port}")
    print(f" [*] Debug Mode: {debug}")
    print(f" [*] Code base divided: 'src/' (app logic) & 'test/' (unit tests)")
    print("="*55 + "\n")
    
    app.run(host=host, port=port, debug=debug)
