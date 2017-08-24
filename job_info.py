'''
2016,03.16基本功能实现了。遗留问题有：
1. 目标：网络连接可直接点击
2. 目标：text带上下拉条. ---------------------ok
'''
#macro
GUI = True

import logging
logger = logging.getLogger("job_info_log")  
formatter = logging.Formatter('', '',)
file_handler = logging.FileHandler("job_info_log.txt",encoding='utf-8')  
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)  

import requests
def get_job_infos_from_forum(url,host,encoding):
    '''get index from any forum
    url: string('http://m.byr.cn/board/Python')
    host: string('m.byr.cn')
    encoding: string("m.byr.cn")'''
    import requests
    
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' }
    s = requests.session()
    s.headers.update(headers)
    
    r = s.get(url)
    r.encoding = encoding
    
    import re
    job_infos_patten = re.compile(r'(?P<job_url>/article/.*?(?=">))">(?P<job_header>.*?(?=</a>)).*?(?=<div>)<div>(.*?)(?=&nbs)')
                                                        #  .*?  .匹配任意字符，？非贪婪。 <job_infos>正则表达式的关键在于：卡住开头和结尾（固定字符），中间任意（.*?）
    job_infos = job_infos_patten.findall(r.text)
    for i in range(0,len(job_infos)):
        job_infos[i] = (job_infos[i][1],job_infos[i][2],"http://"+host+job_infos[i][0])
    return job_infos

def filter_job_infos_by_words(job_infos, words):
    '''job_infos: list, every element in list is tuple
    words: tuple of several word
    '''
    import re
    filtered_job_infos = []# a list of tuple, every tuple is ：（header,时间,url）
    for i in range(len(words)):
        word = words[i]
        if word[0] >= u'\u4e00' and word[0]<=u'\u9fa5':#是汉字
            word_search_pattern = re.compile(r'%s' %word)
        else:
            if(word[-1]=="+"):#解决c++问题
                word_search_pattern = re.compile(r'\+\+',re.IGNORECASE)
            else:
                word_search_pattern = re.compile(r'%s' %word,re.IGNORECASE)
        for job_info in job_infos:
            if word_search_pattern.findall(job_info[0]) != []:
                filtered_job_infos.append(job_info)
    return filtered_job_infos
            
def filter_job_infos_by_time(job_infos):
        pass
    

key_words = []
pages = "0"
filtered_job_infos=[]
if __name__ == "__main__" and GUI:
    #创建界面
    from tkinter import *
    top = Tk()
    top.geometry('1100x800+0+0')#width x height
    # Code to add widgets will go here...
    wdgt_label_0 = Label(top, text="Key words:")
    wdgt_label_0.pack( side = LEFT)
    wdgt_label_0.place(bordermode=OUTSIDE,x=0,y=30)
    wdgt_keywords=Entry(master=top,bd=2,cursor="arrow",width=300)
    wdgt_keywords.pack(side=RIGHT)
    wdgt_keywords.place(bordermode=OUTSIDE,x=80,y=30)

    wdgt_label_1 = Label(top, text="pages:")
    wdgt_label_1.pack( side = LEFT)
    wdgt_label_1.place(bordermode=OUTSIDE, x=0, y=60)
    wdgt_pages=Entry(master=top,bd=2,cursor="arrow")
    wdgt_pages.pack(side=RIGHT)
    wdgt_pages.place(bordermode=OUTSIDE, x=80, y=60)

    var=StringVar()
    wdgt_label_2 = Label(top,textvariable=var,relief=RAISED,bd=0)
    var.set(r'''Type or load "key words" and "pages", use"," between multiple words ''')
    wdgt_label_2.pack(side = RIGHT)
    wdgt_label_2.place(bordermode=OUTSIDE,x=0,y=0)

    wdgt_scrollbar = Scrollbar(top)#滚动条
    wdgt_scrollbar.pack( side = RIGHT, fill=Y )
    #wdgt_scrollbar.place(x=1000,y=200)
    var_1=StringVar()
    #wdgt_result = Message(top,bd=2,textvariable=var_1,relief=RAISED)
    wdgt_result = Text(top,width=150,height=40,yscrollcommand =wdgt_scrollbar.set)
    #var_1.set('push "get"')
    wdgt_result.pack(side=RIGHT)
    wdgt_result.place(bordermode=OUTSIDE,x=0,y=200)
    wdgt_scrollbar.config( command = wdgt_result.yview )



    def show_config():#在wdgt_label_2上显示当前配置
        #global wdgt_keywords,wdgt_pages,wdgt_label_2,var
        global key_words,pages,var
        var.set("key words: %s;  " %key_words + "pages: %s" %pages)
    def show_result():
        global var_1,wdgt_result
        wdgt_result.insert(END,"复制网址，可用Ctrl+C:\nDesigned by yu.ty  https://www.zhihu.com/people/ty-yu-58\n")
        wdgt_result.tag_add("start", "1.0", "1.32")
        wdgt_result.tag_config("start", background="green", foreground="blue")
        wdgt_result.tag_add("end", "2.0", "2.64")
        wdgt_result.tag_config("end", background="green", foreground="blue")
        for tmp in filtered_job_infos:
            #result_tmp+=tmp[0]+tmp[1]+"  "+tmp[2]+"\n"
            wdgt_result.insert(END,tmp[0]+tmp[1]+"  "+tmp[2]+"\n")
        #var_1.set(result_tmp)
        #wdgt_result.insert(END,result_tmp)


    def get_words_from_string(str_input):
        temp = str_input
        words=[]
        while(temp!="" and temp!=" "):
            for i in range(len(temp)):
                #if(temp[i]==',' or temp[i]=="，"):
                if(temp[i]==' '):
                    words.append(temp[:i])
                    temp = temp[i+1:]
                    while(temp[0]==" " and len(temp)>1):
                        temp=temp[1:]
                    break
            if(i==len(temp)-1 and temp!=""):
                #if(temp[-1]!="," or temp[-1]!="，"):
                if(temp[-1]!=" "):
                    words.append(temp)
                else:
                    words.append(temp[:-1])
                temp=''
        return words
    def get_job():
        global key_words,pages
        global wdgt_keywords,wdgt_pages,filtered_job_infos
        temp = wdgt_keywords.get()
