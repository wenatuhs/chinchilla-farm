#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

from mousecore import *
import mousecard

class NewBornPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        color = 'STEEL BLUE'
        co = wx.Colour(0, 0, 0)
        co.SetFromName('RED')

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        sb = wx.StaticBox(self, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)

        fgs = wx.FlexGridSizer(8, 2, 10, 10)
        st1 = wx.StaticText(self, label=u'笼号')
        st2 = wx.StaticText(self, label=u'性别')
        st3 = wx.StaticText(self, label=u'毛色')
        st4 = wx.StaticText(self, label=u'鼠号')
        st5 = wx.StaticText(self, label=u'出生日期')
        st6 = wx.StaticText(self, label=u'父亲')
        st7 = wx.StaticText(self, label=u'母亲')
        st8 = wx.StaticText(self, label=u'备注')
        self.cid = tc1 = wx.TextCtrl(self, -1)
        self.gender = ch2 = wx.Choice(self, -1, choices=SymList.glist, size=(100, -1))
        self.gender.SetStringSelection(SymList.glist[0])
        self.color = ch3 = wx.ComboBox(self, -1, choices=SymList.clist, size=(100, -1))
        try:
            self.color.SetValue(SymList.clist[0])
        except:
            pass
        self.mid = tc4 = wx.TextCtrl(self, -1)
        self.born = dp5 = wx.DatePickerCtrl(self)
        self.father = pb6 = platebtn.PlateButton(self, -1, '')
        self.mother = pb7 = platebtn.PlateButton(self, -1, '')
        self.comment = tc8 = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))
        fgs.AddMany([(st1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st4, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc4, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (ch2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st3, 0, wx.ALIGN_CENTER_VERTICAL),
                     (ch3, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st5, 0, wx.ALIGN_CENTER_VERTICAL),
                     (dp5, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st6, 0, wx.ALIGN_CENTER_VERTICAL),
                     (pb6, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st7, 0, wx.ALIGN_CENTER_VERTICAL),
                     (pb7, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st8, 0),
                     (tc8, 1, wx.EXPAND)])
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableRow(7, 1)
        extra = (5 if os.name == 'posix' else 10)
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add = add = wx.Button(self, -1, u'添加')
        self.can = can = wx.Button(self, -1, u'取消')
        add.Disable()
        hbox.Add(add, 0, wx.RIGHT, 10)
        hbox.Add(can, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)


class NewBorn(wx.Frame):

    def __init__(self, parent, farm):
        wx.Frame.__init__(self, parent)
        
        self.statusbar = self.CreateStatusBar()
        self.farm = farm
        self.parent = parent
        self.InitUI()
        self.Fit()
        self.SetTitle(u'新鼠出生')
        self.Center()
        if self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                self.Move(p+wx.Point(-250, 0))
            else:
                self.Move(p+wx.Point(20, 20))
        self.Show()        

    def InitUI(self):

        self.panel = NewBornPanel(self)
        date = self.panel.born.GetValue().Format('%Y-%m-%d')
        self.panel.mid.SetValue(self.farm.new_id(date))
        
        self.panel.father.Disable()
        self.panel.mother.Disable()

        self.sizer = sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnCancel,id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])  
        self.SetAcceleratorTable(accel_tbl)        

        self.Bind(wx.EVT_TEXT, self.OnChange, self.panel.cid)
        self.Bind(wx.EVT_DATE_CHANGED, self.OnChange, self.panel.born)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.panel.add)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.panel.can)

    def Update(self):
        cid = self.panel.cid.GetValue()
        date = self.panel.born.GetValue().Format('%Y-%m-%d')
        mid = self.farm.new_id(date)
        self.panel.mid.SetValue(mid)
        self.panel.gender.SetStringSelection(SymList.glist[0])
        self.panel.color.SetItems(SymList.clist)
        try:
            self.panel.color.SetValue(SymList.clist[0])
        except:
            pass
        self.panel.comment.SetValue('')
        test = self.farm.pre_born(cid, date)
        if test[0]:
            self.panel.father.SetLabel(test[1])
            self.panel.father.Enable()
            self.Bind(wx.EVT_BUTTON, self.OnMouseCard, self.panel.father)
            self.panel.mother.SetLabel(test[2])
            self.panel.mother.Enable()
            self.Bind(wx.EVT_BUTTON, self.OnMouseCard, self.panel.mother)
            self.panel.add.Enable()
            self.Fit()
        else:
            self.panel.father.SetLabel('')
            self.panel.father.Disable()
            self.panel.mother.SetLabel('')
            self.panel.mother.Disable()
            self.panel.add.Disable()
            self.Fit()
        
    def OnChange(self, event):
        cid = self.panel.cid.GetValue()
        date = self.panel.born.GetValue().Format('%Y-%m-%d')
        mid = self.farm.new_id(date)
        self.panel.mid.SetValue(mid)
        test = self.farm.pre_born(cid, date)
        if test[0]:
            self.panel.father.SetLabel(test[1])
            self.panel.father.Enable()
            self.Bind(wx.EVT_BUTTON, self.OnMouseCard, self.panel.father)
            self.panel.mother.SetLabel(test[2])
            self.panel.mother.Enable()
            self.Bind(wx.EVT_BUTTON, self.OnMouseCard, self.panel.mother)
            self.panel.add.Enable()
            self.Fit()
        else:
            self.panel.father.SetLabel('')
            self.panel.father.Disable()
            self.panel.mother.SetLabel('')
            self.panel.mother.Disable()
            self.panel.add.Disable()
            self.Fit()
            
    def OnMouseCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        mousecard.MouseCard(self.parent, pb.GetLabel(), self.farm, pos=pos)

    def OnCancel(self, event):
        self.Destroy()

    def OnAdd(self, event):
        mid = self.panel.mid.GetValue()
        cid = self.panel.cid.GetValue()
        gender = self.panel.gender.GetStringSelection()
        color = self.panel.color.GetValue()
        if color not in SymList.clist:
            SymList.add(['color', color])
        borndate = self.panel.born.GetValue().Format('%Y-%m-%d')
        comment = self.panel.comment.GetValue()
                
        feedback = self.farm.born(cid, mid, gender, color, borndate, comment)
        self.statusbar.SetStatusText(feedback)
        self.panel.gender.SetFocus()
        
        for child in self.parent.GetChildren():
            child.Update()

if __name__ == '__main__':

    app = wx.App()
    NewBorn(None, title=u'出生登记')
    app.MainLoop()

