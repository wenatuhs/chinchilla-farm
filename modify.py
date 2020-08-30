#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx

from mousecore import *
from validator import *


class ModifyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        color = 'STEEL BLUE'
        co = wx.Colour(0, 0, 0)
        co.SetFromName('RED')

        self.sizer = vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        self.frame = parent

        extra = (5 if os.name == 'posix' else 10)

        sb = wx.StaticBox(self, label=u'待修改鼠鼠号')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.oid = tc0 = wx.TextCtrl(self, -1)
        box.Add(self.oid, 1, wx.EXPAND|wx.ALL, extra)
        vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        sb = wx.StaticBox(self, label=u'待修改鼠信息')
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
        self.mid = tc4 = wx.TextCtrl(self, -1, validator=MouseValidator(1))
        self.cid = tc1 = wx.TextCtrl(self, -1, validator=MouseValidator(2))
        self.gender = ch2 = wx.Choice(self, -1, choices=SymList.glist, size=(100, -1))
        self.gender.SetSelection(-1)
        self.color = ch3 = wx.ComboBox(self, -1, choices=SymList.clist, size=(100, -1))
        self.color.SetValue('')
        self.born = dp5 = wx.DatePickerCtrl(self)
        self.dead = dp11 = wx.DatePickerCtrl(self)
        self.father = tc6 = wx.TextCtrl(self, -1, validator=MouseValidator(3))
        self.mother = tc7 = wx.TextCtrl(self, -1, validator=MouseValidator(3))
        self.cmt = tc8 = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))
        self.level = ch9 = wx.Choice(self, -1, choices=SymList.llist, size=(100, -1))
        self.level.SetStringSelection(SymList.llist[0])
        self.status = ch10 = wx.Choice(self, -1, choices=SymList.slist, size=(100, -1))
        self.status.SetStringSelection(SymList.slist[0])
        self.mid.Disable()
        self.cid.Disable()
        self.gender.Disable()
        self.color.Disable()
        self.born.Disable()
        self.dead.Disable()
        self.father.Disable()
        self.mother.Disable()
        self.cmt.Disable()
        self.level.Disable()
        self.status.Disable()
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
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, extra)
        vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add = add = wx.Button(self, -1, u'修改')
        self.can = can = wx.Button(self, -1, u'取消')
        self.add.Disable()
        hbox.Add(add, 0, wx.RIGHT, 10)
        hbox.Add(can, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)

        st11.Hide()
        dp11.Hide()

        self.add.Bind(wx.EVT_BUTTON, self.frame.OnModify)
        self.can.Bind(wx.EVT_BUTTON, self.frame.OnCancel)
        self.Bind(wx.EVT_TEXT, self.frame.OnSearch, self.oid)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.mid)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.cid)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.father)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.mother)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.cmt)
        self.Bind(wx.EVT_CHOICE, self.frame.OnChange, self.gender)
        self.Bind(wx.EVT_CHOICE, self.frame.OnChange, self.status)
        self.Bind(wx.EVT_COMBOBOX, self.frame.OnChange, self.color)
        self.Bind(wx.EVT_TEXT, self.frame.OnChange, self.color)
        self.Bind(wx.EVT_DATE_CHANGED, self.frame.OnChange, self.born)
        self.Bind(wx.EVT_DATE_CHANGED, self.frame.OnChange, self.dead)


