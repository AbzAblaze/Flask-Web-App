#Import from __init__.py method
from website import create_app

app = create_app()

#Run App
if __name__ == '__main__':
    app.run(debug=True)