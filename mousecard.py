#!/usr/bin/python
# -*- coding: utf-8 -*-


import math
import wx
import  wx.lib.scrolledpanel as scrolled
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

import dialog
from mousecore import *
from validator import *
import cagecard
import addnew
import familytree


class InfoPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, info):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(150, 80))
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        color = 'STEEL BLUE'
        info = wx.StaticText(self, -1, info)
        info.SetForegroundColour(color)
        vbox.Add(info, 1, wx.EXPAND, 0)
        self.SetupScrolling(scroll_x=False)


class MouseCardPanel(wx.Panel):

    def __init__(self, parent, flag=0):
        wx.Panel.__init__(self, parent, -1)
        self.frame = parent
        self.mouse = self.frame.farm.mouses[self.frame.mid]
        self.delta = 2 if (os.name == 'posix') else 1
        tc = wx.TextCtrl(self, -1, 'A')
        font = tc.GetFont()        
        tc.Hide()
        size = font.GetPointSize()
        self.afont = font
        tc = wx.TextCtrl(self, -1, 'A')
        font = tc.GetFont()
        tc.Hide()
        font.SetPointSize(size - self.delta)
        self.yfont = font
        tc = wx.TextCtrl(self, -1, 'A')
        font = tc.GetFont()
        tc.Hide()        
        font.SetPointSize(size - 2*self.delta)
        self.cfont = font
        self.pics = self.getPics()
        color = 'STEEL BLUE'
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.detail = btn_detail = wx.ToggleButton(self, -1, label=u'详细')
        self.detail.Bind(wx.EVT_TOGGLEBUTTON, lambda e: self.frame.OnAction(e, 6))
        self.tree = btn_tree = wx.Button(self, -1, label=u'家谱')
        self.tree.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 7))
        if flag == 0:
            self.move = btn_move = wx.Button(self, -1, label=u'移动')
#            self.status = btn_status = wx.Button(self, -1, label=u'状态')
            self.level = btn_level = wx.Button(self, -1, label=u'级别')
            self.note = btn_note = wx.Button(self, -1, label=u'附注')
            self.die = btn_die = wx.Button(self, -1, label=u'死亡')
            # OnAction() flag 1: 状态, 2: 级别, 3: 移动, 4: 死亡, 5: 附注, 6: 详细, 7: 家谱
            self.move.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 3))