class Modify(wx.Frame):

    def __init__(self, parent, farm, mid=None):
        wx.Frame.__init__(self, parent)

        self.statusbar = self.CreateStatusBar()
        self.parent = parent
        self.farm = farm
        self.mid = mid
        self.InitUI()
        self.SetTitle(u'修改鼠')
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Center()

        if self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                self.Move(p+wx.Point(-250, 0))
            else:
                self.Move(p+wx.Point(20, 20))
        self.Show()

    def InitUI(self):
        self.panel = ModifyPanel(self)
        self.sizer = sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        if self.mid:
            self.panel.mid.SetValue(self.mid)
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnCancel, id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        self.x0, self.y0 = self.GetSizeTuple()
        evt.Skip()

    def OnSearch(self, event):
        mid = self.panel.oid.GetValue()
        try:
            m = self.farm.mouses[mid]
            self.panel.mid.ChangeValue(mid)
            self.panel.cid.ChangeValue(m.cage or '')
            self.panel.gender.SetStringSelection(m.gender)
            self.panel.color.ChangeValue(m.color)
            self.panel.father.ChangeValue(m.father)
            self.panel.mother.ChangeValue(m.mother)
            self.panel.status.SetStringSelection(m.status)
            self.panel.level.SetStringSelection(m.level)
            self.panel.cmt.ChangeValue(m.comment)
            self.panel.mid.Enable()
            self.panel.cid.Enable()
            self.panel.gender.Enable()
            self.panel.color.Enable()
            self.panel.born.Enable()
            self.panel.dead.Enable()
            self.panel.father.Enable()
            self.panel.mother.Enable()
            self.panel.cmt.Enable()
            self.panel.level.Enable()
            self.panel.status.Enable()
            if m.status == u'死亡':
                self.panel.cid.Disable()
                self.panel.dead.Show()
                self.panel.stdead.Show()
            else:
                self.panel.cid.Enable()
                self.panel.dead.Hide()
                self.panel.stdead.Hide()
            dt = wx.DateTime()
            dt.ParseFormat(m.borndate, "%Y-%m-%d")
            self.panel.born.SetValue(dt)
            if dt.ParseFormat(m.deathdate or '', "%Y-%m-%d"):
                self.panel.dead.SetValue(dt)
            self.panel.mid.SetValue(mid)
        except KeyError:
            self.panel.mid.ChangeValue('')
            self.panel.cid.ChangeValue('')
            self.panel.gender.SetSelection(-1)
            self.panel.color.ChangeValue('')
            dt = wx.DateTime()
            self.panel.born.SetValue(dt.Today())
            self.panel.dead.SetValue(dt.Today())
            self.panel.father.ChangeValue('')
            self.panel.mother.ChangeValue('')
            self.panel.cmt.ChangeValue('')
            self.panel.level.SetStringSelection(SymList.llist[0])
            self.panel.status.SetStringSelection(SymList.slist[0])
            self.panel.dead.Hide()
            self.panel.stdead.Hide()
            self.panel.mid.Disable()
            self.panel.cid.Disable()
            self.panel.gender.Disable()
            self.panel.color.Disable()
            self.panel.born.Disable()
            self.panel.dead.Disable()
            self.panel.father.Disable()
            self.panel.mother.Disable()
            self.panel.cmt.Disable()
            self.panel.level.Disable()
            self.panel.status.Disable()
            self.panel.add.Disable()
        self.sizer.Layout()
        self.Unbind(wx.EVT_SIZE)
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnChange(self, event):
        mid = self.panel.mid.GetValue()
        cid = self.panel.cid.GetValue()
        gender = self.panel.gender.GetStringSelection()
        color = self.panel.color.GetValue()
        father = self.panel.father.GetValue()
        mother = self.panel.mother.GetValue()
        status = self.panel.status.GetStringSelection()
        born = self.panel.born.GetValue().Format('%Y-%m-%d')
        dead = self.panel.dead.GetValue().Format('%Y-%m-%d')
        if status in [u'正常', u'生病']:
            self.panel.cid.Enable()
            self.panel.dead.Hide()
            self.panel.stdead.Hide()
            if mid and cid and father and mother and gender and color:
                self.panel.add.Enable()
            else:
                self.panel.add.Disable()
        elif status == u'死亡':
            self.panel.cid.Disable()
            self.panel.dead.Show()
            self.panel.stdead.Show()
            if mid and father and mother and (dead>=born) and gender and color:
                self.panel.add.Enable()
            else:
                self.panel.add.Disable()
        else:
            self.panel.cid.Disable()
            self.panel.dead.Hide()
            self.panel.stdead.Hide()
            if mid and father and mother and gender and color:
                self.panel.add.Enable()
            else:
                self.panel.add.Disable()
        self.sizer.Layout()
        self.Unbind(wx.EVT_SIZE)
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnCancel(self, event):
        self.Destroy()

    def Update(self, flag=0):
        if flag:
            self.panel.oid.ChangeValue('')
            self.panel.mid.ChangeValue('')
            self.panel.cid.ChangeValue('')
            self.panel.gender.SetSelection(-1)
            self.panel.color.ChangeValue('')
            dt = wx.DateTime()
            self.panel.born.SetValue(dt.Today())
            self.panel.dead.SetValue(dt.Today())
            self.panel.father.ChangeValue('')
            self.panel.mother.ChangeValue('')
            self.panel.cmt.ChangeValue('')
            self.panel.level.SetStringSelection(SymList.llist[0])
            self.panel.status.SetStringSelection(SymList.slist[0])
            self.panel.dead.Hide()
            self.panel.stdead.Hide()
            self.panel.mid.Disable()
            self.panel.cid.Disable()
            self.panel.gender.Disable()
            self.panel.color.Disable()
            self.panel.born.Disable()
            self.panel.dead.Disable()
            self.panel.father.Disable()
            self.panel.mother.Disable()
            self.panel.cmt.Disable()
            self.panel.level.Disable()
            self.panel.status.Disable()
            self.panel.add.Disable()
            self.Layout()
        else:
            self.panel.color.SetItems(SymList.clist)
            self.panel.oid.SetValue(self.panel.oid.GetValue())
        self.sizer.Layout()
        self.Unbind(wx.EVT_SIZE)
        x1, y1 = self.GetBestSizeTuple()
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnModify(self, event):
        oid = self.panel.oid.GetValue()
        mid = self.panel.mid.GetValue()
        ocid = self.farm.mouses[oid].cage
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
        if status in [u'已售', u'死亡']:
            cid = ''
        # 判断修改是否可行；不可行的情形：改动后笼号不存在或者改动后鼠号已存在
        feedback = u'修改成功！'
        if (cid != ocid) and (not self.farm.check_cage(cid)):
            feedback = u'修改失败：笼 ' + cid + u' 不存在！'
        if (mid != oid) and self.farm.check_mouse(mid):
            feedback = u'修改失败：鼠 ' + mid + u' 已存在！'
        # 根据修改是否可行，实际执行操作
        self.statusbar.SetStatusText(feedback)
        if feedback.startswith(u'修改成功'):
            m = self.farm.mouses[oid]
            m.id = mid
            m.cage = cid
            m.gender = gender
            m.color = color
            m.borndate = borndate
            m.father = father
            m.mother = mother
            m.level = level
            m.status = status
            m.comment = comment
            if m.status == u'死亡':
                m.deathdate = deathdate
            if ocid:
                self.farm.cages[ocid].check_out(oid)
            del self.farm.mouses[oid]
            self.farm.mouses[mid] = m
            if cid: # 能进行到这步说明 cid 已经存在
                self.farm.cages[cid].check_in(mid)
            if color not in SymList.clist:
                SymList.add(['color', color])
            for child in self.parent.GetChildren():
                if child == self:
                    self.Update(1)
                else:
                    child.Update()
            self.panel.oid.SetFocus()
        elif feedback.startswith(u'修改失败：鼠'):
            self.panel.mid.SetFocus()
        else:
            self.panel.cid.SetFocus()


if __name__ == '__main__':

    app = wx.App()
    AddNew(None, title=u'添加鼠')
    app.MainLoop()

