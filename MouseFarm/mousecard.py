#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

import dialog
from mousecore import SymList

class MouseCardPanel(wx.Panel):

    def __init__(self, parent, flag=0):
        wx.Panel.__init__(self, parent, -1)
        self.frame = parent
        self.mouse = self.frame.farm.mouses[self.frame.mid]        
        tc = wx.TextCtrl(self, -1, 'A')
        font = tc.GetFont()
        tc.Hide()
        self.afont = font
        tc = wx.TextCtrl(self, -1, 'A')
        font = tc.GetFont()
        tc.Hide()
        font.SetPointSize(7)
        self.cfont = font
        self.pics = self.getPics()
        color = 'STEEL BLUE'
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        if flag == 0:
            self.move = btn_move = wx.Button(self, -1, label=u'移动')
            self.status = btn_status = wx.Button(self, -1, label=u'状态')
            self.level = btn_level = wx.Button(self, -1, label=u'级别')
            self.note = btn_note = wx.Button(self, -1, label=u'附注')
            self.die = btn_die = wx.Button(self, -1, label=u'死亡')
            # OnAction() flag 1: 状态, 2: 级别, 3: 移动, 4: 死亡
            self.move.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 3))
            self.status.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 1))
            self.level.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 2))
            self.note.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 5))
            self.die.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 4))
        elif flag == -1 or flag == -2:
            pass
        elif flag == 4:
            self.done = btn_done = wx.Button(self, -1, label=u'确认死亡')
            self.cancel = btn_cancel = wx.Button(self, -1, label=u'取消')
            self.done.Bind(wx.EVT_BUTTON, self.frame.OnDone)
            self.cancel.Bind(wx.EVT_BUTTON, self.frame.OnCancel)
        else:
            self.done = btn_done = wx.Button(self, -1, label=u'完成')
            self.cancel = btn_cancel = wx.Button(self, -1, label=u'取消')
            self.done.Bind(wx.EVT_BUTTON, self.frame.OnDone)
            self.cancel.Bind(wx.EVT_BUTTON, self.frame.OnCancel)

        # 基本信息栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        picbox = wx.StaticBox(self, label='', size=(75, 75))
        hbox1.Add(picbox, 0, wx.LEFT, 0)
        hbox1.Add((10, -1))
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        st_mid = wx.StaticText(self, -1, u'鼠号')
        vbox1.Add(st_mid, 0, wx.TOP, 0)
        st_cid = wx.StaticText(self, -1, u'笼号')
        vbox1.Add(st_cid, 0, wx.TOP, 10)
        st_age = wx.StaticText(self, -1, u'年龄')
        vbox1.Add(st_age, 0, wx.TOP, 10)
        st_born = wx.StaticText(self, -1, u'出生日期')
        vbox1.Add(st_born, 0, wx.TOP, 10)
        if flag == -2 or flag == 4:
            st_dead = wx.StaticText(self, -1, u'死亡日期')
            vbox1.Add(st_dead, 0, wx.TOP, 10)
        hbox1.Add(vbox1, 0, wx.EXPAND, 0)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        st_mid2 = wx.StaticText(self, -1, self.mouse.id)
        st_mid2.SetForegroundColour(color)
        vbox2.Add(st_mid2, 0, wx.TOP, 0)
        if flag == 3:
            st_cid2 = wx.TextCtrl(self, -1, (self.mouse.cage or ''))
            self.cid = st_cid2
        else:
            st_cid2 = wx.StaticText(self, -1, (self.mouse.cage or ''))
            st_cid2.SetForegroundColour(color)
        vbox2.Add(st_cid2, 0, wx.TOP, 10)
        st_age2 = wx.StaticText(self, -1, "{:.1f}".format(self.mouse.age()/30.0)+u'月')
        st_age2.SetForegroundColour(color)
        vbox2.Add(st_age2, 0, wx.TOP, 10)
        st_born2 = wx.StaticText(self, -1, self.mouse.borndate)
        st_born2.SetForegroundColour(color)
        vbox2.Add(st_born2, 0, wx.TOP, 10)
        if flag == -2:
            st_dead2 = wx.StaticText(self, -1, (self.mouse.deathdate or ''))
            st_dead2.SetForegroundColour(color)
            vbox2.Add(st_dead2, 0, wx.TOP, 10)
        elif flag == 4:
            self.dpc = st_dead2 = wx.DatePickerCtrl(self)
            vbox2.Add(st_dead2, 0, wx.TOP, 5)
        hbox1.Add(vbox2, 0, wx.EXPAND|wx.LEFT, 10)
        vbox.Add(hbox1, 0, wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND, 25)

        vbox.Add((-1, 10))
        line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
        vbox.Add((-1, 10))
        # 进一步信息
        st_gender = wx.StaticText(self, -1, u'性别')
        st_gender2 = wx.StaticText(self, -1, self.mouse.gender)
        st_gender2.SetForegroundColour(color)
        st_level = wx.StaticText(self, -1, u'级别')
        if flag == 2:
            st_level2 = wx.Choice(self, -1, choices=SymList.llist)
            st_level2.SetStringSelection(self.mouse.level)
            self.level = st_level2
        else:
            st_level2 = wx.StaticText(self, -1, self.mouse.level)
            st_level2.SetForegroundColour(color)
        st_color = wx.StaticText(self, -1, u'毛色')
        st_color2 = wx.StaticText(self, -1, self.mouse.color)
        st_color2.SetForegroundColour(color)
        st_status = wx.StaticText(self, -1, u'状态')
        if flag == 1:
            st_status2 = wx.Choice(self, -1, choices=[u'正常', u'生病'])
            st_status2.SetStringSelection(self.mouse.status)
            self.status = st_status2
        else:
            st_status2 = wx.StaticText(self, -1, self.mouse.status)
            st_status2.SetForegroundColour(color)
        st_cmt = wx.StaticText(self, -1, u'附注')
        if flag == 5:
            st_cmt2 = wx.TextCtrl(self, -1, (self.mouse.comment or ''))
            self.comment = st_cmt2
        else:
            st_cmt2 = wx.StaticText(self, -1, (self.mouse.comment or ''))
            st_cmt2.SetForegroundColour(color)
        st_fa = wx.StaticText(self, -1, u'父亲')
        try:
            m = self.frame.farm.mouses[self.mouse.father]
            pb_fa = platebtn.PlateButton(self, -1, self.mouse.father)
            pb_fa.SetFont(self.afont)
            if m.status == u'正常':
                pb_fa.SetBitmap(self.pics['man'])
            elif m.status == u'生病':
                pb_fa.SetBitmap(self.pics['mansick'])
            elif m.status == u'死亡':
                pb_fa.SetBitmap(self.pics['mandead'])
            else:
                pb_fa.SetBitmap(self.pics['mansold'])
            pb_fa.SetToolTipString(u"毛色："+m.color+u"\n级别："+m.level+\
                                   u"\n年龄："+"{:.1f}".format(m.age()/30.0)+\
                                   u"月\n附注："+(m.comment or ''))
            pb_fa.Bind(wx.EVT_BUTTON, self.frame.OnMouseCard)
        except:
            pb_fa = wx.StaticText(self, -1, self.mouse.father)
        pb_fa.SetForegroundColour(color)
        st_mo = wx.StaticText(self, -1, u'母亲')
        try:
            m = self.frame.farm.mouses[self.mouse.mother]
            pb_mo = platebtn.PlateButton(self, -1, self.mouse.mother)
            pb_mo.SetFont(self.afont)
            if m.status == u'正常':
                pb_mo.SetBitmap(self.pics['woman'])
            elif m.status == u'生病':
                pb_mo.SetBitmap(self.pics['womansick'])
            elif m.status == u'死亡':
                pb_mo.SetBitmap(self.pics['womandead'])
            else:
                pb_mo.SetBitmap(self.pics['womansold'])
            pb_mo.SetToolTipString(u"毛色："+m.color+u"\n级别："+m.level+\
                                   u"\n年龄："+"{:.1f}".format(m.age()/30.0)+\
                                   u"月\n附注："+(m.comment or ''))
            pb_mo.Bind(wx.EVT_BUTTON, self.frame.OnMouseCard)
        except:
            pb_mo = wx.StaticText(self, -1, self.mouse.mother)
        pb_mo.SetForegroundColour(color)

        fgs = wx.FlexGridSizer(4, 4, 10, 10)
        fgs.AddMany([(st_gender, 0),
                     (st_gender2, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND),
                     (st_color, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_color2, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND),
                     (st_level, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_level2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_status, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_status2, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_fa, 0, wx.ALIGN_CENTER_VERTICAL),
                     (pb_fa, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_mo, 0, wx.ALIGN_CENTER_VERTICAL),
                     (pb_mo, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_cmt, 0, wx.ALIGN_CENTER_VERTICAL),
                     (st_cmt2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)])
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(3, 1)
        vbox.Add(fgs, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 25)

        # 按钮分布及编辑界面的日期和备注
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        if flag == 0:
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))
            
            hbox2.Add(self.move, 0, wx.LEFT|wx.RIGHT, 10)
            hbox2.Add(self.level, 0, wx.RIGHT, 10)
            hbox2.Add(self.status, 0, wx.RIGHT, 10)
            hbox2.Add(self.note, 0, wx.RIGHT, 10)
            hbox2.Add(self.die, 0, wx.RIGHT, 10)
        elif flag == -1 or flag == -2:
            pass
        elif flag == 4:
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))   
                 
            hbox2.Add(self.done, 0, wx.RIGHT, 10)
            hbox2.Add(self.cancel, 0, wx.RIGHT, 10)
            fgs = wx.FlexGridSizer(1, 2, 5, 10)
            st2 = wx.StaticText(self, label=u'备注')            
            self.cmt = tc = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
            fgs.AddMany([(st2, 0),
                         (tc, 1, wx.EXPAND)])
            fgs.AddGrowableCol(1, 1)
            fgs.AddGrowableRow(0, 1)
            vbox.Add(fgs, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 25)
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))
        else:
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))
                    
            hbox2.Add(self.done, 0, wx.RIGHT, 10)
            hbox2.Add(self.cancel, 0, wx.RIGHT, 10)
            fgs = wx.FlexGridSizer(2, 2, 5, 10)
            st1 = wx.StaticText(self, label=u'日期')
            st2 = wx.StaticText(self, label=u'备注')
            self.dpc = dpc = wx.DatePickerCtrl(self)
            self.cmt = tc = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
            fgs.AddMany([(st1, 0, wx.ALIGN_CENTER_VERTICAL),
                         (dpc, 0, wx.ALIGN_CENTER_VERTICAL),
                         (st2, 0),
                         (tc, 1, wx.EXPAND)])
            fgs.AddGrowableCol(1, 1)
            fgs.AddGrowableRow(1, 1)
            vbox.Add(fgs, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 25)
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))
        vbox.Add(hbox2, 0, wx.ALIGN_RIGHT|wx.RIGHT, 0)
        # 现有鼠鼠卡的笼子信息
        if not (flag == -1 or flag == -2):
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))

            gs = wx.GridSizer(1, 5, 10, 5)
            cid = self.mouse.cage
            cage = self.frame.farm.cages[cid]
            if cage.house != '1':
                num = int(cid.split('-')[1])
                pre = cage.house + '-'
            else:
                num = int(cid)
                pre = ''
            n0 = num - ((num - 1) % 5)
            pics = self.getPics()
            for i in range(5):
                pbs = []
                sts = []
                cid = pre + str(n0+i)
                cage = self.frame.farm.cages[cid]
                c = wx.StaticBox(self, label=cid)
                box = wx.StaticBoxSizer(c, wx.VERTICAL)
                for mid in cage.guest:
                    try:
                        m = self.frame.farm.mouses[mid]
                        pb = platebtn.PlateButton(self, -1, mid)
                        if m.age() < 90:
                            pb.SetFont(self.cfont)
                            if m.gender == u'公':
                                if m.status == u'正常':
                                    pb.SetBitmap(self.pics['boy'])
                                elif m.status == u'生病':
                                    pb.SetBitmap(self.pics['boysick'])
                            else:
                                if m.status == u'正常':
                                    pb.SetBitmap(self.pics['girl'])
                                elif m.status == u'生病':
                                    pb.SetBitmap(self.pics['girlsick'])
                        else:
                            pb.SetFont(self.afont)
                            if m.gender == u'公':
                                if m.status == u'正常':
                                    pb.SetBitmap(self.pics['man'])
                                elif m.status == u'生病':
                                    pb.SetBitmap(self.pics['mansick'])
                            else:
                                if m.status == u'正常':
                                    pb.SetBitmap(self.pics['woman'])
                                elif m.status == u'生病':
                                    pb.SetBitmap(self.pics['womansick'])
                        pb.Bind(wx.EVT_BUTTON, self.frame.OnMouseCard)
                        menu = wx.Menu()
                        menu.Append(wx.NewId(), u'移动')
                        menu.Append(wx.NewId(), u'状态')
                        menu.Append(wx.NewId(), u'级别')
                        menu.Append(wx.NewId(), u'死亡')
                        menu.SetTitle(mid)
                        pb.SetMenu(menu)
                        if mid == self.frame.mid:
                            pb.SetForegroundColour(color)
                        pb.SetToolTipString(u"毛色："+m.color+u"\n级别："+m.level+\
                                            u"\n年龄："+"{:.1f}".format(m.age()/30.0)+\
                                            u" 月\n附注："+(m.comment or ''))
                        pbs.append(pb)
                    except:
                        pb = wx.StaticText(self, -1, mid)
                        sts.append(pb)
                pbs = sorted(pbs, key=lambda pb: self.frame.farm.mouses[pb.GetLabel()].age(), \
                             reverse=True)
                total = pbs + sts
                for pb in total:
                    box.Add(pb, 0, wx.ALIGN_LEFT|wx.BOTTOM, 1)
                gs.Add(box, 1, wx.EXPAND)
            vbox.Add(gs, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        vbox.Add((-1, 10))
        
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), self.frame.exitID)])
        self.SetAcceleratorTable(accel_tbl)

        self.Bind(wx.EVT_MENU, self.frame.OnMenu)

    def getPics(self):
        pics = {}

        male = wx.Image("boy.png")
        male.Rescale(14, 14)
        pics['man'] = wx.BitmapFromImage(male)
        male.Rescale(10, 10)
        pics['boy'] = wx.BitmapFromImage(male)
        female = wx.Image("girl.png")
        female.Rescale(14, 14)
        pics['woman'] = wx.BitmapFromImage(female)
        female.Rescale(10, 10)
        pics['girl'] = wx.BitmapFromImage(female)

        male = wx.Image("boysick.png")
        male.Rescale(14, 14)
        pics['mansick'] = wx.BitmapFromImage(male)
        male.Rescale(10, 10)
        pics['boysick'] = wx.BitmapFromImage(male)
        female = wx.Image("girlsick.png")
        female.Rescale(14, 14)
        pics['womansick'] = wx.BitmapFromImage(female)
        female.Rescale(10, 10)
        pics['girlsick'] = wx.BitmapFromImage(female)

        male = wx.Image("boydead.png")
        male.Rescale(14, 14)
        pics['mandead'] = wx.BitmapFromImage(male)
        male.Rescale(10, 10)
        pics['boydead'] = wx.BitmapFromImage(male)
        female = wx.Image("girldead.png")
        female.Rescale(14, 14)
        pics['womandead'] = wx.BitmapFromImage(female)
        female.Rescale(10, 10)
        pics['girldead'] = wx.BitmapFromImage(female)

        male = wx.Image("boysold.png")
        male.Rescale(14, 14)
        pics['mansold'] = wx.BitmapFromImage(male)
        male.Rescale(10, 10)
        pics['boysold'] = wx.BitmapFromImage(male)
        female = wx.Image("girlsold.png")
        female.Rescale(14, 14)
        pics['womansold'] = wx.BitmapFromImage(female)
        female.Rescale(10, 10)
        pics['girlsold'] = wx.BitmapFromImage(female)
        return pics


