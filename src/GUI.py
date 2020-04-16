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


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None,
                          title="Communication Port", size=(300, 200))
        self.panel = wx.Panel(self)
        self.selComButton = wx.Button(self.panel, -1, "Select Comport")
        self.selComButton.SetToolTip("Select Comport")
        self.selComButton.Bind(wx.EVT_BUTTON, self.selectPopUp)

    def selectPopUp(self, event):
        dlg = wx.SingleChoiceDialog(None, "Pick a com port", "Com ports", [
                                    "Com1", "Com2", "Com3", "Com4"], wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            res = dlg.GetStringSelection()
            self.selComButton.SetLabel(res)
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
