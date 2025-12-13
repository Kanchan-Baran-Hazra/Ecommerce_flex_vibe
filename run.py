from app import create_app,db
import os


app=create_app()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if __name__=='__main__':
    app.run(debug=True)