# -*- coding: utf-8 -*-


import wx
    
from mousecore import *
from validator import *


class AddNewCagePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        color = 'STEEL BLUE'

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        sb = wx.StaticBox(self, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)

        fgs = wx.FlexGridSizer(2, 4, 10, 10)
        st1 = wx.StaticText(self, label=u'鼠房')
        st2 = wx.StaticText(self, label=u'鼠笼编号')
        st3 = wx.StaticText(self, label=u'至')
        self.house = tc1 = wx.TextCtrl(self, -1, '1', validator=MouseValidator(0))
        self.cmin = tc2 = wx.TextCtrl(self, -1, validator=MouseValidator(0))
        self.cmax = tc3 = wx.TextCtrl(self, -1, validator=MouseValidator(0))
        fgs.AddMany([(st1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (wx.StaticText(self)),
                     (wx.StaticText(self)),
                     (st2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st3, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc3, 0, wx.ALIGN_CENTER_VERTICAL)])
        extra = (5 if os.name == 'posix' else 10)
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add = add = wx.Button(self, -1, u'添加')
        self.can = can = wx.Button(self, -1, u'取消')
        self.add.Disable()
        hbox.Add(add, 0, wx.RIGHT, 10)
        hbox.Add(can, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)        


class AddNewCage(wx.Frame):

    def __init__(self, parent, farm):
        wx.Frame.__init__(self, parent, style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        
        self.statusbar = self.CreateStatusBar()
        self.parent = parent
        self.farm = farm
        self.InitUI()
        self.SetTitle(u'添加鼠笼')
        self.Fit()
        self.Center()
        if self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                pass
            else:
                self.Move(p+wx.Point(20, 20))
        self.Show()

    def InitUI(self):

        self.panel = AddNewCagePanel(self)

        self.sizer = sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)        
        
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnCancel, id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)

        self.panel.add.Bind(wx.EVT_BUTTON, self.OnAdd)
        self.panel.can.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.Bind(wx.EVT_TEXT, self.OnChange, self.panel.house)
        self.Bind(wx.EVT_TEXT, self.OnChange, self.panel.cmin)
        self.Bind(wx.EVT_TEXT, self.OnChange, self.panel.cmax)
        
    def OnChange(self, event):
        house = self.panel.house.GetValue()
        cmin = self.panel.cmin.GetValue()
        cmax = self.panel.cmax.GetValue()
        if house and cmin and cmax and (1 <= int(cmin) <= int(cmax)):
            self.panel.add.Enable()
        else:
            self.panel.add.Disable()
        
    def OnCancel(self, event):
        self.Destroy()
        
    def OnAdd(self, event):
        house = self.panel.house.GetValue()
        cmin = self.panel.cmin.GetValue()
        cmax = self.panel.cmax.GetValue()
        if house == '1':
            cagelist = [str(c) for c in range(int(cmin), int(cmax)+1)]
        else:
            cagelist = [house+'-'+str(c) for c in range(int(cmin), int(cmax)+1)]
        feedback = self.farm.new_cages(cagelist)
        for child in self.parent.GetChildren():
            try:
                if child.GetTitle() == SymList.nlist[1]:
                    child.Update(2)
                else:
                    child.Update()
            except:
                child.Update()
        self.statusbar.SetStatusText(feedback)
        self.panel.cmin.SetValue('')
        self.panel.cmax.SetValue('')
        self.panel.house.SetFocus()


if __name__ == '__main__':

    app = wx.App()
    AddNewCage(None)
    app.MainLoop()

