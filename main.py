from tkinter import *
import tkinter.ttk as ttk
import matplotlib
matplotlib.use("TkAgg")
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from preprocessingData import read_data, read_datapd, sum_weekly_sale_by_week, get_data, sum_weekly_sale_by_month
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from model import Model
from voiceRecognition import recognize_speech_from_mic, convertStringToInt
from tkinter import messagebox
import speech_recognition as sr

class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        self.model = Model()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        print(column)

    def init_window(self):
        self.master.title('Sale Forecast')
        self.create_menubar()

        #Add label chart
        self.label_chart = Label(master=self.master, font=("Helvetica", 16), text = "")
        self.label_chart.pack()
        self.label_chart.place(x = 40, y = 10)

        #Add button
        # self.button = Button(master=self.master, text='Voice Recognition',font = 'Times 14 ', command = lambda: self.regWin(Recognition).pack())
        # self.button.pack()
        # self.button.place(y = 875, x = 500)

        self.matplotCanvas()
        self.create_table()

    def matplotCanvas(self):
        self.f = Figure(figsize=(10, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.set_title('')

        self.canvas = FigureCanvasTkAgg(self.f, self.label_chart)
        self.canvas.get_tk_widget().grid(row = 0, column = 0)
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        # self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        # self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def create_menubar(self):
        # create menubar
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import")
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command= self.master.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.fucntion = Menu(self.menubar, tearoff=0)
        self.fucntion.add_command(label="Report", command=lambda: self.report_window(Report).pack())
        self.fucntion.add_command(label="Forecast", command = lambda: self.forecast_window(Forecast).pack())
        self.menubar.add_cascade(label="View", menu=self.fucntion)

        self.voicemenubar = Menu(self.menubar, tearoff=0)
        self.voicemenubar.add_command(command = lambda: self.regWin(Recognition).pack(), label = 'Voice Recognition')
        self.menubar.add_cascade(label = 'Voice', menu = self.voicemenubar, command = lambda: self.regWin(Recognition).pack())

        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_command(label='Voice Recognition', command = self.voiceHelp)
        self.help.add_command(label='About us')
        self.menubar.add_cascade(label='Help', menu=self.help)

        self.master.config(menu=self.menubar)

    def create_table(self):
        self.TableMargin = Frame(self.master, width=1000, height = 328)
        self.TableMargin.pack(side=TOP, fill= None)
        self.TableMargin.place(x = 40, y = 524)
        self.TableMargin.pack_propagate(0)

        self.scrollbarx = Scrollbar(self.TableMargin, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.TableMargin, orient=VERTICAL)
        self.tree = ttk.Treeview(self.TableMargin, columns= column, selectmode="extended", yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=BOTTOM, fill=X)

        for i in range(16):
            self.tree.heading(column[i], text=column[i], anchor=CENTER)
            if i == 0:
                self.tree.column('#' + str(i), stretch=NO, minwidth=100, width=0, anchor=CENTER)
            else:
                self.tree.column('#' + str(i), stretch=NO, minwidth=100, width=100, anchor=CENTER)
        self.tree.column('#16', stretch=NO, minwidth=100, width=100)
        self.tree.tag_configure('odd', background='#E8E8E8')
        self.tree.tag_configure('even', background='#f7f7f9')
        self.tree.tag_configure('column', background='#b8dcff')
        self.change_data_tree()
        self.tree.pack(fill = X, expand = NO)

    def report_window(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = Toplevel(self.master)
            _class(self.new)

        self.new.geometry("512x256")
        self.new.resizable(0,0)

        self.combobox = ttk.Combobox(self.new, values = ['All'] + list(set(pd_data.Store)),font = 'Times 14 ')
        self.combobox.pack()
        self.combobox.current(0) #combobox.get()
        self.combobox.place(x = 300, y = 20)
        self.label_store = Label(master=self.new, text="Choose the id store:", font = 'Times 14 ')
        self.label_store.pack()
        self.label_store.place(x=20, y=20)
        self.comboboxtime = ttk.Combobox(self.new, values=['Week'], font = 'Times 14 ')
        self.comboboxtime.pack()
        self.comboboxtime.current(0)  # combobox.get()
        self.comboboxtime.place(x=300, y=60)
        self.label_time = Label(master=self.new, text="Choose the period:", font = 'Times 14 ')
        self.label_time.pack()
        self.label_time.place(x=20, y=60)

        self.button_show = Button(master=self.new, command=self.plot, text='Report', font = 'Times 14 ')
        self.button_show.pack()
        self.button_show.place(y=150, x=250)

    def plot(self, voice = False, idx = None):
        if voice == False:
            if str(self.combobox.get()) == 'All':
                df = sum_weekly_sale_by_week(pd_data)
                self.a.set_title('The total weekly sales volume of the retail chain')
                self.change_data_tree()
            else:
                df = sum_weekly_sale_by_week(pd_data, int(self.combobox.get()))
                self.a.set_title("The weekly sales volume of the store's id: " + self.combobox.get())
                self.change_data_tree(idx = self.combobox.get())
        else:
            if idx == None:
                df = sum_weekly_sale_by_week(pd_data)
                self.a.set_title('The total weekly sales volume of the retail chain')
                self.change_data_tree()
            else:
                df = sum_weekly_sale_by_week(pd_data, int(self.number[0]))
                self.a.set_title("The weekly sales volume of the store's id: " + str(self.number[0]))
                self.change_data_tree(idx = str(self.number[0]))
        theta = df.Date
        r = df.Weekly_Sales
        self.a.plot(theta, r)
        self.canvas.draw()
        self.a.clear()

    def plotForecast(self, voice = False, idx = None):
        if voice:
            if idx == None:
                forecastData = self.model.get_predict()
                actualData = self.model.get_actual()
                self.a.set_title('The total weekly forecast sales volume of the retail chain')
                self.change_data_tree()
            else:
                forecastData = self.model.get_predict(idx)
                actualData = self.model.get_actual(idx)
                self.a.set_title("The weekly forecast sales volume of the store's id: " + str(idx))
                self.change_data_tree(idx = str(self.number[0]))
        else:
            if str(self.comboboxForecast.get()) == 'All':
                forecastData = self.model.get_predict()
                actualData = self.model.get_actual()
                self.a.set_title('The total weekly forecast sales volume of the retail chain')
                self.change_data_tree()
            else:
                forecastData = self.model.get_predict(int(self.comboboxForecast.get()))
                actualData = self.model.get_actual(int(self.comboboxForecast.get()))
                self.a.set_title("The weekly forecast sales volume of the store's id: " + self.comboboxForecast.get())
                self.change_data_tree(idx = self.comboboxForecast.get())
        df = sum_weekly_sale_by_week(pd_data)
        theta = df.Date
        self.a.plot(theta.iloc[-33:], actualData, label = 'The actual data')
        self.a.plot(theta.iloc[-33:], forecastData, label = 'The predicted data')
        self.a.legend()
        self.canvas.draw()
        self.a.clear()



    def change_data_tree(self, idx = None):
        self.tree.delete(*self.tree.get_children())
        print(idx)
        if idx == None:
            for i in range(len(data[:1000])):
                if i%2 == 0:
                    self.tree.insert("", END, values=data[i][1:], tags = ('even',))
                else:
                    self.tree.insert("", END, values=data[i][1:], tags=('odd',))
        else:
            for i in range(len(data)):
                if data[i][1] == idx:
                    if i % 2 == 0:
                        self.tree.insert("", END, values=data[i][1:], tags=('even',))
                    else:
                        self.tree.insert("", END, values=data[i][1:], tags=('odd',))

    def forecast_window(self, _class):
        try:
            if self.forecast.state() == "normal":
                self.forcast.focus()
        except:
            self.forcast = Toplevel(self.master)
            _class(self.forcast)
        self.forcast.geometry("512x256")
        self.forcast.resizable(0, 0)

        self.comboboxForecast = ttk.Combobox(self.forcast, values=['All'] + list(set(pd_data.Store)),font = 'Times 14 ')
        self.comboboxForecast.pack()
        self.comboboxForecast.current(0)  # combobox.get()
        self.comboboxForecast.place(x=300, y=20)
        self.label_store_forcast = Label(master=self.forcast, text="Choose the id store:",font = 'Times 14 ')
        self.label_store_forcast.pack()
        self.label_store_forcast.place(x=20, y=20)
        self.comboboxtimeForecast = ttk.Combobox(self.forcast, values=['Week'],font = 'Times 14 ')
        self.comboboxtimeForecast.pack()
        self.comboboxtimeForecast.current(0)  # combobox.get()
        self.comboboxtimeForecast.place(x=300, y=60)
        self.label_time_forecast = Label(master=self.forcast, text="Choose the period:",font = 'Times 14 ')
        self.label_time_forecast.pack()
        self.label_time_forecast.place(x=20, y=60)

        self.button_show_forcast = Button(master=self.forcast, command=self.plotForecast, text='Forecast',font = 'Times 14 ')
        self.button_show_forcast.pack()
        self.button_show_forcast.place(y=150, x=250)

    def regWin(self, _class):
        try:
            if self.recognition.state() == "normal":
                self.recognition.focus()
        except:
            self.recognition = Toplevel(self.master)
            _class(self.recognition)

            self.recognition.geometry("512x256")
            self.recognition.resizable(0, 0)
            self.titlevar = StringVar()
            self.titlevar.set('Please press Speak button to start!')
            self.titleLabel = Label(master = self.recognition, text = 'Voice Recognition', font = 'Times 16 bold italic', fg = 'blue').pack()
            self.content = Label(master = self.recognition, textvariable = self.titlevar, font = 'Times 14', fg = 'blue').pack()
            self.buttonForecast = Button(master=self.recognition, text='Start',
                                 command=self.voicReg,  font = 'Times 14')
            self.buttonForecast.pack()
            self.contentvar = StringVar()
            self.contentlabel = Label(master= self.recognition, textvariable = self.contentvar, font = 'Times 14', fg = 'blue')
            self.contentlabel.pack()
            self.executevar = StringVar()
            self.executelabel = Label(master=self.recognition, textvariable=self.executevar, font='Times 14', fg='blue')
            self.executelabel.pack()

    def voicReg(self):
        guess = recognize_speech_from_mic(self.recognizer, self.microphone)
        # guess["transcription"] = 'before 9'
        if guess["error"]:
            self.contentvar.set('Error: '+ guess['error'])
            # return

        if guess["transcription"]:
            self.contentvar.set('You said: ' + guess['transcription'])
            newString = convertStringToInt(guess["transcription"])
            self.number = [int(s) for s in newString.split() if s.isdigit()]
            if 'report' in newString or 'before' in newString or 'previous' in newString or 'past' in newString:
                if self.number:
                    self.executeReg(True)
                    self.plot(voice=True, idx=self.number[0])
                else:
                    self.executeReg(True)
                    self.plot(voice=True)
            else:
                if 'forecast' in newString or 'after' in newString or 'next' in newString or 'future' in newString:
                    if self.number:
                        self.executeReg(True)
                        self.plotForecast(voice=True, idx=self.number[0])
                    else:
                        self.executeReg(True)
                        self.plotForecast(voice=True)
                else:
                    self.executevar.set("I don't know what you want.")
        else:
            self.executevar.set("I didn't catch that. What did you say?")

    def executeReg(self, understand):
        if understand == True:
            self.executevar.set('I got it. Executing the command... Done!')

    def voiceHelp(self):
        messagebox.showinfo('Voice Recognition', '1. To report properly: You say a sentence which contains at least one word:"before", "past", "previous" and "report".'
                                                 '\n\n2. To forecast properly: You say a sentence which contains at least one word: "forecast", "after", "next" and "future".\n\n'
                                                 '3.If you want only one store to report or forecast, the sentence you said must contain a number.')


class Report:
    def __init__(self, root):
        self.root = root

class Forecast:
    def __init__(self, root):
        self.root = root

class Recognition:
    def __init__(self, root):
        self.root = root

def main():
    root = Tk();
    root.geometry("1080x960")
    root.resizable(0,0)
    window = Window(root)
    root.mainloop()

if __name__ =='__main__':
    column, data = read_data()
    pd_data = read_datapd()
    main()
