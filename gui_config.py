import wx


class GUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        panel = wx.Panel(self)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.SetSize((300, 200))
        self.SetTitle('Bee Hive Config')
        vbox = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(5, 5)


   #     title = wx.StaticText(panel, label="Title")
  #      author = wx.StaticText(panel, label="Author")
  #      review = wx.StaticText(panel, label="Review")

#        local = wx.CheckBox(panel, label="Local Install")

        sizer.Add(wx.CheckBox(panel, label="Local Install"),
                  pos=(1, 0), flag=wx.LEFT, border=10)

        self.Centre()
        self.Show(True)


    def OnQuit(self, e):
        self.Close()


def main():
    ex = wx.App()
    GUI(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()