class MouseCard(wx.Frame):

    def __init__(self, parent, mid, farm, pos=None):
        wx.Frame.__init__(self, parent, title=u'鼠卡 '+mid)
        
        self.parent = parent
        self.farm = farm
        self.mid = mid
        self.exitID = wx.NewId()
        self.statusbar = self.CreateStatusBar()
        self.InitUI()
        self.Fit()
        self.Center()

        if pos:
            self.Move(pos)
        elif self.parent:
            p = self.GetPosition()
            if self.parent.GetTitle() == SymList.nlist[0]:
                self.Move(p+wx.Point(200, 0))
            else:
                self.Move(p+wx.Point(20, 20))
        self.Show()

    def InitUI(self):
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        status = self.farm.mouses[self.mid].status
        if status == u'死亡':
            self.panel = MouseCardPanel(self, -2)
        elif status == u'已售':
            self.panel = MouseCardPanel(self, -1)
        else:
            self.panel = MouseCardPanel(self, 0)
        self.sizer.Add(self.panel, 1, wx.EXPAND)

    def Update(self):
        try:
            self.sizer.Hide(0)
            self.sizer.Remove(0)
            self.InitUI()
            self.Layout()
            self.Fit()
        except:
            self.Destroy() # 解决穿越导致的鼠卡为还不存在鼠的矛盾

    def OnMenu(self, evt):
        e_obj = evt.GetEventObject()
        if evt.GetId() == self.exitID:
            self.Destroy()
        else:
            mitem = e_obj.FindItemById(evt.GetId())
            if mitem != wx.NOT_FOUND:
                action = mitem.GetItemLabel()
                mid = e_obj.GetTitle()
                if action == u'移动':
                    mouse = self.farm.mouses[mid]
                    md = dialog.SimpleMoveDialog(self, mouse)
                    md.ShowModal()
                    if md.move:
                        feedback = self.farm.move(mid, md.cid)
                        for child in self.parent.GetChildren():
                            child.Update()
                        self.statusbar.SetStatusText(feedback)
                    md.Destroy()
                elif action == u'状态':
                    if self.farm.mouses[mid].status == u'生病':
                        feedback = self.farm.change(mid, u'正常')
                    else:
                        feedback = self.farm.change(mid, u'生病')
                    self.statusbar.SetStatusText(feedback)
                    for child in self.parent.GetChildren():
                        child.Update()
                elif action == u'级别':
                    mouse = self.farm.mouses[mid]
                    sd = dialog.SimpleLevelDialog(self, mouse)
                    sd.ShowModal()
                    if sd.change:
                        feedback = self.farm.change(mid, sd.level)
                        for child in self.parent.GetChildren():
                            child.Update()
                        self.statusbar.SetStatusText(feedback)
                    sd.Destroy()
                elif action == u'死亡':
                    feedback = self.farm.burn(mid)
                    self.statusbar.SetStatusText(feedback)
                    for child in self.parent.GetChildren():
                        child.Update()

    def OnAction(self, event, flag):
        self.sizer.Hide(0)
        self.sizer.Remove(0)
        self.panel = MouseCardPanel(self, flag)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.Layout()
        self.Fit()

    def OnDone(self, event):
        date = self.panel.dpc.GetValue().Format('%Y-%m-%d')
        comment = self.panel.cmt.GetValue()
        try:
            cid = self.panel.cid.GetValue()
            feedback = self.farm.move(self.mid, cid, date, comment)
        except:
            try:
                prop = self.panel.status.GetStringSelection()
                feedback = self.farm.change(self.mid, prop, date, comment)
            except:
                try:
                    prop = self.panel.level.GetStringSelection()
                    feedback = self.farm.change(self.mid, prop, date, comment)
                except:                    
                    try:
                        prop = self.panel.comment.GetValue()
                        feedback = self.farm.comment(self.mid, prop, date, comment)
                    except:
                        feedback = self.farm.burn(self.mid, date, comment)
        for child in self.parent.GetChildren():
            child.Update()
            if child == self:
                self.statusbar.SetStatusText(feedback)

    def OnCancel(self, event):
        self.Update()

    def OnMouseCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        MouseCard(self.parent, pb.GetLabel(), self.farm, pos=pos)


if __name__ == '__main__':

    app = wx.App()
    from mousecore import *
    f = Farm()
    MouseCard(None, 'AX1', f)
    app.MainLoop()

