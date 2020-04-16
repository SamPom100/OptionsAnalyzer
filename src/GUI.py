import wx


def onButton():
    print("Button pressed.")

    app = wx.App()
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetDimensions(0, 0, 200, 50)
    dlg = wx.TextEntryDialog(frame, 'Enter a Stock Ticker', 'Text Entry')
    dlg.SetValue("AAPL")
    if dlg.ShowModal() == wx.ID_OK:
        #print('Ticker entered was: %s\n' % dlg.GetValue())
        return dlg.GetValue()
    dlg.Destroy()
