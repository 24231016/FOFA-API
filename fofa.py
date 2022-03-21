# -*- coding: utf-8 -*-
import pyfofa
import time
import csv
import pandas as pd
import os
import sys
start=time.time()
bar_len = 60
logo="""

 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██╗    ██╗ █████╗ ██████╗ ███████╗ █████╗ ██████╗ ███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██║    ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║ █╗ ██║███████║██████╔╝█████╗  ███████║██████╔╝█████╗  
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██║███╗██║██╔══██║██╔══██╗██╔══╝  ██╔══██║██╔══██╗██╔══╝  
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ╚███╔███╔╝██║  ██║██║  ██║██║     ██║  ██║██║  ██║███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                                                  Author:qekuxpre   Ver:2.0
"""
print(logo)
def search():
    email = '' #輸入email
    key = '' #輸入API KEY
    search = pyfofa.FofaAPI(email, key) #因fofa網域有變，需至pyfofa套件庫中的api.py，更改self.base_url至最新
    try:
        print('檢查Email&Key中')
        test = search.get_data("123456")['size']
    except:
        print('請檢查Email及Key是否輸入正確')
        exit(1)
    search_fofa = input("\n請輸入關鍵字 :")    
    keyword = str(search_fofa).split("\"")
    if len(keyword) > 1:
        f = open("./output/%s_%s.csv"%(keyword[1],time.strftime("%m月%d日%H%M", time.localtime())),'w',encoding='utf_8_sig',newline='')
        doc = open("./output/%s_%s.html"%(keyword[1],time.strftime("%m月%d日%H%M", time.localtime())), "a+" ,encoding="UTF-8")
    else:
        f = open("./output/%s_%s.csv"%(search_fofa,time.strftime("%m月%d日%H%M", time.localtime())),'w',encoding='utf_8_sig',newline='')
        doc = open("./output/%s_%s.html"%(keyword[1],time.strftime("%m月%d日%H%M", time.localtime())), "a+" ,encoding="UTF-8")
    try:
        doc.write(html1)
        size = search.get_data(search_fofa)['size']        
        pagenum = int(int(size)/100 + 1)
        print("共%s筆，共%s頁(因API限制最多10000筆&100頁)"%(size,pagenum))
        name = ['Url','Title','Country','City','IP','Port','Server','Protocol'] #csv表格列
        writer = csv.writer(f)
        writer.writerow(name)
        print("請稍候，爬取中")
        for page in range(1,pagenum+1):
            try:                
                re_date = search.get_data(search_fofa, page, "host,title,country_name,city,ip,port,server,protocol")['results']
                writer.writerows(re_date)
                filled_len = int(round(bar_len * (page) / float(pagenum)))
                percents = round(100.0 * (page) / float(pagenum), 1)
                bar = ['='] * filled_len + ['-'] * (bar_len - filled_len)
                
                sys.stdout.write('[%s] %s%s %s/%s頁\r' % (''.join(bar), percents, '%', page, pagenum))
                sys.stdout.flush()                
            except:                
                pass
            for host,title in search.get_data(search_fofa, page,"host,title")['results']:
                if host.find('https'):
                    host = "http://" + host               
                body = """<br>            
                <a href="%s" target="_blank">%s  </a>    
                """%(host,title)
                doc.write(body)
        print("\n!!完成!!")        
        end = time.time()
        sd = end-start
        lj = os.path.dirname(__file__)
        print('\n資料保存在:'+lj + '\\output目錄下面')
        print('\n耗費:%s秒'%round(sd))
        html2 = """
        </div>
        </body>
        </html>"""
        doc.write(html2)
        doc.close()
    except Exception as e:
        print(e)
        print("\n請檢查關鍵字或是頁數是否正確")
html1 = """
    <html>
    <head></head>
    <style>
    body {
        background-color: #2b2b2b;
        color: #ccc;
    }
    a {
        background-color: transparent;
        text-decoration: none;
        outline: 0;
    }
    a:link {
        color:#FF0000;
        text-decoration:underline;
    }
    a:visited {
        color:#00FF00;
        text-decoration:none;
    }
    a:hover {
        color:#000000;
        text-decoration:none;
    }
    a:active {
        color:#FFFFFF;
        text-decoration:none;
    }
    </style>
    <body>
    <div>"""
search()
