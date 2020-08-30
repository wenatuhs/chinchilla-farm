# -*- coding: utf-8 -*-
# Filename: addlog.py


from mousecore import *
from validator import *

import wx


class AddLogPanel(wx.Panel):

    def __init__(self, parent, flag='M'):
        wx.Panel.__init__(self, parent, -1)

        self.frame = parent

        self.sizer = vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.extra = extra = (5 if os.name == 'posix' else 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label=u'日期')
        st2 = wx.StaticText(self, label=u'种类')
        self.date = dpc = wx.DatePickerCtrl(self)
        flags = [u'移动', u'出售', u'出生', u'死亡', u'状态', u'级别', u'附注']
        self.choc = cho = wx.Choice(self, -1, choices=flags)
        self.choc.SetStringSelection(flags[0])
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.choc)
        hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(dpc, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
        hbox.Add(cho, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        vbox.Add(hbox, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10)

        box = self.GetBox(flag)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add = b_add = wx.Button(self, -1, u'添加')
        self.reset = b_reset = wx.Button(self, -1, u'重置')
        hbox.Add(b_add, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_reset, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)

    def GetBox(self, flag):
        sb = wx.StaticBox(self, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)

        if flag == 'M':
            st1 = wx.StaticText(self, label=u'鼠')
            st2 = wx.StaticText(self, label=u'从笼')
            st3 = wx.StaticText(self, label=u'移动至笼')
            self.mid = tc1 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(1))
            self.cid1 = tc2 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(2))
            self.cid2 = tc3 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(2))
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
            hbox.Add(tc1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(tc2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st3, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(tc3, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            box.Add(hbox, 0, wx.ALL, self.extra)
        elif flag == 'S':
            st1 = wx.StaticText(self, label=u'下列鼠')
            st2 = wx.StaticText(self, label=u'出售至')
            self.hint = u'鼠号间请用空格分隔，空格个数不限'
            self.mids = tc1 = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(-1, 50))
            self.mids.SetToolTipString(self.hint)
#            self.mids.SetStyle(0, 16, wx.TextAttr("GRAY"))
#            self.mids.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
#            self.mids.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            self.buyer = tc2 = wx.ComboBox(self, choices=SymList.blist, style=wx.CB_DROPDOWN)
            self.buyer.SetValue('')
            fgs = wx.FlexGridSizer(2, 2, self.extra, 5)
            fgs.AddMany([(st1, 0),
                         (tc1, 0, wx.EXPAND, 0),
                         (st2, 0),
                         (tc2, 0, wx.EXPAND, 0)])
            fgs.AddGrowableCol(1, 1)
            box.Add(fgs, 0, wx.EXPAND|wx.ALL, self.extra)
        elif flag == 'B':
            st1 = wx.StaticText(self, label=u'鼠')
            st2 = wx.StaticText(self, label=u'出生于笼')
            self.mid = tc1 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(1))
            self.cid = tc2 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(2))
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
            hbox.Add(tc1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(tc2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            box.Add(hbox, 0, wx.ALL, self.extra)
        elif flag == 'D':
            st1 = wx.StaticText(self, label=u'鼠')
            st2 = wx.StaticText(self, label=u'死亡于笼')
            self.mid = tc1 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(1))
            self.cid = tc2 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(2))
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
            hbox.Add(tc1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(tc2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            box.Add(hbox, 0, wx.ALL, self.extra)
        elif flag == 'Cs':
            st1 = wx.StaticText(self, label=u'鼠')
            st2 = wx.StaticText(self, label=u'的状态更改为')
            self.mid = tc1 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(1))
            self.status = tc2 = wx.Choice(self, -1, choices=SymList.slist[:2])
            tc2.SetStringSelection(SymList.slist[0])
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
            hbox.Add(tc1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(tc2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            box.Add(hbox, 0, wx.ALL, self.extra)
        elif flag == 'Cl':
            st1 = wx.StaticText(self, label=u'鼠')
            st2 = wx.StaticText(self, label=u'的级别更改为')
            self.mid = tc1 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(1))
            self.level = tc2 = wx.Choice(self, -1, choices=SymList.llist)
            tc2.SetStringSelection(SymList.llist[0])
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
            hbox.Add(tc1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(tc2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            box.Add(hbox, 0, wx.ALL, self.extra)
        elif flag == 'N':
            st1 = wx.StaticText(self, label=u'鼠')
            st2 = wx.StaticText(self, label=u'的附注更改为')
            self.mid = tc1 = wx.TextCtrl(self, -1, size=(80, -1), validator=MouseValidator(1))
            self.note = tc2 = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(-1, 50))
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
            hbox.Add(tc1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
            box.Add(hbox, 0, wx.ALL, self.extra)
            box.Add(tc2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, self.extra)

        line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
        box.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)

        st = wx.StaticText(self, label=u'备注')
        self.cmt = tc = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st, 0, wx.LEFT, 0)
        hbox.Add((5, -1))
        hbox.Add(tc, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        box.Add(hbox, 1, wx.EXPAND|wx.ALL, self.extra)

        return box

#    def OnSetFocus(self, evt):
#        if self.mids.GetValue() == self.hint:
#            self.mids.SetValue('')
#
#    def OnKillFocus(self, evt):
#        if self.mids.GetValue() == '':
#            self.mids.SetValue(self.hint)
#            self.mids.SetStyle(0, 16, wx.TextAttr("GRAY"))

    def OnChoice(self, evt):
        flag = self.frame.dict[evt.GetString()]
        self.sizer.Hide(2)
        self.sizer.Hide(1)
        self.sizer.Detach(2)
        self.sizer.Detach(1)
        box = self.GetBox(flag)
        if os.name == 'posix':
            self.sizer.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            self.sizer.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add = b_add = wx.Button(self, -1, u'添加')
        self.reset = b_reset = wx.Button(self, -1, u'重置')
        self.add.Bind(wx.EVT_BUTTON, self.frame.OnAdd)
        self.reset.Bind(wx.EVT_BUTTON, self.frame.OnReset)
        hbox.Add(b_add, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_reset, 0, wx.EXPAND|wx.RIGHT, 10)
        self.sizer.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)

        self.frame.Layout()
        self.frame.Unbind(wx.EVT_SIZE)
        self.frame.SetMinSize((1, 1))
        x1, y1 = self.frame.GetBestSizeTuple()
        self.frame.SetMinSize((x1, y1))
        x, y = max(self.frame.x0, x1), max(self.frame.y0, y1)
        self.frame.SetSize((x, y))
        self.frame.Bind(wx.EVT_SIZE, self.frame.OnSize)


class AddLog(wx.Frame):

    def __init__(self, parent, farm):
        wx.Frame.__init__(self, parent)

        self.dict = {u'移动': 'M',
                     u'出售': 'S',
                     u'出生': 'B',
                     u'死亡': 'D',
                     u'状态': 'Cs',
                     u'级别': 'Cl',
                     u'附注': 'N'}
        self.InitUI()
        self.parent = parent
        self.farm = farm
        self.statusbar = self.CreateStatusBar()
        self.SetTitle(u'添加日志')
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Centre()

        if self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                self.Move(p+wx.Point(335, 0))
            else:
                self.Move(p+wx.Point(20, 20))
        self.Show()

    def InitUI(self):
        self.panel = panel = AddLogPanel(self)
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.panel.add.Bind(wx.EVT_BUTTON, self.OnAdd)
        self.panel.reset.Bind(wx.EVT_BUTTON, self.OnReset)

        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose,id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        self.x0, self.y0 = self.GetSizeTuple()
        evt.Skip()

    def OnAdd(self, evt):
        date = self.panel.date.GetValue().Format('%Y-%m-%d')
        comment = self.panel.cmt.GetValue()
        flag = self.dict[self.panel.choc.GetStringSelection()]
        if flag == 'M':
            mid = self.panel.mid.GetValue()
            cid1 = self.panel.cid1.GetValue()
            cid2 = self.panel.cid2.GetValue()
            record = Record('M', [mid, cid1, cid2], date, comment)
            self.panel.mid.SetValue('')
            self.panel.cid1.SetValue('')
            self.panel.cid2.SetValue('')
            self.panel.mid.SetFocus()
        elif flag == 'S':
            mids = self.panel.mids.GetValue()
            custom = self.panel.buyer.GetValue()
            if custom not in SymList.blist:
                SymList.add(['custom', custom])
            record = Record('S', [custom]+mids.split(), date, comment)
            self.panel.mids.SetValue('')
            self.panel.buyer.SetValue('')
            self.panel.mids.SetFocus()
        elif flag == 'B':
            mid = self.panel.mid.GetValue()
            cid = self.panel.cid.GetValue()
            record = Record('B', [mid, cid], date, comment)
            self.panel.mid.SetValue('')
            self.panel.mid.SetFocus()
        elif flag == 'D':
            mid = self.panel.mid.GetValue()
            cid = self.panel.cid.GetValue()
            record = Record('D', [mid, cid], date, comment)
            self.panel.mid.SetValue('')
            self.panel.cid.SetValue('')
            self.panel.mid.SetFocus()
        elif flag == 'Cs':
            mid = self.panel.mid.GetValue()
            level = self.panel.status.GetStringSelection()
            record = Record('C', [mid, level], date, comment)
            self.panel.status.SetStringSelection(SymList.slist[0])
            self.panel.mid.SetValue('')
            self.panel.mid.SetFocus()
        elif flag == 'Cl':
            mid = self.panel.mid.GetValue()
            level = self.panel.level.GetStringSelection()
            record = Record('C', [mid, level], date, comment)
            self.panel.level.SetStringSelection(SymList.llist[0])
            self.panel.mid.SetValue('')
            self.panel.mid.SetFocus()
        elif flag == 'N':
            mid = self.panel.mid.GetValue()
            note = self.panel.note.GetValue()
            record = Record('N', [mid, note], date, comment)
            self.panel.note.SetValue('')
            self.panel.mid.SetValue('')
            self.panel.mid.SetFocus()
        self.panel.cmt.Clear()
        self.farm.insert([record])
        self.statusbar.SetStatusText(u'插入记录成功！')
        for child in self.parent.GetChildren():
            try:
                if child.GetTitle() == SymList.nlist[1]:
                    child.Update(2)
                else:
                    child.Update()
            except:
                child.Update()

    def OnReset(self, evt):
        flag = self.dict[self.panel.choc.GetStringSelection()]
        self.panel.sizer.Hide(2)
        self.panel.sizer.Hide(1)
        self.panel.sizer.Detach(2)
        self.panel.sizer.Detach(1)
        box = self.panel.GetBox(flag)
        if os.name == 'posix':
            self.panel.sizer.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            self.panel.sizer.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.add = b_add = wx.Button(self.panel, -1, u'添加')
        self.panel.reset = b_reset = wx.Button(self.panel, -1, u'重置')
        self.panel.add.Bind(wx.EVT_BUTTON, self.OnAdd)
        self.panel.reset.Bind(wx.EVT_BUTTON, self.OnReset)
        hbox.Add(b_add, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_reset, 0, wx.EXPAND|wx.RIGHT, 10)
        self.panel.sizer.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)
        self.panel.SetFocus()
        self.Layout()
        self.Unbind(wx.EVT_SIZE)
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnClose(self, evt):
        self.Destroy()

    def Update(self):
        try:
            self.panel.buyer.SetItems(SymList.blist)
        except:
            pass


if __name__ == '__main__':

    app = wx.App()
    AddLog(None)
    app.MainLoop()

