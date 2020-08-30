# -*- coding: utf-8 -*-
# Filename: familytree.py


import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn


class FamilyTreePanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
                
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)                        
                
        self.back = btn = wx.Button(self, -1, u'返回')
        vbox.Add(btn, 0, wx.EXPAND|wx.ALL, 15)
        
        sb = wx.StaticBox(self, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        
        gs = wx.GridSizer(2, 1, 0, 10)
        st = wx.StaticText(self, -1, u'孩子')
        pb = platebtn.PlateButton(self, -1, 'AX1', None)
        gs.AddMany([(st, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (pb, 0, wx.ALIGN_CENTER_HORIZONTAL)])
        box.Add(gs, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 20)
        
        gs = wx.GridSizer(2, 2, 0, 40)
        st1 = wx.StaticText(self, -1, u'父亲')
        st2 = wx.StaticText(self, -1, u'母亲')
        pb1 = platebtn.PlateButton(self, -1, 'AA1', None)
        pb2 = platebtn.PlateButton(self, -1, 'AA2', None)
        gs.AddMany([(st1, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (st2, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (pb1, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (pb2, 0, wx.ALIGN_CENTER_HORIZONTAL)])
        box.Add(gs, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 20)
        
        gs = wx.GridSizer(2, 5, 0, 10)
        st1 = wx.StaticText(self, -1, u'祖父')
        st2 = wx.StaticText(self, -1, u'祖母')
        st3 = wx.StaticText(self, -1, u'外祖父')
        st4 = wx.StaticText(self, -1, u'外祖母')
        pb1 = platebtn.PlateButton(self, -1, 'AE1', None)
        pb2 = platebtn.PlateButton(self, -1, 'AE2', None)
        pb3 = platebtn.PlateButton(self, -1, 'AF1', None)
        pb4 = platebtn.PlateButton(self, -1, 'AF2', None)
        gs.AddMany([(st1, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (st2, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (wx.StaticText(self), 0),
                    (st3, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (st4, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (pb1, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (pb2, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (wx.StaticText(self), 0),
                    (pb3, 0, wx.ALIGN_CENTER_HORIZONTAL),
                    (pb4, 0, wx.ALIGN_CENTER_HORIZONTAL)])
        box.Add(gs, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 20)
        
        vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 15)
                
        
class FamilyTree(wx.Frame):
  
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
                
        self.InitUI()
        self.Fit()
        self.Centre()
        self.Show()
        
    def InitUI(self):    
    
        self.panel = panel = FamilyTreePanel(self)
        
        self.statusbar = self.CreateStatusBar()
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.panel.back)
        
    def OnBack(self, event):
        self.Destroy()

    
if __name__ == '__main__':
  
    app = wx.App()
    FamilyTree(None, title=u'血统')
    app.MainLoop()
    
    