#如果输入框里有，用输入框里的。如果没有，不做改变
        if(temp!=""):
            key_words = get_words_from_string(temp)
        if(wdgt_pages.get()!=""):
            pages = wdgt_pages.get()
        show_config()
        #生成url
        num =int(pages)
        if(num==""):
            pages="0"
            return
        url = []
        #获取北邮人信息
        for i in range(1,num+1):
            url.append("http://m.byr.cn/board/JobInfo?p="+"%s" %i)
        host = 'm.byr.cn'
        filtered_job_infos = []
        encoding = "utf-8"
        for tmp_url in url:
            job_infos = get_job_infos_from_forum(tmp_url,host,encoding)#爬帖子
            filtered_job_infos+=filter_job_infos_by_words(job_infos, key_words)#筛选帖子
        #获取水木信息
        url = []
        for i in range(1,num+1):
            url.append("http://m.newsmth.net/board/Career_Upgrade?p="+"%s" %i)
            url.append("http://m.newsmth.net/board/ExecutiveSearch?p="+"%s" %i)
        host = 'm.newsmth.net'
        for tmp_url in url:
            job_infos = get_job_infos_from_forum(tmp_url,host,encoding)
            filtered_job_infos+=filter_job_infos_by_words(job_infos, key_words)#筛选帖子
        for tmp in filtered_job_infos:
            logger.debug(tmp)
        show_result()


    wdgt_button_start =Button(top, text ="Get", command = get_job)
    wdgt_button_start.pack(side=BOTTOM)
    wdgt_button_start.place(bordermode=OUTSIDE, x=0, y=90)

    def save_config():
        global key_words,pages
        import pickle
        with open('job_info.pkl','wb') as f:
            #如果输入框里有，用输入框里的。如果没有，不做改变
            temp = wdgt_keywords.get()
            if(temp!=""):
                key_words = get_words_from_string(temp)
            if(wdgt_pages.get()!="" or wdgt_pages.get()!="0"):
                pages = wdgt_pages.get()
            pickle.dump(key_words,f)
            pickle.dump(pages,f)
        show_config()
    def load_config():
        with open('job_info.pkl',"rb") as f:
            global key_words,pages
            import pickle
            key_words = pickle.load(f)#list. 每一项是字符串
            pages=pickle.load(f)
        show_config()

    wdgt_button_save =Button(top, text ="Save config", command = save_config)
    wdgt_button_save.pack(side=BOTTOM)
    wdgt_button_save.place(bordermode=OUTSIDE, x=0, y=120)
    wdgt_button_load =Button(top, text ="Load config", command = load_config)
    wdgt_button_load.pack(side=BOTTOM)
    wdgt_button_load.place(bordermode=OUTSIDE, x=0, y=150)
    top.mainloop()
#智能,硬件,hardware,FPGA,电子,opencl,Integration,图像,专利,intellectual,patent
#智能 硬件 hardware FPGA 电子 opencl Integration 图像 专利 intellectual patent