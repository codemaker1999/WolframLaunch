import Tkinter as tk
import tkSimpleDialog as tksd
import tkMessageBox as mbox
import os

def query_parse(q):
    '''
    Attempt to parse query
    EX:
        "5+3" will appear in the query url as "5%2B3"
        "5 + 3^7" will appear in the query url as "5+%2B+3%5E7"
    You can test and add more by querying at wolframalpha.com
    This is mostly only needed for plus signs (which are seen as
    spaces in the URL by worfram)
    '''
    s = ''
    for char in q:
        if char == '+':
            char = '%2B'
        elif char == ' ':
            char = '+'
        elif char == '^':
            char = '%5E'
        ##elif char == '':
        ##    char = ''
        s+=char
    return s

def ask_matrix():
    '''build n by m matrix in wolfram input string'''
    n = tksd.askinteger('Matrix Builder','Enter number of rows')
    if n == None: return ''
    m = tksd.askinteger('Matrix Builder','Enter number of columns')
    if m == None: return ''
    s = "{" #Open matrix
    for i in range(n):
        #Make 1D array if n==1
        if not(n==1):
            s+="{" #Open row
        #Fill row
        for j in range(m):
            ans = tksd.askstring('Matrix Builder','Enter Row %d'%(i+1))
            if ans == None: return ''
            s+=ans
            #Only add comma if not at last element
            if m-1 != j:
                s+=','
        if not(n==1):
            s+="}" #Close row
        #Only add comma after row if not at last element
        if n-1 != i:
            s+=','
    s+="}" #Close matrix
    return s

if __name__ == '__main__':    
    # Set up Tkinter
    root = tk.Tk()
    root.title('Wolfram Launcher')
    w,h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('350x26+%d+%d'%(w/2 - 175,h/2))
    
    # Add Widgets
    entry = tk.Entry(root)
    entry.grid(row=1,column=2,sticky=tk.E+tk.W)
    entry.focus_set()
    #
    def add_matrix():
        'wrapper to put matrix in entry'
        matrix = ask_matrix()
        entry.insert('end',matrix)
    
    buttonleft = tk.Button(root, text='Add Matrix', command=add_matrix)
    buttonleft.grid(row=1,column=1,sticky=tk.W)
    #
    def go(callback=None):
        'Launch wolfram with default browser'
        raw_query = entry.get()
        query = query_parse( raw_query )
        os.system('start "" "http://www.wolframalpha.com/input/?i=%s"'%query)
        root.destroy()
        exit()
    
    buttonright = tk.Button(root, text='Go', command=go)
    buttonright.grid(row=1,column=3,sticky=tk.E)
    #
    # Finish up..
    root.bind('<Return>', go)
    root.columnconfigure(2,weight=1)
    #
    tk.mainloop()
