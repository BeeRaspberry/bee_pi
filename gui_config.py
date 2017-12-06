import os
import wx
import json

def loadConfig(file_name):
    global data, original_data

    data = {'host': 'localhost', 'DHTPin': 4, 'DHTModel': 0,
            'DataStore': 0, 'delay': 300, 'hiveId': 1,
            'filename': 'beedata.csv'}

    config_exists = os.path.exists(file_name)

    if config_exists:
        with open(file_name) as data_file:
            data = json.load(data_file)

    original_data = data

def writeConfig(fileName):
    with open(fileName, "w") as data_file:
        json.dump(data, data_file)

class GUI(wx.Frame):
    def __init__(self, parent, title):
        super(GUI, self).__init__(parent, title=title, size=(250, 400))
        self.init_screen()

    def init_screen(self):
        posX = 0
        posY = 0

        panel0 = wx.Panel(self, size=(250,200))
        lstLocation = ['File', 'API']
        lstTypes = ['DHT11', 'DHT22', 'AM2302']
        self.dataLocation = wx.RadioBox(panel0, label='Data Location',
                                choices=lstLocation, pos=(posX, posY),
                                majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.dhtTypes = wx.RadioBox(panel0, label='DHT Type', choices=lstTypes,
                                majorDimension=1,  pos=(110, posY),
                                style=wx.RA_SPECIFY_COLS)
        self.dataLocation.Bind(wx.EVT_RADIOBOX, self.onDataLocation)

        posY = posY + 110
 #       panel1 = wx.Panel(self, pos=(posX, posY), size=(250,200))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel0, -1, "Delay (seconds):", pos=(5, posY))
        hbox2.Add(label2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtDelay = wx.TextCtrl(panel0, pos=(100, posY))

        posY = posY + 30
        label3 = wx.StaticText(panel0, -1, "Hive Id:", pos=(5, posY))
        hbox2.Add(label3, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtHiveId = wx.TextCtrl(panel0, pos=(100, posY))

        posY = posY + 30
  #      self.panel2 = wx.Panel(self, pos=(0, posY), size=(250,150))
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.label1 = wx.StaticText(panel0, label="Host:", pos=(5,posY))
        self.label1.Hide()

        hbox1.Add(self.label1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtHost = wx.TextCtrl(panel0, pos=(100, posY))

        hbox1.Add(self.txtHost, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtHost.Bind(wx.EVT_TEXT, self.OnKeyTyped)
        self.txtHost.Hide()
        vbox2.Add(hbox1)

        hbox2.Add(self.txtDelay, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtDelay.Bind(wx.EVT_TEXT, self.OnKeyTyped)
        vbox2.Add(hbox2)

        posY = posY + 50
 #       self.panel3 = wx.Panel(self, pos=(0, posY), size=(250,150))
        btnCancel = wx.Button(panel0, wx.ID_ANY, 'Cancel', (10, posY))
        btnCancel.Bind(wx.EVT_BUTTON, self.onBtnCancel)
        btnSave = wx.Button(panel0, wx.ID_ANY, 'Save', (110, posY))
        btnSave.Bind(wx.EVT_BUTTON, self.onBtnSave)

        self.setValues()
        self.Centre()
        self.Show(True)
#        self.panel2.Hide()
        self.Fit()

    def setValues(self):
        self.dataLocation.SetSelection(data['DataStore'])
        self.dhtTypes.SetSelection(data['DHTModel'])
        self.txtDelay.SetValue(str(data['delay']))
        self.txtHiveId.SetValue(str(data['hiveId']))
        self.txtHost.SetValue(data['host'])

    def onDataLocation(self, event):
        location = self.dataLocation.GetSelection()
        if location == 1:
            self.txtHost.Show(True)
            self.label1.Show(True)
        else:
            self.txtHost.Hide()
            self.label1.Hide()

    def ondhtTypes(self, event):
        dhtTypes = self.dhtTypes.GetSelection()

    def OnKeyTyped(self, event):
        print(event.GetString())

    def onBtnCancel(self, event):
        data = original_data
        self.init_screen()

    def onBtnSave(self, event):
        data['DataStore'] = self.dataLocation.GetSelection()
        data['DHTModel'] = self.dhtTypes.GetSelection()
        data['delay'] = int(self.txtDelay.GetValue())
        data['hiveId'] = int(self.txtHiveId.GetValue())
        data['host'] = self.txtHost.GetValue()
        writeConfig('config.json')
        self.Close()

    def OnQuit(self, e):
        self.Close()


def main():
    ex = wx.App()
    loadConfig('config.json')
    GUI(None, 'Bee Hive Config')
    ex.MainLoop()


if __name__ == '__main__':
    main()