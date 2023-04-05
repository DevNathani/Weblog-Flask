# The only purpose of this module is to run the Application

from flask_blog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)
