from sheetclass import sheet, osu
from os import path
from tkinter import *
from tkinter import ttk

if path.isfile('./login.mph') == False:
    with open('login.mph', 'w+') as f:
        spreadsheetlink = input("Enter Spreadsheet link : ")
        f.write(spreadsheetlink + "\n")
        mappoolername = input("Enter Mappooler Name : ")
        f.write(mappoolername + "\n")
        mappooleramount = input("Enter Mappooler Amount : ")
        f.write(mappooleramount + "\n")
        index = input("Enter sheet index : ")
        f.write(index + "\n")
        print("Okay, you're logged in, welcome to Mappoolers' Helper Project !")

with open('login.mph', 'r') as r:
    logindata = r.readlines()
    mappoolsheet = sheet(logindata[0], int(logindata[3]), logindata[1].replace("\n", ""), int(logindata[2]))

class root(Tk):
    def __init__(self):
        super(root, self).__init__()
        self.title("Mappoolers' Helper Project")
        self.minsize(640, 400)
        self.option = ttk.Labelframe(self, text="Option")
        self.option.grid(row=1, column=10)
        self.specialoption = ttk.Labelframe(self, text="Special Option")
        self.specialoption.grid(row=5, column=10)
        self.mainframe = ttk.Labelframe(self, text="")
        self.mainframe.grid(row=1, column=0)
        self.button1()
        self.specialButton1()
        self.specialButton2()
        self.maps = []
        self.labelstatus = ttk.Labelframe(self, text="Status")
        self.labelstatus.grid(row=10, column=0)
        self.status = ttk.Label(self.labelstatus, text="You're currently working on {} round in {}".format(mappoolsheet.worksheet.title, mappoolsheet.worksheet.spreadsheet.title))
        self.status.grid(row=1, column=0)
        self.button2()
        self.button3()
        self.statusbutton()

    def button1(self):
        def addmapbutton():
            for widget in self.mainframe.winfo_children():
                widget.destroy()
            self.labelFrame = ttk.LabelFrame(self.mainframe, text="Add map")
            self.labelFrame.grid(row=1, column=0)
            self.allmapframe = ttk.Labelframe(self.mainframe, text="Maps")
            self.allmapframe.grid(row=6, column=0)
            self.allmaplabel = ttk.Label(self.allmapframe, text="")
            self.allmaplabel.grid(row=2, column=0)

            def labeladdmap():
                self.labelmap = ttk.Label(self.labelFrame, text="Map ID")
                self.labelmap.grid(column=1, row=1)
                self.labelt = ttk.Label(self.labelFrame, text="Type")
                self.labelt.grid(column=1, row=2)
                self.labelcomment = ttk.Label(self.labelFrame, text="Comment")
                self.labelcomment.grid(column=1, row=3)

            def buttonaddmap():
                self.bt = ttk.Button(self.labelFrame, text="Add map", command=addmap)
                self.bt.grid(column = 2, row = 4)
            
            def iptaddmap():
                self.iput = ttk.Entry(self.labelFrame, width=15)
                self.iput.grid(column=2, row=1)
                self.t = ttk.Entry(self.labelFrame, width=15)
                self.t.grid(column=2, row=2)
                self.comment = ttk.Entry(self.labelFrame, width=100)
                self.comment.grid(column=2, row=3)
            
            def addmap():
                aboutmap = {}
                aboutmap['map'] = self.iput.get()
                aboutmap['type'] = self.t.get()
                aboutmap['comment'] = self.comment.get()
                self.maps.append(aboutmap)
                bm = osu.beatmaps(aboutmap['map'])
                self.allmaplabel['text'] += "{} | ({}) {} - {} [{}] Comment : {}\n".format(aboutmap['type'], aboutmap['map'], bm['artist'], bm['title'], bm['version'], aboutmap['comment'])
                self.iput.delete(0, 'end')
                self.t.delete(0, 'end')
                self.comment.delete(0, 'end')
                          
            def addallmaps():
                for map_ in self.maps:
                    mappoolsheet.add_map(map_['map'], map_['type'], map_['comment'])
                self.maps = []
                self.allmaplabel['text'] = ""
            
            def addallbutton():
                self.bt_ = ttk.Button(self.allmapframe, text="Add all maps", command=addallmaps)
                self.bt_.grid(row=3, column=0)

            labeladdmap()
            iptaddmap()
            buttonaddmap()
            addallbutton()

        self.bt1 = ttk.Button(self.option, text="Add map to sheet", command=addmapbutton)
        self.bt1.grid(row=1, column=0)

    def statusbutton(self):

        def changestatuslabel():
            for widget in self.mainframe.winfo_children():
                widget.destroy()
            self.sheetlabel = ttk.Labelframe(self.mainframe, text="Sheet Link : ")
            self.sheetlabel.grid(row=1, column=0)
            self.sheetinput = ttk.Entry(self.sheetlabel, width=69)
            self.sheetinput.grid(row=0, column=1)
            self.mappoolername = ttk.Labelframe(self.mainframe, text="Mappooler Name : ")
            self.mappoolername.grid(row=3, column=0)
            self.mappoolerinput = ttk.Entry(self.mappoolername, width=69)
            self.mappoolerinput.grid(row=0, column=1)
            self.mappooleramt = ttk.Labelframe(self.mainframe, text="Mappooler Amount : ")
            self.mappooleramt.grid(row=5, column=0)
            self.amtinput = ttk.Entry(self.mappooleramt, width=69)
            self.amtinput.grid(row=0, column=1)
            self.ind = ttk.Labelframe(self.mainframe, text="Index : ")
            self.ind.grid(row=7, column=0)
            self.inde_ = ttk.Entry(self.ind, width=10)
            self.inde_.grid(row=0, column=1)
            def changestatus():
                with open("login.mph", "w+") as login:
                    login.write("{}\n{}\n{}\n{}".format(self.sheetinput.get(), self.mappoolerinput.get(), self.amtinput.get(), self.inde_.get()))
                    self.sheetlabel.destroy()
                    self.mappoolername.destroy()
                    self.mappooleramt.destroy()
                    self.ind.destroy()
                    self.changestatusbutton.destroy()
                    ttk.Label(self.mainframe, text="Update Success, please restart the client to work on brand new sheet").grid(row=8, column=0)
                    
            
            self.changestatusbutton = ttk.Button(self.mainframe, text="Change Status", command=changestatus)
            self.changestatusbutton.grid(row=9, column=1)

        self.stbt = ttk.Button(self.labelstatus, text="Click to change the worksheet", command=changestatuslabel)
        self.stbt.grid(row=2, column=0)

    def specialButton1(self):
        def pAllAgreement():
            mappoolsheet.pickAgreement()
        
        self.spbt1 = ttk.Button(self.specialoption, text="Pick all Agreements", command=pAllAgreement)
        self.spbt1.grid(row=1, column=0)
    
    def specialButton2(self):
        def showallbeatmapdata():
            for widget in self.mainframe.winfo_children():
                widget.destroy()
            self.lbf = ttk.Labelframe(self.mainframe, text="Beatmaps")
            self.lbf.grid(row=1, column=0)
            bmdata = mappoolsheet.showAllMaps()
            self.lb = ttk.Label(self.lbf, text=bmdata)
            self.lb.grid(row=1, column=0)
        
        self.spbt2 = ttk.Button(self.specialoption, text="Show all beatmaps data", command=showallbeatmapdata)
        self.spbt2.grid(row=2, column=0)
    
    def button2(self):
        def votelabel():
            for widget in self.mainframe.winfo_children():
                widget.destroy()
            self.voteframe = ttk.Labelframe(self.mainframe, text="Vote map")
            self.voteframe.grid(row=1, column=0)
            allmaparr = mappoolsheet.showAllMaps().split("\n")
            self.mapCombobox = ttk.Combobox(self.voteframe, values = allmaparr, width=69)
            self.mapCombobox.grid(row=1, column=0)
            self.votebutton = ttk.Button(self.voteframe, text="Vote this map", command=vote)
            self.votebutton.grid(row=2, column=0)
            self.mapvotedframe = ttk.Labelframe(self.mainframe, text="Voted Maps")
            self.mapvotedframe.grid(row=6, column=0)
            self.mapvoted = ttk.Label(self.mapvotedframe, text="")
            self.mapvoted.grid(row=1, column=0)
            self.voteallbutton = ttk.Button(self.mapvotedframe, text="Vote all maps", command=voteall)
            self.voteallbutton.grid(row=2, column=0)

        def vote():
            self.maps.append(self.mapCombobox.get().split("/")[-1])
            self.mapvoted['text'] += "{}\n".format(self.mapCombobox.get())
            self.mapCombobox.delete(0, 'end')

        def voteall():
            for i in self.maps:
                mappoolsheet.vote(i, True)
            self.mapvoted['text'] = ""
            self.maps = []

        self.bt2 = ttk.Button(self.option, text="Vote", command=votelabel)
        self.bt2.grid(row=2, column=0)
    
    def button3(self):

        def picklabel():
            for widget in self.mainframe.winfo_children():
                widget.destroy()
            self.pickframe = ttk.Labelframe(self.mainframe, text="Pick map")
            self.pickframe.grid(row=1, column=0)
            allmaparr = mappoolsheet.showAllMaps().split("\n")
            self.mappickCombobox = ttk.Combobox(self.pickframe, values = allmaparr, width=69)
            self.mappickCombobox.grid(row=1, column=0)
            self.pickbutton = ttk.Button(self.pickframe, text="Pick this map", command=pick)
            self.pickbutton.grid(row=2, column=0)
            self.mappickedframe = ttk.Labelframe(self.mainframe, text="Picked Maps")
            self.mappickedframe.grid(row=6, column=0)
            self.mappicked = ttk.Label(self.mappickedframe, text="")
            self.mappicked.grid(row=1, column=0)
            self.pickallbutton = ttk.Button(self.mappickedframe, text="Pick all maps", command=pickall)
            self.pickallbutton.grid(row=2, column=0)

        def pick():
            self.maps.append(self.mappickCombobox.get().split("/")[-1])
            self.mappicked['text'] += "{}\n".format(self.mappickCombobox.get())
            self.mappickCombobox.delete(0, 'end')

        def pickall():
            for i in self.maps:
                mappoolsheet.pick(i)
            self.mappicked['text'] = ""
            self.maps = []

        self.bt3 = ttk.Button(self.option, text="Pick", command=picklabel)
        self.bt3.grid(row=3, column=0)