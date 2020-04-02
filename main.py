from frontend.FlaskApp import FlaskApp

if __name__ == '__main__':
    FlaskApp().app.run(ssl_context=('cert.pem', 'key.pem'), host="192.168.137.86")
