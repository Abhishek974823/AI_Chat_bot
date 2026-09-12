from web1 import create_app1
app = create_app1()
app.jinja_env.filters['zip'] = zip
if __name__ == '__main__':
    app.run(debug=True)