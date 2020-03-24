import uuid

from flask import Flask, request, send_from_directory, render_template, make_response

from core import core
from frontend.Controller import CartController


class FlaskApp:
    """
    The FlaskApp providing the frontend view
    """
    app = Flask(__name__, static_url_path='')
    app.config['SECRET_KEY'] = uuid.uuid4().hex
    core.page_controller = CartController()

    @staticmethod
    @app.route('/')
    def page():
        """Returns the page body
        Sets the session cookie if not existent. (uuid4.hex)
        :return: return the Frontend according to the page controller
        """
        response = make_response(core.page_controller.page())
        if not request.cookies.get('session'):
            response.set_cookie('session', uuid.uuid4().hex)
        return response

    @staticmethod
    @app.route('/event')
    def event():
        """Handes incomming events to the page controller
        :return: result of the event handling
        """
        return core.page_controller.event(**request.args)

    @staticmethod
    @app.route('/poll')
    def poll():
        """Handes incomming long poll requests to the page controller
        :return: reply to the long poll, containing data or information the poll timed out
        """
        return core.page_controller.poll(request.cookies.get('session'))

    @staticmethod
    @app.route('/impressum')
    def impressum():
        """ Returnes the impressum
        :return: the impressum page
        """
        return render_template('page.html', main='impressum.html')

    @staticmethod
    @app.route('/img/<path:path>')
    def images(path):
        """ Handles requests for image data.
        :param path: path to image
        :return: requested image
        """
        return send_from_directory('static/img', path)

    @staticmethod
    @app.route('/webfonts/<path:path>')
    def fonts(path):
        """ Handles requests for web font.
        :param path: path to web font
        :return: requested web font
        """
        return send_from_directory('static/webfonts', path)

    @staticmethod
    @app.route("/css/<path:path>")
    def css(path):
        """ Handles requests for css file.
        :param path: path to css file
        :return: requested css file
        """
        return send_from_directory("static/css", path)

    @staticmethod
    @app.route("/js/<path:path>")
    def javascript(path):
        """ Handles requests for javascript file.
        :param path: path to javascript file
        :return: requested javascript file
        """
        return send_from_directory("static/js", path)
