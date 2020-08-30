#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn
    
from mousecore import *


class AddNewPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        color = 'STEEL BLUE'
        co = wx.Colour(0, 0, 0)
        co.SetFromName('RED')

        self.sizer = vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        self.frame = parent

        sb = wx.StaticBox(self, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)

        fgs = wx.FlexGridSizer(11, 2, 10, 10)
        st1 = wx.StaticText(self, label=u'笼号')
        st2 = wx.StaticText(self, label=u'性别')
        st3 = wx.StaticText(self, label=u'毛色')
        st4 = wx.StaticText(self, label=u'鼠号')
        st5 = wx.StaticText(self, label=u'出生日期')
        st6 = wx.StaticText(self, label=u'父亲')
        st7 = wx.StaticText(self, label=u'母亲')
        st8 = wx.StaticText(self, label=u'附注')
        st9 = wx.StaticText(self, label=u'级别')
        st10 = wx.StaticText(self, label=u'状态')
        self.stdead = st11 = wx.StaticText(self, label=u'死亡日期')
        self.mid = tc4 = wx.TextCtrl(self, -1)
        self.cid = tc1 = wx.TextCtrl(self, -1)
        self.gender = ch2 = wx.Choice(self, -1, choices=SymList.glist, size=(100, -1))
        self.gender.SetStringSelection(SymList.glist[0])
        self.color = ch3 = wx.ComboBox(self, -1, choices=SymList.clist, size=(100, -1))
        try:
            self.color.SetValue(SymList.clist[0])
        except:
            pass
        self.born = dp5 = wx.DatePickerCtrl(self)
        self.dead = dp11 = wx.DatePickerCtrl(self)
        self.father = tc6 = wx.TextCtrl(self, -1)
        self.mother = tc7 = wx.TextCtrl(self, -1)                                      
        self.cmt = tc8 = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))
        self.level = ch9 = wx.Choice(self, -1, choices=SymList.llist, size=(100, -1))
        self.level.SetStringSelection(SymList.llist[0])
        self.status = ch10 = wx.Choice(self, -1, choices=SymList.slist, size=(100, -1))
        self.status.SetStringSelection(SymList.slist[0])
        fgs.AddMany([(st4, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc4, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc1, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st5, 0, wx.ALIGN_CENTER_VERTICAL),
                     (dp5, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st11, 0, wx.ALIGN_CENTER_VERTICAL),
                     (dp11, 0, wx.ALIGN_CENTER_VERTICAL),                     
                     (st2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (ch2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st3, 0, wx.ALIGN_CENTER_VERTICAL),
                     (ch3, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st9, 0, wx.ALIGN_CENTER_VERTICAL),
                     (ch9, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st10, 0, wx.ALIGN_CENTER_VERTICAL),
                     (ch10, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st6, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc6, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st7, 0, wx.ALIGN_CENTER_VERTICAL),
                     (tc7, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st8, 0),
                     (tc8, 1, wx.EXPAND)])
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableRow(10, 1)
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
        
        st11.Hide()
        dp11.Hide()

        self.add.Bind(wx.EVT_BUTTON, self.frame.OnAdd)
        self.can.Bind(wx.EVT_BUTTON, self.frame.OnCancel)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.mid)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.cid)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.father)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.mother)
        self.Bind(wx.EVT_CHOICE, self.frame.OnChange, self.status)
        self.Bind(wx.EVT_DATE_CHANGED, self.frame.OnChange, self.born)
        self.Bind(wx.EVT_DATE_CHANGED, self.frame.OnChange, self.dead)


