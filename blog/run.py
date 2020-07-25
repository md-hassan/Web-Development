#application launcher

from flaskblog import create_app  # imports from package, __init__.py file in particular

app = create_app()

if __name__ == '__main__':          # to app run directly run using python
	app.run(debug=True)