#            self.status.Bind(wx.EVT_BUTTON, lambda e: self.frame.OnAction(e, 1))
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
            st_cid2 = wx.TextCtrl(self, -1, (self.mouse.cage or ''), validator=MouseValidator(2))
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
            pb_fa = self.getPB(self.mouse.father)
        except:
            pb_fa = platebtn.PlateButton(self, -1, self.mouse.father)
            pb_fa.SetPressColor(wx.Colour(33, 33, 33))
            pb_fa.SetForegroundColour(color)
            pb_fa.Bind(wx.EVT_BUTTON, self.frame.OnAddNew)
        st_mo = wx.StaticText(self, -1, u'母亲')
        try:            
            pb_mo = self.getPB(self.mouse.mother)
        except:
            pb_mo = platebtn.PlateButton(self, -1, self.mouse.mother)
            pb_mo.SetPressColor(wx.Colour(33, 33, 33))
            pb_mo.SetForegroundColour(color)
            pb_mo.Bind(wx.EVT_BUTTON, self.frame.OnAddNew)

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
        # 详细信息
        vbox.Add((-1, 10))
        line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
        vbox.Add((-1, 10))

        gs = wx.GridSizer(1, 3, 5, 5)
        sb1 = wx.StaticBox(self, -1, u'生育记录')
        box1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)
        info1 = InfoPanel(self, self.frame.farm.getBornRecords(self.frame.mid, 1))
        box1.Add(info1, 1, wx.EXPAND, 0)
        sb2 = wx.StaticBox(self, -1, u'移动记录')
        box2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)
        info2 = InfoPanel(self, self.frame.farm.getMoveRecords(self.frame.mid, 1))
        box2.Add(info2, 1, wx.EXPAND, 0)
        box3 = self.siblings = self.getView()
        gs.AddMany([(box1, 1, wx.EXPAND),
                    (box2, 1, wx.EXPAND),
                    (box3, 1, wx.EXPAND)])
        vbox.Add(gs, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        vbox.Hide(8)
        vbox.Hide(7)
        vbox.Hide(6)
        vbox.Hide(5)
        # 按钮分布及编辑界面的日期和备注
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.detail, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        hbox2.Add(self.tree, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox2.Add(wx.StaticText(self), 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        if flag == 0:
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))

            hbox2.Add(self.move, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
            hbox2.Add(self.level, 0, wx.EXPAND|wx.RIGHT, 10)
#            hbox2.Add(self.status, 0, wx.EXPAND|wx.RIGHT, 10)
            hbox2.Add(self.note, 0, wx.EXPAND|wx.RIGHT, 10)
            hbox2.Add(self.die, 0, wx.EXPAND|wx.RIGHT, 10)
        elif flag == -1 or flag == -2:
#             hbox2.Hide(0)
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))
        elif flag == 4:
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))

            hbox2.Add(self.done, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
            hbox2.Add(self.cancel, 0, wx.EXPAND|wx.RIGHT, 10)
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

            hbox2.Add(self.done, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
            hbox2.Add(self.cancel, 0, wx.EXPAND|wx.RIGHT, 10)
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
        vbox.Add(hbox2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        # 现有鼠鼠卡的笼子信息
        if not (flag == -1 or flag == -2):
            vbox.Add((-1, 10))
            line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)
            vbox.Add((-1, 10))

            gs = wx.FlexGridSizer(1, 5, 10, 5)
            for i in range(5): gs.AddGrowableCol(i, 1)
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
                try:
                    pbs = []
                    sts = []
                    cid = pre + str(n0+i)
                    cage = self.frame.farm.cages[cid]
                    c = wx.StaticBox(self, label='')
                    box = wx.StaticBoxSizer(c, wx.VERTICAL)
                    for mid in cage.guest:
                        try:
                            pb = self.getPB(mid)
                            menu = wx.Menu()
                            menu.Append(wx.NewId(), u'移动')
#                            menu.Append(wx.NewId(), u'状态')
                            menu.Append(wx.NewId(), u'级别')
                            menu.Append(wx.NewId(), u'死亡')
                            menu.SetTitle(mid)
                            pb.SetMenu(menu)
                            if mid == self.frame.mid:
                                pb.SetForegroundColour(color)
                            pbs.append(pb)
                        except:
                            pb = wx.StaticText(self, -1, mid)
                            sts.append(pb)
                    pbs = sorted(pbs, key=lambda pb: self.frame.farm.mouses[pb.GetLabel()].age(), \
                                 reverse=True)
                    total = pbs + sts
                    if total:
                        n = math.ceil(len(total) / 2.0)
                        cgs = wx.FlexGridSizer(n, 2, 0, 0)
                        cgs.Add(total[0])
                        cgs.Add(wx.StaticText(self), 0)
                        try:
                            for pb in total[1:]:
                                cgs.Add(pb)
                        except:
                            pass
                        box.Add(cgs, 0, wx.EXPAND|wx.ALL, 0)
                    else:
                        box.Add(wx.StaticText(self, -1, '', size=(40, 20)), 0, \
                                wx.ALIGN_LEFT|wx.BOTTOM, 1)
                    vbox1 = wx.BoxSizer(wx.VERTICAL)
                    pb = platebtn.PlateButton(self, -1, cid)
                    pb.SetFont(self.yfont)
                    if self.frame.farm.cages[cid].channel == u'关':
                        pb.SetForegroundColour('GREY')
                        pb.SetPressColor(wx.Colour(33, 33, 33))
                    else:
                        pb.SetPressColor(wx.RED)
                    pb.Bind(wx.EVT_RIGHT_DOWN, self.OnSwitch)
                    pb.Bind(wx.EVT_BUTTON, self.frame.OnCageCard)
                    vbox1.Add(pb)
                    vbox1.Add(box, 1, wx.EXPAND)
                except KeyError:
                    c = wx.StaticBox(self, label=' ')
                    box = wx.StaticBoxSizer(c, wx.VERTICAL)
                    box.Add(wx.StaticText(self, -1, '', size=(40, 20)), 0, \
                            wx.ALIGN_LEFT|wx.BOTTOM, 1)
                    vbox1 = wx.BoxSizer(wx.VERTICAL)
                    pb = platebtn.PlateButton(self, -1, ' ')
                    pb.SetFont(self.yfont)
                    c.Hide()
                    pb.Hide()
                    vbox1.Add(pb, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
                    vbox1.Add(box, 1, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
                gs.Add(vbox1, 1, wx.EXPAND)
            vbox.Add(gs, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        vbox.Add((-1, 10))

    def getPics(self):
        pics = {}
        im = wx.Image("boyl.png")
        im.Rescale(14, 14)
        pics['bl'] = wx.BitmapFromImage(im)
        im = wx.Image("boym.png")
        im.Rescale(14, 12, wx.IMAGE_QUALITY_HIGH)
        pics['bm'] = wx.BitmapFromImage(im)
        im = wx.Image("boys.png")
        im.Rescale(10, 10, wx.IMAGE_QUALITY_HIGH)
        pics['bs'] = wx.BitmapFromImage(im)
        im = wx.Image("girll.png")
        im.Rescale(14, 14)
        pics['gl'] = wx.BitmapFromImage(im)
        im = wx.Image("girlm.png")
        im.Rescale(14, 12, wx.IMAGE_QUALITY_HIGH)
        pics['gm'] = wx.BitmapFromImage(im)
        im = wx.Image("girls.png")
        im.Rescale(10, 10, wx.IMAGE_QUALITY_HIGH)
        pics['gs'] = wx.BitmapFromImage(im)               
        return pics
        
    def getPB(self, mid):
        m = self.frame.farm.mouses[mid]
        pb = platebtn.PlateButton(self, -1, mid)
        if m.age() <= SymList.alist[0]:
            pb.SetFont(self.cfont)
            if m.gender == SymList.glist[0]:
                pb.SetBitmap(self.pics['bs'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
            else:
                pb.SetBitmap(self.pics['gs'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
        elif SymList.alist[0] < m.age() <= SymList.alist[1]:
            pb.SetFont(self.yfont)
            if m.gender == SymList.glist[0]:
                pb.SetBitmap(self.pics['bm'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
            else:
                pb.SetBitmap(self.pics['gm'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
        else:
            pb.SetFont(self.afont)
            if m.gender == SymList.glist[0]:
                pb.SetBitmap(self.pics['bl'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
            else:
                pb.SetBitmap(self.pics['gl'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
        pb.Bind(wx.EVT_BUTTON, self.frame.OnMouseCard)
        pb.SetToolTipString(u"毛色："+m.color+u"\n级别："+m.level+\
                            u"\n年龄："+"{:.1f}".format(m.age()/30.0)+\
                            u" 月\n附注："+(m.comment or ''))
        return pb
        
    def getView(self):
        sb = wx.StaticBox(self, -1, u'同胎鼠')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        pbs = []
        sts = []
        self.pics = self.getPics()
        for mid in self.frame.farm.getSiblings(self.frame.mid):
            try:
                pb = self.getPB(mid)
                pbs.append(pb)
            except:
                pb = wx.StaticText(self, -1, mid)
                sts.append(pb)
        pbs = sorted(pbs, key=lambda pb: int(pb.GetLabel()[2:]))
        total = pbs + sts
        if total:
            n = int(math.ceil(len(total) / 3.0))
            cgs = wx.FlexGridSizer(n, 3, 0, 0)
            try:
                for pb in total:
                    cgs.Add(pb)
            except:
                pass
            box.Add(cgs, 1, wx.EXPAND)
        return box

    def OnSwitch(self, evt):
        e_obj = evt.GetEventObject()
        cid = e_obj.GetLabel()
        if self.frame.farm.cages[cid].channel == u'开':
            feedback = self.frame.farm.cages[cid].switch()
            e_obj.SetForegroundColour('GREY')
            e_obj.SetPressColor(wx.Colour(33, 33, 33))
        else:
            feedback = self.frame.farm.cages[cid].switch()
            e_obj.SetForegroundColour('BLACK')
            e_obj.SetPressColor(wx.RED)
        self.frame.statusbar.SetStatusText(feedback)
        for child in self.frame.parent.GetChildren():
            try:
                if child.GetTitle() == SymList.nlist[2]:
                    child.Update()
                elif child.GetTitle() == SymList.nlist[3]:
                    child.Update(cid)
                elif isinstance(child, cagecard.CageCard) :
                    child.Update()
                elif isinstance(child, mousecard.MouseCard) and (child != self.frame):
                    child.Update()
            except:
                pass


class MouseCard(wx.Frame):

    def __init__(self, parent, mid, farm, pos=None):
        wx.Frame.__init__(self, parent, title=u'鼠卡 '+mid)

        self.parent = parent
        self.farm = farm
        self.mid = mid
        self.statusbar = self.CreateStatusBar()
        self.InitUI()
        self.Fit()
        self.SetMinSize(self.GetSize())
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
        self.exitID = exitID = wx.NewId()
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        self.x0, self.y0 = self.GetSizeTuple()
        evt.Skip()

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
                            try:
                                if child.GetTitle() == SymList.nlist[1]:
                                    child.Update(2)
                                else:
                                    child.Update()
                            except:
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
                        try:
                            if child.GetTitle() == SymList.nlist[1]:
                                child.Update(2)
                            else:
                                child.Update()
                        except:
                            child.Update()
                elif action == u'级别':
                    mouse = self.farm.mouses[mid]
                    sd = dialog.SimpleLevelDialog(self, mouse)
                    sd.ShowModal()
                    if sd.change:
                        feedback = self.farm.change(mid, sd.level)
                        for child in self.parent.GetChildren():
                            try:
                                if child.GetTitle() == SymList.nlist[1]:
                                    child.Update(2)
                                else:
                                    child.Update()
                            except:
                                child.Update()
                        self.statusbar.SetStatusText(feedback)
                    sd.Destroy()
                elif action == u'死亡':
                    feedback = self.farm.burn(mid)
                    self.statusbar.SetStatusText(feedback)
                    for child in self.parent.GetChildren():
                        try:
                            if child.GetTitle() == SymList.nlist[1]:
                                child.Update(2)
                            else:
                                child.Update()
                        except:
                            child.Update()

    def OnAction(self, event, flag):
        if (flag != 6) and (flag != 7):
            label = self.panel.detail.GetLabel()
            self.panel = MouseCardPanel(self, flag)
            vbox = self.panel.GetSizer()
            if label == u'简洁':
                self.panel.detail.SetValue(True)
                self.panel.detail.SetLabel(u'简洁')
                vbox.Show(8)
                vbox.Show(7)
                vbox.Show(6)
                vbox.Show(5)
            self.sizer.Hide(0)
            self.sizer.Remove(0)
            self.sizer.Add(self.panel, 1, wx.EXPAND)
        elif flag == 7:
            pos = self.GetPosition()+wx.Point(20, 20)
            familytree.FamilyTree(self.parent, self.mid, self.farm, pos)
        else:
            vbox = self.panel.GetSizer()
            if self.panel.detail.GetLabel() == u'详细':
                self.panel.detail.SetLabel(u'简洁')
                vbox.Show(8)
                vbox.Show(7)
                vbox.Show(6)
                vbox.Show(5)                
            else:
                self.panel.detail.SetLabel(u'详细')
                vbox.Hide(8)
                vbox.Hide(7)
                vbox.Hide(6)
                vbox.Hide(5)
        self.Unbind(wx.EVT_SIZE)
        self.Layout()
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def Update(self):
        try:
            status = self.farm.mouses[self.mid].status
            label = self.panel.detail.GetLabel()
            if status == u'死亡':
                self.panel = MouseCardPanel(self, -2)
            elif status == u'已售':
                self.panel = MouseCardPanel(self, -1)
            else:
                self.panel = MouseCardPanel(self, 0)
            vbox = self.panel.GetSizer()
            if label == u'简洁':
                self.panel.detail.SetValue(True)
                self.panel.detail.SetLabel(u'简洁')
                vbox.Show(8)
                vbox.Show(7)
                vbox.Show(6)
                vbox.Show(5)
            self.sizer.Hide(0)
            self.sizer.Remove(0)
            self.sizer.Add(self.panel, 1, wx.EXPAND)
            self.Unbind(wx.EVT_SIZE)
            self.Layout()
            self.SetMinSize((1, 1))
            x1, y1 = self.GetBestSizeTuple()
            self.SetMinSize((x1, y1))
            x, y = max(self.x0, x1), max(self.y0, y1)
            self.SetSize((x, y))
            self.Bind(wx.EVT_SIZE, self.OnSize)
        except:
            self.Destroy() # 解决穿越导致的鼠卡为还不存在鼠的矛盾

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
            try:
                if child.GetTitle() == SymList.nlist[1]:
                    child.Update(2)
                elif child == self:
                    self.Update()
                    self.statusbar.SetStatusText(feedback)
                else:
                    child.Update()
            except:
                child.Update()

    def OnCancel(self, event):
        self.Update()

    def OnMouseCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        MouseCard(self.parent, pb.GetLabel(), self.farm, pos=pos)
        
    def OnCageCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        cagecard.CageCard(self.parent, pb.GetLabel(), self.farm, pos=pos)
        
    def OnAddNew(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        addnew.AddNew(self.parent, self.farm, pb.GetLabel(), pos=pos)


if __name__ == '__main__':

    app = wx.App()
    from mousecore import *
    f = Farm()
    MouseCard(None, 'AX1', f)
    app.MainLoop()

