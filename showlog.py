# -*- coding: utf-8 -*-
# Filename: showlog.py


from mousecore import *

import wx


class ShowLogPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)       

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)        
        
        self.prev = b_prev = wx.Button(self, -1, u'上一天')
        self.next = b_next = wx.Button(self, -1, u'下一天')        
        
        sb = wx.StaticBox(self, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        fgs = wx.FlexGridSizer(2, 2, 10, 5)
        st1 = wx.StaticText(self, label=u'日期')
        st2 = wx.StaticText(self, label=u'日志')        
        self.dpc = dpc = wx.DatePickerCtrl(self)        
        self.log = tc = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY, size=(350, 200))
        fgs.AddMany([(st1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (dpc, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st2, 0),
                     (tc, 1, wx.EXPAND)])
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableRow(1, 1)
        extra = (5 if os.name == 'posix' else 10)
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(b_prev, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_next, 0, wx.EXPAND|wx.RIGHT, 0)                
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)


class ShowLog(wx.Frame):

    def __init__(self, parent, farm):
        wx.Frame.__init__(self, parent)

        self.farm = farm
        self.parent = parent
        self.statusbar = self.CreateStatusBar()
        self.sep = '\n'+'-'*40+'\n'
        self.InitUI()
        self.SetTitle(u'浏览日志')
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Center()
        if self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                self.Move(p+wx.Point(-350, 0))
            else:                
                self.Move(p+wx.Point(20, 20))        
        self.Show()

    def InitUI(self):
        self.panel = panel = ShowLogPanel(self)        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Update()
        
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, self.panel.dpc)
        self.Bind(wx.EVT_BUTTON, self.OnNext, self.panel.next)
        self.Bind(wx.EVT_BUTTON, self.OnPrev, self.panel.prev)
        
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose,id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])  
        self.SetAcceleratorTable(accel_tbl)
        
    def Update(self):
        date = self.panel.dpc.GetValue().Format('%Y-%m-%d')
        try:
            records = self.farm.logs[date]
            content = self.sep.join([record.show() for record in records])
        except KeyError:
            content = u"暂无记录！"
        self.panel.log.Clear()
        self.panel.log.write(content)
        
    def OnClose(self, evt):
        self.Destroy()
        
    def OnDateChanged(self, event):
        date = event.GetDate().Format('%Y-%m-%d')
        try:
            records = self.farm.logs[date]
            content = self.sep.join([record.show() for record in records])
        except KeyError:
            content = u"暂无记录！"
        self.panel.log.Clear()
        self.panel.log.write(content)
        
    def OnNext(self, evt):
        date = self.panel.dpc.GetValue()
        day = wx.TimeSpan().Day()
        date += day
        self.panel.dpc.SetValue(date)
        s = date.Format('%Y-%m-%d')
        try:
            records = self.farm.logs[s]
            content = self.sep.join([record.show() for record in records])
        except KeyError:
            content = u"暂无记录！"
        self.panel.log.Clear()
        self.panel.log.write(content)
                
    def OnPrev(self, evt):
        date = self.panel.dpc.GetValue()
        day = wx.TimeSpan().Day()
        date -= day
        self.panel.dpc.SetValue(date)        
        s = date.Format('%Y-%m-%d')
        try:
            records = self.farm.logs[s]
            content = self.sep.join([record.show() for record in records])
        except KeyError:
            content = u"暂无记录！"
        self.panel.log.Clear()
        self.panel.log.write(content)


if __name__ == '__main__':

    app = wx.App()
    ShowLog(None, title=u'浏览日志')
    app.MainLoop()
    
    
