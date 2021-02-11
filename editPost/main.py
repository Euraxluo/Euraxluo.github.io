from flask import Flask,render_template,request

import datetime
import os
import multiprocessing

app = Flask(__name__)

def execCmd(cmd):
    try:
        print("*"*20)
        print(cmd,"starting...")
        print("*"*20)
        os.system(cmd)
    except Exception as e:
        print ('%s\t 运行失败,失败原因\r\n%s' % (cmd,e))

@app.route('/')
def render_index():
    return render_template('template.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/post',methods=['POST'])
def post_edit_result():
    if request.method=='POST':
        try:
            name=request.form['name']
            if name[-1]=='/':
                name=name[:-1]
            value=request.form['value']
            data=''
            with open('./content/zh-cn'+name+'.md',mode='w',encoding='utf8') as f:
                f.write(value)
            with open('./content/zh-cn'+name+'.md',mode='r',encoding='utf8') as f:
                date = f.read()
            return {'code':200,'content':date}
        except Exception as e:
            print(e)
    return {'code':403,'content':'request valid not pass'}

@app.route('/get')
def get_url():
    url = request.args.get("url")
    content=''
    try:
        if url[-1]=='/':
            url=url[:-1]
        with open('./content/zh-cn'+url+'.md',encoding='utf8') as f:
            content=f.read()
    except Exception as e:
        print(e)
    data={
        'url':url,
        'content':content
    }
    return data
    
def start_server():
    cmds = ['hugo server -p 5001']
    threads = []
    for cmd in cmds:
        print(".................")
        th = multiprocessing.Process(target=execCmd, args=(cmd,))
        th.start()
        threads.append(th)

    app.run(debug=True)
    for th in threads:
        th.join()
    print ("程序结束运行%s" % datetime.datetime.now())

if __name__ == '__main__':
    start_server()

