# -*- coding: utf-8 -*-
# Filename: mouselist.py


from mousecore import *
import dialog
import mousecard
import json

import math
import wx
import wx.dataview as dv


class InfoModel(dv.PyDataViewIndexListModel):

    def __init__(self, data):
        dv.PyDataViewIndexListModel.__init__(self, len(data))
        self.data = data
        self.id = None

    def GetColumnType(self, col):
        if col:
            return "string"
        else:
            return "bool"

    def GetValueByRow(self, row, col):
        try:
            return self.data[row][col]
        except:
            pass

    def SetValueByRow(self, value, row, col):
        self.data[row][col] = value
        if not col:
            self.id = self.GetValueByRow(row, col+1)

    def GetColumnCount(self):
        if not self.data:
            return 11
        else:
            return len(self.data[0])

    def GetCount(self):
        return len(self.data)

    def GetAttrByRow(self, row, col, attr):
        if col == 1:
#            attr.SetColour('STEEL BLUE')
            attr.SetBold(True)
            return True
        return False

    def Compare(self, item1, item2, col, ascending):
        if not ascending:
            item2, item1 = item1, item2
        try:
            row1 = self.GetRow(item1)
            row2 = self.GetRow(item2)
            if col == 1:
                id1 = self.data[row1][col]
                id2 = self.data[row2][col]
                if cmp(id1[:2], id2[:2]):
                    return cmp(id1[:2], id2[:2])
                else:
                    return cmp(int(id1[2:]), int(id2[2:]))
            else:
                return cmp(self.data[row1][col], self.data[row2][col])
        except:
            return 0

    def DeleteRows(self, rows):
        rows = list(rows)
        rows.sort(reverse=True)

        for row in rows:
            del self.data[row]
            self.RowDeleted(row)

    def DeleteAll(self):
        for i in range(len(self.data)):
            del self.data[0]
            self.RowDeleted(0)

    def AddRow(self, value):
        self.data.append(value)
        self.RowAppended()


