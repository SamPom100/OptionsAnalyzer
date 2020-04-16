import wx


def onButton():
    print("Button pressed.")

    app = wx.App()
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetDimensions(0, 0, 200, 50)
    dlg = wx.TextEntryDialog(frame, 'Enter a Stock Ticker', 'Text Entry')
    dlg.SetValue("AAPL")
    if dlg.ShowModal() == wx.ID_OK:
        # print('Ticker entered was: %s\n' % dlg.GetValue())
        return dlg.GetValue()
    dlg.Destroy()


def pickStrikePrice():

    class MyFrame(wx.Frame):
        def __init__(self, parent, title):
            super(MyFrame, self).__init__(parent, title=title, size=(600, 400))
            self.panel = MyPanel(self)

    class MyPanel(wx.Panel):
        def __init__(self, parent):
            super(MyPanel, self).__init__(parent)
            self.label = wx.StaticText(
                self, label="What Programming Language You Like?", pos=(50, 30))
            languages = ['Java', 'C++', 'C#',
                         'Python', 'Erlang', 'PHP', 'Ruby']
            self.combobox = wx.ComboBox(self, choices=languages, pos=(50, 50))
            self.label2 = wx.StaticText(self, label="", pos=(50, 80))
            self.Bind(wx.EVT_COMBOBOX, self.OnCombo)

        def OnCombo(self, event):
            self.label2.SetLabel("You Like " + self.combobox.GetValue())

    class MyApp(wx.App):
        def OnInit(self):
            self.frame = MyFrame(parent=None, title="Combobox")
            self.frame.Show()
            return True

    app = MyApp()
    app.MainLoop()
