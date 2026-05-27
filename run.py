from src import create_app
from src.config import Config

app = create_app()

if __name__ == '__main__':
    port = app.config.get('PORT', 19191)
    debug = app.config.get('DEBUG', True)
    
    print(f"\n" + "="*55)
    print(f" [*] Flask Application is starting up...")
    print(f" [*] Running on: http://127.0.0.1:{port}")
    print(f" [*] Debug Mode: {debug}")
    print(f" [*] Code base divided: 'src/' (app logic) & 'test/' (unit tests)")
    print("="*55 + "\n")
    
    app.run(host='127.0.0.1', port=port, debug=debug)