class MouseListPanel(wx.Panel):
    def __init__(self, parent, model=None):
        wx.Panel.__init__(self, parent)
        self.frame = parent
        self.mids = []
        self.conditions = []
        self.mouses = self.frame.farm.mouses
        self.extra = extra = (0 if os.name == 'posix' else 5)

        if model is None:
            self.model = InfoModel(self.getMouseData())
        else:
            self.model = model
        self.sizer = sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        vbox = wx.BoxSizer(wx.VERTICAL)
        sb = wx.StaticBox(self, label=u'操作')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.all = btn_all = wx.Button(self, -1, u"全选")
        self.cancel = btn_cancel = wx.Button(self, -1, u"取消选择")
        self.sell = btn_sell = wx.Button(self, -1, u"出售")
        self.detail = btn_detail = wx.Button(self, -1, u"详细")
        self.sell.Disable()
        self.detail.Disable()
        gs = wx.GridSizer(2, 2, 5, 5)
        gs.AddMany([(btn_all, 1, wx.EXPAND),
                    (btn_cancel, 1, wx.EXPAND),
                    (btn_sell, 1, wx.EXPAND),
                    (btn_detail, 1, wx.EXPAND)])
        box.Add(gs, 0, wx.EXPAND|wx.ALL, extra)

        self.all.Bind(wx.EVT_BUTTON, self.OnAll)
        self.cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.sell.Bind(wx.EVT_BUTTON, self.OnSell)
        self.detail.Bind(wx.EVT_BUTTON, self.OnDetail)

        vbox.Add(box, 0, wx.EXPAND|wx.ALL, 0)
        vbox.Add((-1, 10))

        sb2 = wx.StaticBox(self, label=u'过滤')
        box2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)
        self.app = btn_apply = wx.Button(self, label=u"应用")
        self.reset = btn_reset = wx.Button(self, label=u"重置")
        gs = wx.GridSizer(1, 2, 5, 5)
        gs.AddMany([(btn_apply, 1, wx.EXPAND),
                    (btn_reset, 1, wx.EXPAND)])
        box2.Add(gs, 0, wx.EXPAND|wx.ALL, extra)

        self.app.Bind(wx.EVT_BUTTON, self.OnApply)
        self.reset.Bind(wx.EVT_BUTTON, self.OnReset)

        box2.Add((-1, 10))

        box_gen, self.gen = self.genCheckBoxGroup(u'性别', SymList.glist, 2)
        box_col, self.col = self.genCheckBoxGroup(u'毛色', SymList.clist, 2)
        box_lev, self.lev = self.genCheckBoxGroup(u'级别', SymList.llist, 2)
        box_sta, self.sta = self.genCheckBoxGroup(u'状态', SymList.slist, 2)
        box_age, self.age = self.genRangeGroup(u'年龄')

        self.gen[0].Bind(wx.EVT_CHECKBOX, lambda evt: self.OnCheck(evt, 'gen'))
        self.col[0].Bind(wx.EVT_CHECKBOX, lambda evt: self.OnCheck(evt, 'col'))
        self.lev[0].Bind(wx.EVT_CHECKBOX, lambda evt: self.OnCheck(evt, 'lev'))
        self.sta[0].Bind(wx.EVT_CHECKBOX, lambda evt: self.OnCheck(evt, 'sta'))
        self.age[0].Bind(wx.EVT_CHECKBOX, lambda evt: self.OnCheck(evt, 'age'))

        box2.Add(box_gen, 0, wx.EXPAND|wx.ALL, extra)
        box2.Add((-1, 5))
        box2.Add(box_col, 0, wx.EXPAND|wx.ALL, extra)
        box2.Add((-1, 5))
        box2.Add(box_lev, 0, wx.EXPAND|wx.ALL, extra)
        box2.Add((-1, 5))
        box2.Add(box_sta, 0, wx.EXPAND|wx.ALL, extra)
        box2.Add((-1, 5))
        box2.Add(box_age, 0, wx.EXPAND|wx.ALL, extra)

        vbox.Add(box2, 0, wx.EXPAND|wx.ALL, 0)
        sizer.Add(vbox, 0, wx.EXPAND|wx.ALL, 10)

        box_dvc, self.dvc = self.genDVCGroup(u'信息')
        self.dvc.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged)
        sizer.Add(box_dvc, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 10)
        if self.model.data[0][1] == '':
            self.model.DeleteAll()
            self.model.Cleared()
        self.sizer.Layout()
        self.frame.Fit()

    def getDVC(self):
        dvc = dv.DataViewCtrl(self, size=(877, -1),
                                   style=wx.BORDER_THEME
                                   | dv.DV_VERT_RULES
                                   | dv.DV_ROW_LINES
                                   | dv.DV_MULTIPLE)
        dvc.AssociateModel(self.model)
        c1 = dvc.AppendTextColumn(u'鼠号', 1, width=80)
        dvc.AppendTextColumn(u'笼号', 2, width=60)
        dvc.AppendTextColumn(u'性别', 3, width=40)
        dvc.AppendTextColumn(u'年龄', 4, width=60)
        dvc.AppendTextColumn(u'毛色', 5, width=60)
        dvc.AppendTextColumn(u'级别', 6, width=60)
        dvc.AppendTextColumn(u'状态', 7, width=60)
        dvc.AppendTextColumn(u'出生日期', 8, width=90)
        dvc.AppendTextColumn(u'死亡日期', 9, width=90)
        dvc.AppendTextColumn(u'附注', 10, width=200)
        c0 = dvc.PrependToggleColumn(u'选择', 0, width=40, align=wx.ALIGN_CENTER, \
                                     mode=dv.DATAVIEW_CELL_ACTIVATABLE)
                                     #mode=dv.DATAVIEW_CELL_EDITABLE)
        for c in dvc.Columns:
            c.Sortable = True
            c.Reorderable = True
        c0.MinWidth = 40
        c0.Reorderable = False
        c1.Reorderable = False
        return dvc

    def genCheckBoxGroup(self, label, choices, extra=0):
        sb = wx.StaticBox(self, label=label)
        box = wx.StaticBoxSizer(sb)
        ck0 = wx.CheckBox(self, -1, u"不限")
        checkboxes = [ck0]
        for choice in choices:
            checkboxes.append(wx.CheckBox(self, -1, choice))
            checkboxes[-1].Disable()
        ck0.SetValue(True)
        n = math.ceil((len(checkboxes)+extra)/3.0)
        gs = wx.GridSizer(n, 3, 5, 5)
        gs.Add(ck0, 0)
        for i in range(extra):
            gs.Add(wx.StaticText(self), 0)
        for ck in checkboxes[1:]:
            gs.Add(ck, 1, wx.EXPAND)
        box.Add(gs, 1, wx.EXPAND|wx.ALL, self.extra)
        return box, checkboxes

    def genRangeGroup(self, label):
        sb = wx.StaticBox(self, label=label)
        box = wx.StaticBoxSizer(sb)
        ck0 = wx.CheckBox(self, -1, u"不限")
        st1 = wx.StaticText(self, -1, u'从（月数）')
        st2 = wx.StaticText(self, -1, u'至（月数）')
        tc1 = wx.TextCtrl(self, -1, size=(70, -1))
        tc2 = wx.TextCtrl(self, -1, size=(70, -1))
        tc1.Disable()
        tc2.Disable()
        ranges = [ck0, tc1, tc2]
        ck0.SetValue(True)
        gs = wx.FlexGridSizer(3, 2, 5, 5)
        gs.AddMany([(ck0, 0),
                    (wx.StaticText(self), 0),
                    (st1, 0),
                    (tc1, 1, wx.EXPAND),
                    (st2, 0),
                    (tc2, 1, wx.EXPAND)])
        gs.AddGrowableCol(1, 1)
        box.Add(gs, 1, wx.EXPAND|wx.ALL, self.extra)
        return box, ranges

    def genDVCGroup(self, label):
        sb = wx.StaticBox(self, label=label)
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        dvc = self.getDVC()
        box.Add(dvc, 1, wx.EXPAND|wx.ALL, self.extra)
        return box, dvc

    def OnValueChanged(self, evt):
        if not evt.GetColumn():
            if self.model.id in self.mids:
                self.mids.remove(self.model.id)
            else:
                self.mids.append(self.model.id)
        self.frame.Update()         

    def OnCheck(self, evt, flag):
        if flag == 'gen':
            ckl = self.gen[1:]
        elif flag == 'col':
            ckl = self.col[1:]
        elif flag == 'sta':
            ckl = self.sta[1:]
        elif flag == 'lev':
            ckl = self.lev[1:]
        elif flag == 'age':
            ckl = self.age[1:]
        if evt.IsChecked():
            for ck in ckl:
                ck.Disable()
        else:
            for ck in ckl:
                ck.Enable()

    def filtrate(self, mouseitem):
        return (mouseitem[1].gender in self.conditions[0]) and \
               (mouseitem[1].color in self.conditions[1]) and \
               (mouseitem[1].status in self.conditions[2]) and \
               (mouseitem[1].level in self.conditions[3]) and \
               (self.conditions[4][0] <= mouseitem[1].age()/30.0 <= self.conditions[4][1])

    def getCheckState(self, key):
        return (key in self.mids)

    def getMouseData(self):
        if self.conditions:
            self.mouses = dict(filter(self.filtrate, self.frame.farm.mouses.items()))
        else:
            self.mouses = self.frame.farm.mouses
        self.mids = [mid for mid in self.mids if (mid in self.mouses.keys())]
        mouselist = self.mouses.items()
        mouselist.sort(key=lambda e: (e[0][0:2], int(e[0][2:])))
        mousedata = [[self.getCheckState(k), k, (v.cage or ''), v.gender, \
                      "{:.1f}".format(v.age()/30.0), v.color, v.level, v.status, \
                      v.borndate, (v.deathdate or ''), (v.comment or '')] for k,v in mouselist]
        if mousedata:
            return mousedata
        else:
            return [[False, '', '', '', '', '', '', '', '', '', '']]

    def checkValid(self, gen, col, sta, lev, age):
        report = []
        if not gen:
            report.append(u'请选择性别！')
        if not col:
            report.append(u'请选择毛色！')
        if not sta:
            report.append(u'请选择状态！')
        if not lev:
            report.append(u'请选择级别！')
        try:
            if not age[0]:
                age[0] = -1e9
            else:
                age[0] = float(age[0])
            if not age[1]:
                age[1] = 1e9
            else:
                age[1] = float(age[1])
            if age[0] > age[1]:
                report.append(u'年龄范围请从小到大填写！')
        except:
            report.append(u'年龄范围请填写数字！')
        if report:
            return report
        else:
            return 1

    def OnApply(self, evt):
        if self.gen[0].IsChecked():
            gen = SymList.glist
        else:
            gen = [ck.GetLabel() for ck in self.gen[1:] if ck.IsChecked()]
        if self.col[0].IsChecked():
            col = SymList.clist
        else:
            col = [ck.GetLabel() for ck in self.col[1:] if ck.IsChecked()]
        if self.sta[0].IsChecked():
            sta = SymList.slist
        else:
            sta = [ck.GetLabel() for ck in self.sta[1:] if ck.IsChecked()]
        if self.lev[0].IsChecked():
            lev = SymList.llist
        else:
            lev = [ck.GetLabel() for ck in self.lev[1:] if ck.IsChecked()]
        if self.age[0].IsChecked():
            age = ['', '']
        else:
            age = [tc.GetValue() for tc in self.age[1:]]
        feedback = self.checkValid(gen, col, sta, lev, age)
        if feedback == 1:
            self.conditions = [gen, col, sta, lev, age]
            self.frame.Update(1)
        else:
            self.frame.statusbar.SetStatusText(' '.join(feedback))

    def OnReset(self, evt):
        cks = self.gen[1:]+self.col[1:]+self.sta[1:]+self.lev[1:]
        for ck in cks:
            ck.SetValue(False)
            ck.Disable()
        for tc in self.age[1:]:
            tc.SetValue('')
            tc.Disable()
        ck0s = [self.gen[0], self.col[0], self.sta[0], self.lev[0], self.age[0]]
        for ck in ck0s:
            ck.SetValue(True)
        self.conditions = []
        self.frame.Update()

    def OnAll(self, evt):
        self.mids = self.mouses.keys()
        self.frame.Update()

    def OnCancel(self, evt):
        self.mids = []
        self.frame.Update()

    def OnSell(self, evt):
        sd = dialog.SellDialog(self.frame, self.mids, self.frame.farm)
        sd.ShowModal()        
        if sd.sold:
            feedback = self.frame.farm.sell(self.mids, sd.buyer, sd.date, sd.comment)
            if sd.buyer not in SymList.blist:
                SymList.add(['custom', sd.buyer])
            for child in self.frame.parent.GetChildren():
                child.Update()
            self.frame.statusbar.SetStatusText(self.summary(feedback))
        sd.Destroy()
        
    def OnDetail(self, evt):
        pos = self.GetPosition() + wx.Point(200, 200)
        for mid in self.mids:
            pos += wx.Point(20, 20)
            mousecard.MouseCard(self.frame.parent, mid, self.frame.farm, pos=pos)        

    def summary(self, feedback):
        fails = []
        for fb in feedback:
            if not fb.startswith(u'成功'):
                fails.append(fb)
        if fails:
            return ' '.join(fails)
        else:
            return u'出售成功！'
            

