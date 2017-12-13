import os
import wx
import json
import config
#from find_probes import find

lstLocation = ['File', 'API']
lstTypes = ['None', 'DHT11', 'DHT22', 'AM2302']
type_values = [0,11,22,2302]


class GUI(wx.Frame):
    def __init__(self, parent, title):
        super(GUI, self).__init__(parent, title=title, size=(550, 400))
        self.init_screen()

    def init_screen(self):
        posX = 0
        posY = 0

        panel0 = wx.Panel(self, size=(250,200))

        self.dataLocation = wx.RadioBox(panel0, label='Data Location',
                                choices=lstLocation, pos=(posX, posY),
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.label1 = wx.StaticText(panel0, label="Host:", pos=(200, posY+30))
        self.label1.Hide()
        self.txtHost = wx.TextCtrl(panel0, pos=(300, posY+25))
        self.txtHost.Hide()

        posY = posY + 70
        st = wx.StaticText(panel0, label="Sensor Probes", pos=(225,posY))

        posY = posY + 20
        self.dhtType1 = wx.RadioBox(panel0, label='DHT Type', choices=lstTypes,
                                majorDimension=1,  pos=(posX, posY),
                                style=wx.RA_SPECIFY_COLS)
        self.dhtOutdoor1 = wx.CheckBox(panel0,label='Outdoor Sensor?',
                                       pos=(110, posY + 20))
        self.dhtType2 = wx.RadioBox(panel0, label='DHT Type', choices=lstTypes,
                                majorDimension=1,  pos=(275, posY),
                                style=wx.RA_SPECIFY_COLS)
        self.dhtOutdoor2 = wx.CheckBox(panel0,label='Outdoor Sensor?',
                                       pos=(400, posY + 20))

        self.dataLocation.Bind(wx.EVT_RADIOBOX, self.onDataLocation)

        posY = posY + 130

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel0, -1, "Delay (seconds):", pos=(5, posY))
        hbox2.Add(label2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtDelay = wx.TextCtrl(panel0, pos=(100, posY))

#        posY = posY + 30
        label3 = wx.StaticText(panel0, -1, "Hive Id:", pos=(300, posY))
        hbox2.Add(label3, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.txtHiveId = wx.TextCtrl(panel0, pos=(350, posY))
  #      posY = posY + 30
  #      self.panel2 = wx.Panel(self, pos=(0, posY), size=(250,150))
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(self.label1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
  #      self.txtHost = wx.TextCtrl(panel0, pos=(100, posY))

        hbox1.Add(self.txtHost, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
#        self.txtHost.Bind(wx.EVT_TEXT, self.OnKeyTyped)
#        self.txtHost.Hide()
        vbox2.Add(hbox1)

        hbox2.Add(self.txtDelay, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
#        self.txtDelay.Bind(wx.EVT_TEXT, self.OnKeyTyped)
        vbox2.Add(hbox2)

        posY = posY + 50
 #       self.panel3 = wx.Panel(self, pos=(0, posY), size=(250,150))
        btnCancel = wx.Button(panel0, wx.ID_ANY, 'Cancel', (170, posY))
        btnCancel.Bind(wx.EVT_BUTTON, self.onBtnCancel)
        btnSave = wx.Button(panel0, wx.ID_ANY, 'Save', (270, posY))
        btnSave.Bind(wx.EVT_BUTTON, self.onBtnSave)

        self.setValues()
        self.Centre()
        self.Show(True)
#        self.panel2.Hide()
        self.Fit()

    def setValues(self):
        self.dataLocation.SetSelection(data['DataStore'])
        if data['probes'].__len__() > 0:
            self.dhtType1.SetSelection(type_values.index(data['probes'][0]['DHTModel']))
            self.dhtOutdoor1.SetValue(bool(data['probes'][0]['outdoor']))
        if data['probes'].__len__() > 1:
            self.dhtType2.SetSelection(type_values.index(data['probes'][1]['DHTModel']))
            self.dhtOutdoor2.SetValue(bool(data['probes'][1]['outdoor']))
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

 #   def ondhtTypes(self, event):
 #       dhtType = self.dhtTypes.GetSelection()

 #   def OnKeyTyped(self, event):
 #       print(event.GetString())

    def onBtnCancel(self, event):
        data = original_data
        self.init_screen()

    def onBtnSave(self, event):
        data['delay'] = int(self.txtDelay.GetValue())
        data['hiveId'] = int(self.txtHiveId.GetValue())
        data['host'] = self.txtHost.GetValue()

        data['DataStore'] = self.dataLocation.GetSelection()
        if data['probes'].__len__() > 0:
            data['probes'][0]['DHTModel'] = type_values[self.dhtType1.GetSelection()]
            data['probes'][0]['outdoor'] = self.dhtOutdoor1.GetValue()
        else:
            data['probes'] = [{'DHTModel': type_values[self.dhtType1.GetSelection()],
                     'outdoor': self.dhtOutdoor1.GetValue()}]

        if data['probes'].__len__() > 1:
            data['probes'][1]['DHTModel'] = type_values[self.dhtType2.GetSelection()]
            data['probes'][1]['outdoor'] = self.dhtOutdoor2.GetValue()
        else:
            data['probes'].append({'DHTModel':
                                type_values[self.dhtType1.GetSelection()],
                                'outdoor': self.dhtOutdoor1.GetValue()})

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