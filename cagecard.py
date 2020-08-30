#!/usr/bin/python
# -*- coding: utf-8 -*-


import math
import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

from mousecore import *
import mousecard
import dialog


class CageCardPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.frame = parent
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
        vbox.Add((-1, 10))
        # 现有鼠鼠卡的笼子信息
        gs = wx.FlexGridSizer(1, 5, 10, 5)
        for i in range(5): gs.AddGrowableCol(i, 1)
        cid = self.frame.cid
        cage = self.frame.farm.cages[cid]
        if cage.house != '1':
            num = int(cid.split('-')[1])
            pre = cage.house + '-'
        else:
            num = int(cid)
            pre = ''
        n0 = num - ((num - 1) % 5)
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
                if self.frame.cid == cid:
                    font = pb.GetFont()
                    font.SetWeight(wx.BOLD)
                    pb.SetFont(font)
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
                elif isinstance(child, CageCard) and (child != self.frame):
                    child.Update()
                elif isinstance(child, mousecard.MouseCard):
                    child.Update()
            except:
                pass

class CageCard(wx.Frame):

    def __init__(self, parent, cid, farm, pos=None):
        wx.Frame.__init__(self, parent, title=u'笼卡 '+cid)

        self.parent = parent
        self.farm = farm
        self.cid = cid
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

        self.panel = CageCardPanel(self)
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

    def Update(self):
        try:
            self.panel = CageCardPanel(self)
            vbox = self.panel.GetSizer()
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
            self.Destroy() # 解决穿越导致的笼卡为还不存在笼的矛盾

    def OnMouseCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        mousecard.MouseCard(self.parent, pb.GetLabel(), self.farm, pos=pos)

    def OnCageCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        CageCard(self.parent, pb.GetLabel(), self.farm, pos=pos)


if __name__ == '__main__':

    app = wx.App()
    from mousecore import *
    f = Farm()
    MouseCard(None, 'AX1', f)
    app.MainLoop()

