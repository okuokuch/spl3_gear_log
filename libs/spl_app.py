from tkinter import *
from tkinter import ttk
import datetime

class Application(ttk.Frame):

    def __init__(self, master:Tk=None):
        super().__init__(master)
        self.master.title('ギアパワーログ取得')
        self.master.geometry('800x450')
        self.font_family = 'calibri'
        self.font_size = 15
        self.font_size_title = 17
        self.grid_x, self.grid_y = 2,2
        self.style = ttk.Style()
        self.style.configure("Custom.TButton",font = (self.font_family, self.font_size))
        self.create_wedgets()

    def create_wedgets(self):
        #Frameの作成
        self.user_auth = ttk.Frame(self.master, relief="ridge", padding=(5,5,5,5))
        self.user_auth.grid(column=0, row=0, sticky=N+W+E+S, padx=5, pady=5)
        self.make_log = ttk.Frame(self.master, relief="ridge", padding=(5,5,5,5))
        self.make_log.grid(column=0, row=1, sticky=N+W+E+S, padx=5, pady=5)
        self.input_output = ttk.Frame(self.master, relief="ridge", padding=(5,5,5,5))
        self.input_output.grid(column=0, row=2, sticky=N+W+E+S, padx=5, pady=5)

        #variableの定義
        self.user_auth_time = StringVar()
        self.user_auth_time.set('前回更新時間：')
        self.user_auth_state = StringVar()
        self.user_auth_state.set('認証状況：要確認')

        #テキスト、ボタン、入力欄の設定
        self.auth_recog = ttk.Label(self.user_auth, text='ユーザ認証', font=(self.font_family, self.font_size_title))
        self.auth_recog_start = ttk.Button(self.user_auth, text='開始', style='Custom.TButton')
        self.auth_entry = ttk.Entry(self.user_auth, font=(self.font_family, self.font_size))
        self.auth_entry_fin = ttk.Button(self.user_auth, text='読取り', command=self.set_time, style='Custom.TButton')
        self.user_auth_time_label = ttk.Label(self.user_auth, textvariable=self.user_auth_time, font=(self.font_family, self.font_size))
        self.user_auth_state_label = ttk.Label(self.user_auth, textvariable=self.user_auth_state, font=(self.font_family, self.font_size))
        self.gear_power_log = ttk.Label(self.make_log, text='ギアパワーログ', font=(self.font_family, self.font_size_title))
        self.start_making_log = ttk.Button(self.make_log, text='自動更新開始', style='Custom.TButton')
        self.stop_makeing_log = ttk.Button(self.make_log, text='自動更新停止', style='Custom.TButton')
        self.drink_label = ttk.Label(self.make_log, text='ドリンク', font=(self.font_family, self.font_size))
        self.drink_combobox = ttk.Combobox(self.make_log, values=('なし', 'メインパワー'), font=(self.font_family, self.font_size), state='readonly')
        self.drink_combobox.current(0)
        self.manual_makeing_log = ttk.Button(self.make_log, text='手動更新', style='Custom.TButton')
        self.manual_makeing_gear_list = ttk.Button(self.make_log, text='手動ギア一覧取得', style='Custom.TButton')
        self.input_output_label = ttk.Label(self.input_output, text='データ入出力', font=(self.font_family, self.font_size_title))
        self.input_json = ttk.Button(self.input_output, text='json入力', style='Custom.TButton')
        self.output_json = ttk.Button(self.input_output, text='json出力', style='Custom.TButton')
        self.json_label = ttk.Label(self.input_output, text='Gear Seed CheckerのDatabaseで利用するためのファイル', font=(self.font_family, self.font_size))
        self.input_csv = ttk.Button(self.input_output, text='csv入力', style='Custom.TButton')
        self.output_csv = ttk.Button(self.input_output, text='csv出力', style='Custom.TButton')
        self.csv_label = ttk.Label(self.input_output, text='ギアパワーログを確認・修正するためのファイル', font=(self.font_family, self.font_size))

        #各種配置の設定
        self.auth_recog.grid(column=0,row=0, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.auth_recog_start.grid(column=0, row=1, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.auth_entry.grid(column=0, row=2, sticky=W+E, padx=self.grid_x, pady=self.grid_y)
        self.auth_entry_fin.grid(column=1, row=2, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.user_auth_time_label.grid(column=0, row=3, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.user_auth_state_label.grid(column=0, row=4, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.gear_power_log.grid(column=0, row=0, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.start_making_log.grid(column=0, row=1, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.stop_makeing_log.grid(column=1, row=1, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.drink_label.grid(column=0, row=2, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.drink_combobox.grid(column=1, row=2, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.manual_makeing_gear_list.grid(column=0, row=3, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.input_output_label.grid(column=0, row=0, columnspan=2, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.input_json.grid(column=0, row=1, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.output_json.grid(column=1, row=1, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.json_label.grid(column=2, row=1, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.input_csv.grid(column=0, row=2, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.output_csv.grid(column=1, row=2, sticky=W, padx=self.grid_x, pady=self.grid_y)
        self.csv_label.grid(column=2, row=2, sticky=W, padx=self.grid_x, pady=self.grid_y)

        #配置の重みづけ
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=2)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.user_auth.columnconfigure(0, weight=1)
        self.user_auth.columnconfigure(1, weight=1)
        self.user_auth.rowconfigure(0, weight=1)
        self.user_auth.rowconfigure(1, weight=1)
        self.user_auth.rowconfigure(2, weight=1)
        self.user_auth.rowconfigure(3, weight=1)
        self.user_auth.rowconfigure(4, weight=1)
        self.make_log.rowconfigure(0, weight=1)
        self.make_log.rowconfigure(1, weight=1)
        self.make_log.rowconfigure(2, weight=1)
        self.make_log.rowconfigure(3, weight=1)
        self.input_output.rowconfigure(0, weight=1)
        self.input_output.rowconfigure(1, weight=1)
        self.input_output.rowconfigure(2, weight=1)

    def set_time(self):
        """テスト用に作成した関数。"""
        dt = datetime.datetime.now()
        self.user_auth_time.set('前回更新時間{0}-{1}-{2} {3}:{4}:{5}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))

root = Tk()
app = Application(master = root)
app.mainloop()