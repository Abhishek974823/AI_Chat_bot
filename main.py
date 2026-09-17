from web1 import create_app1,db
app = create_app1()
app.jinja_env.filters['zip'] = zip
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)