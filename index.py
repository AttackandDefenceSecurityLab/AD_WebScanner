from flask import Flask,render_template,url_for,request
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
import os,json,subprocess
#from flask_cache import Cache
#from AD_Scanner_Base import *

app=Flask(__name__)
bootstrap=Bootstrap(app)
# cache = Cache(app, config={'CACHE_TYPE': 'redis',
#                            'CACHE_REDIS_HOST': '127.0.0.1',
#                            'CACHE_REDIS_PORT': 6379,
#                            'CACHE_REDIS_PASSWORD': '',
#                            'CACHE_REDIS_DB': 0}     )


@app.route('/')
@app.route('/',methods=['POST'])
#@cache.cached(timeout=5*60 )


def index():
    if request.method=='POST':
        url=request.form['URL']
        cmd="python AD_Scanner_Base.py -u "+url
        result= subprocess.Popen (cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        results=result.stdout.read()
        #err=result.stderr
        res=str(results,encoding="utf-8")
        json.dumps(res)
        return render_template('content.html',result=res)
    else:
        return render_template('AD.html')



if __name__ == "__main__":
    app.run(debug=True)

