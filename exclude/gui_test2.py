import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(300, 200))

        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)

        self.rb1 = wx.RadioButton(pnl, 11, label='Value A',
                                  pos=(10, 10), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(pnl, 22, label='Value B', pos=(10, 40))
        self.rb3 = wx.RadioButton(pnl, 33, label='Value C', pos=(10, 70))


 #       self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

        lblList = ['Value X', 'Value Y', 'Value Z']

        self.rbox = wx.RadioBox(pnl, label='RadioBox', pos=(80, 10), choices=lblList,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onRadioBox)

        self.Centre()
        self.Show(True)

    def OnRadiogroup(self, e):
        rb = e.GetEventObject()
        print
        rb.GetLabel(), ' is clicked from Radio Group'

    def onRadioBox(self, e):
        print
        self.rbox.GetStringSelection(), ' is clicked from Radio Box'


ex = wx.App()
Example(None, 'RadioButton and RadioBox')
ex.MainLoop()