class AddNew(wx.Frame):

    def __init__(self, parent, farm, mid=None):
        wx.Frame.__init__(self, parent)
        
        self.statusbar = self.CreateStatusBar()
        self.parent = parent
        self.farm = farm
        self.mid = mid
        self.InitUI()
        self.SetTitle(u'添加鼠')
        self.Fit()
        self.Center()
        
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnCancel, id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)
        
        if self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                self.Move(p+wx.Point(-250, 0))
            else:
                self.Move(p+wx.Point(20, 20))
        self.Show()

    def InitUI(self):
        self.panel = AddNewPanel(self)
        self.sizer = sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        if self.mid:
            self.panel.mid.SetValue(self.mid)
        
    def OnChange(self, event):
        cid = self.panel.cid.GetValue()
        mid = self.panel.mid.GetValue()
        father = self.panel.father.GetValue()
        mother = self.panel.mother.GetValue()
        status = self.panel.status.GetStringSelection()
        born = self.panel.born.GetValue().Format('%Y-%m-%d')
        dead = self.panel.dead.GetValue().Format('%Y-%m-%d')
        if status in [u'正常', u'生病']:
            self.panel.cid.Enable()        
            self.panel.dead.Hide()
            self.panel.stdead.Hide()
            if mid and cid and father and mother:
                self.panel.add.Enable()
            else:
                self.panel.add.Disable()
        elif status == u'死亡':
            self.panel.cid.Disable()
            self.panel.dead.Show()
            self.panel.stdead.Show()
            if mid and father and mother and (dead>=born):
                self.panel.add.Enable()
            else:
                self.panel.add.Disable()
        else:
            self.panel.cid.Disable()
            self.panel.dead.Hide()
            self.panel.stdead.Hide()            
            if mid and father and mother:
                self.panel.add.Enable()
            else:
                self.panel.add.Disable()            
        self.Fit()
        
    def OnCancel(self, event):
        self.Destroy()
        
    def Update(self):
        self.panel.mid.SetValue('')
        self.panel.cid.SetValue('')
        self.panel.gender.SetStringSelection(SymList.glist[0])
        self.panel.color.SetItems(SymList.clist)
        try:
            self.panel.color.SetValue(SymList.clist[0])
        except:
            pass
        dt = wx.DateTime()
        self.panel.born.SetValue(dt.Today())
        self.panel.dead.SetValue(dt.Today())
        self.panel.father.SetValue('')
        self.panel.mother.SetValue('')                                      
        self.panel.cmt.SetValue('')
        self.panel.level.SetStringSelection(SymList.llist[0])
        self.panel.status.SetStringSelection(SymList.slist[0])
        self.panel.dead.Hide()
        self.panel.stdead.Hide() 
        self.panel.mid.SetFocus()
        self.panel.cid.Enable()
        self.Layout()
        self.Fit()

    def OnAdd(self, event):
        mid = self.panel.mid.GetValue()
        cid = self.panel.cid.GetValue()
        gender = self.panel.gender.GetStringSelection()
        color = self.panel.color.GetValue()
        borndate = self.panel.born.GetValue().Format('%Y-%m-%d')
        deathdate = self.panel.dead.GetValue().Format('%Y-%m-%d')
        father = self.panel.father.GetValue()
        mother = self.panel.mother.GetValue()
        level = self.panel.level.GetStringSelection()
        status = self.panel.status.GetStringSelection()        
        comment = self.panel.cmt.GetValue()
        mouse = Mouse(mid, gender, color, mother, father, borndate)
        if status == u'死亡':
            mouse.deathdate = deathdate
        mouse.status = status
        mouse.level = level
        mouse.comment = comment
        feedback = self.farm.add_mouses([mouse])[0]
        if feedback.startswith(u'成功'):
            if color not in SymList.clist:
                SymList.add(['color', color])
            feedback2 = self.farm.move(mid, cid)
            if feedback2.startswith(u'移动') or (status in SymList.slist[2:]):
                self.statusbar.SetStatusText(feedback)
            else:
                self.statusbar.SetStatusText(feedback+' '+feedback2)
            for child in self.parent.GetChildren():
                child.Update()
        else:
            self.statusbar.SetStatusText(feedback)
            self.panel.mid.SetFocus()


if __name__ == '__main__':

    app = wx.App()
    AddNew(None, title=u'添加鼠')
    app.MainLoop()