class MouseList(wx.Frame):

    def __init__(self, parent, farm):
        wx.Frame.__init__(self, parent)

        self.statusbar = self.CreateStatusBar()
        self.parent = parent
        self.farm = farm
        self.InitUI()
        self.Fit()
        self.SetTitle(u'鼠列表')
        self.Center()
        try:
            self.Show()
        except:
            pass

    def InitUI(self):
        self.panel = MouseListPanel(self)
        self.statusbar.SetStatusText(u'共有 %d 项符合条件' % len(self.panel.mouses.keys()))

        sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose,id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)

    def Update(self, flag=0):
        # very dirty code but works
        old = self.panel.model.GetCount()
        data = self.panel.getMouseData()
        new = len(data)
        if new > old:
            for i in range(new-old):
                self.panel.model.AddRow([False, '', '', '', '', '', '', '', '', '', ''])
        elif new < old:
            self.panel.model.DeleteAll()
            for i in range(new):
                self.panel.model.AddRow([False, '', '', '', '', '', '', '', '', '', ''])
        # the real part
        self.panel.model.data = data
        if not new:
            self.panel.model.Cleared()
        if self.panel.mids:
            self.panel.detail.SetLabel(u'详细 ('+unicode(len(self.panel.mids))+u'项)')
            self.panel.sell.SetLabel(u'出售 ('+unicode(len(self.panel.mids))+u'项)')
            self.panel.detail.Enable()
            self.panel.sell.Enable()
        else:
            self.panel.detail.SetLabel(u'详细')
            self.panel.sell.SetLabel(u'出售')
            self.panel.detail.Disable()
            self.panel.sell.Disable()
        if flag == 1:
            self.statusbar.SetStatusText(u'过滤成功！共有 %d 项符合条件' % len(self.panel.mouses.keys()))
        else:
            self.statusbar.SetStatusText(u'共有 %d 项符合条件' % len(self.panel.mouses.keys()))
        self.panel.sizer.Layout()
        self.panel.Refresh()
        self.Fit()

    def OnClose(self, evt):
        try:
            self.Destroy()
        except:
            pass


if __name__ == '__main__':

    f = Farm()
    m = f.mouses

    app = wx.App()
    MouseList(None, title=u'鼠列表', mouses=m)
    app.MainLoop()

