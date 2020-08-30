# -*- coding: utf-8 -*-
# Filename: overview.py


import math
import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

from mousecore import *
import mousecard
import cagecard
import familytree
import dialog


class OverviewPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.delta = 2 if (os.name == 'posix') else 1
        tc = wx.TextCtrl(self, -1, 'A')
        font = tc.GetFont()
        tc.Hide()
        self.afont = font
        size = font.GetPointSize()
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
        color = 'STEEL BLUE'
        self.frame = parent
        self.pics = self.getPics()

        self.sizer = vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        vbox.Add((-1, 10))

        self.hbox = hbox = wx.BoxSizer(wx.HORIZONTAL)
        st_house = wx.StaticText(self, -1, u'鼠房')
        st_row = wx.StaticText(self, -1, u'排数')

        self.info, self.rowinfo = self.getInfo()
        houses = sorted(self.info.keys())
        # 考虑鼠厂初始状态无鼠
        try:
            rows = [str(i) for i in range(1, self.rowinfo['1']+1)]
        except:
            rows = []
        self.house = co_house = wx.Choice(self, -1, choices=houses)
        if houses:
            self.house.SetStringSelection(houses[0])
        self.row = co_row = wx.Choice(self, -1, choices=rows)
        if rows:
            self.row.SetStringSelection(rows[0])
        hbox.Add(st_house, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
        hbox.Add(co_house, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        hbox.Add(st_row, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
        hbox.Add(co_row, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        vbox.Add(hbox)

        vbox.Add((-1, 10))

        line = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)

        vbox.Add((-1, 10))

        try:
            cids = self.getCages(houses[0], rows[0])
        except:
            cids = []
        gs = self.getView(cids)

        vbox.Add(gs, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        vbox.Add((-1, 10))

        self.house.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.row.Bind(wx.EVT_CHOICE, self.OnChoice)

        self.Bind(wx.EVT_MENU, self.OnMenu)

    def getInfo(self):
        cids = self.frame.farm.cages.keys()
        info = {}
        rowinfo = {}
        for cid in cids:
            try:
                house, num = cid.split('-')
                if house in info:
                    info[house].append(num)
                else:
                    info[house] = [num]
            except:
                if '1' in info:
                    info['1'].append(cid)
                else:
                    info['1'] = [cid]
        for key in info.keys():
            info[key] = sorted(info[key], key=lambda e: int(e))
            rowinfo[key] = int(math.ceil(len(info[key]) / 70.0))
        return info, rowinfo

    def getCages(self, house, row):
        try:
            cages = self.info[house]
        except:
            cages = []
        a = (int(row)-1)*70
        b = int(row)*70
        if house == '1':
            return cages[a:b]
        else:
            return [house+'-'+num for num in cages[a:b]]

    def getView(self, cids):
        gs = wx.FlexGridSizer(7, 11, 1, 2)
        for i in range(7): gs.AddGrowableRow(i, 1)
        for i in range(5): gs.AddGrowableCol(i, 1)
        for i in range(6, 11): gs.AddGrowableCol(i, 1)
        self.cagedict = {}
        for i in range(7*10):
            try:
                pbs = []
                sts = []
                cid = cids[i]
                cage = self.frame.farm.cages[cid]
                c = wx.StaticBox(self, label='')
                box = wx.StaticBoxSizer(c, wx.VERTICAL)
                for mid in cage.guest:
                    try:
                        pb = self.getPB(mid)
                        pbs.append(pb)
                    except:
                        pb = wx.StaticText(self, -1, mid)
                        sts.append(pb)
                pbs = sorted(pbs, key=lambda pb: self.frame.farm.mouses[pb.GetLabel()].age(),\
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
                    box.Add(wx.StaticText(self, -1, '', size=(40, 20)), 0, wx.ALIGN_LEFT|wx.BOTTOM, 1)
                if not ((i - 5) % 10):
                    gs.Add(wx.StaticText(self, -1, '', size=(20, -1)), 0, wx.EXPAND)
                vbox = wx.BoxSizer(wx.VERTICAL)
                pb = platebtn.PlateButton(self, -1, cid)
                pb.SetFont(self.yfont)
                if self.frame.farm.cages[cid].channel == u'关':
                    pb.SetForegroundColour('GREY')
                    pb.SetPressColor(wx.Colour(33, 33, 33))
                else:
                    pb.SetPressColor(wx.RED)
                pb.Bind(wx.EVT_RIGHT_DOWN, self.OnSwitch)
                pb.Bind(wx.EVT_BUTTON, self.frame.OnCageCard)
                self.cagedict[cid] = pb
                vbox.Add(pb)
                vbox.Add(box, 1, wx.EXPAND)
            except:
                c = wx.StaticBox(self, label='')
                box = wx.StaticBoxSizer(c, wx.VERTICAL)
                box.Add(wx.StaticText(self, -1, '', size=(40, 20)), 0, wx.ALIGN_LEFT|wx.BOTTOM, 1)
                if not ((i - 5) % 10):
                    gs.Add(wx.StaticText(self, -1, '', size=(20, -1)), 0, wx.EXPAND)
                vbox = wx.BoxSizer(wx.VERTICAL)
                pb = platebtn.PlateButton(self, -1, ' ')
                pb.SetFont(self.yfont)
                c.Hide()
                pb.Hide()
                vbox.Add(pb, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
                vbox.Add(box, 1, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
            gs.Add(vbox, 1, wx.EXPAND)
        return gs

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
            else:
                pb.SetBitmap(self.pics['gs'])
        elif SymList.alist[0] < m.age() <= SymList.alist[1]:
            pb.SetFont(self.yfont)
            if m.gender == SymList.glist[0]:
                pb.SetBitmap(self.pics['bm'])
            else:
                pb.SetBitmap(self.pics['gm'])
        else:
            pb.SetFont(self.afont)
            if m.gender == SymList.glist[0]:
                pb.SetBitmap(self.pics['bl'])
            else:
                pb.SetBitmap(self.pics['gl'])
        pb.Bind(wx.EVT_BUTTON, self.frame.OnMouseCard)
        menu = wx.Menu()
        menu.Append(wx.NewId(), u'移动')
#        menu.Append(wx.NewId(), u'状态')
        menu.Append(wx.NewId(), u'级别')
        menu.Append(wx.NewId(), u'死亡')
        menu.AppendSeparator()
        menu.Append(wx.NewId(), u'家谱')
        menu.SetTitle(mid)
        pb.SetMenu(menu)
        pb.SetToolTipString(u"毛色："+m.color+u"\n级别："+m.level+\
                            u"\n年龄："+"{:.1f}".format(m.age()/30.0)+\
                            u" 月\n附注："+(m.comment or ''))
        return pb

    def OnMenu(self, evt):
        e_obj = evt.GetEventObject()
        if evt.GetId() == self.frame.exitID:
            self.frame.Destroy()
        else:
            try:
                mitem = e_obj.FindItemById(evt.GetId())
                if mitem != wx.NOT_FOUND:
                    action = mitem.GetItemLabel()
                    mid = e_obj.GetTitle()
                    if action == u'移动':
                        mouse = self.frame.farm.mouses[mid]
                        md = dialog.SimpleMoveDialog(self, mouse)
                        md.ShowModal()
                        if md.move:
                            feedback = self.frame.farm.move(mid, md.cid)
                            for child in self.frame.parent.GetChildren():
                                try:
                                    if child.GetTitle() == SymList.nlist[1]:
                                        child.Update(2)
                                    else:
                                        child.Update()
                                except:
                                    child.Update()
                            self.frame.statusbar.SetStatusText(feedback)
                        md.Destroy()
                    elif action == u'状态':
                        if self.frame.farm.mouses[mid].status == u'生病':
                            feedback = self.frame.farm.change(mid, u'正常')
                        else:
                            feedback = self.frame.farm.change(mid, u'生病')
                        self.frame.statusbar.SetStatusText(feedback)
                        for child in self.frame.parent.GetChildren():
                            try:
                                if child.GetTitle() == SymList.nlist[1]:
                                    child.Update(2)
                                else:
                                    child.Update()
                            except:
                                child.Update()
                    elif action == u'级别':
                        mouse = self.frame.farm.mouses[mid]
                        sd = dialog.SimpleLevelDialog(self, mouse)
                        sd.ShowModal()
                        if sd.change:
                            feedback = self.frame.farm.change(mid, sd.level)
                            for child in self.frame.parent.GetChildren():
                                try:
                                    if child.GetTitle() == SymList.nlist[1]:
                                        child.Update(2)
                                    else:
                                        child.Update()
                                except:
                                    child.Update()
                            self.frame.statusbar.SetStatusText(feedback)
                        sd.Destroy()
                    elif action == u'死亡':
                        feedback = self.frame.farm.burn(mid)
                        self.frame.statusbar.SetStatusText(feedback)
                        for child in self.frame.parent.GetChildren():
                            try:
                                if child.GetTitle() == SymList.nlist[1]:
                                    child.Update(2)
                                else:
                                    child.Update()
                            except:
                                child.Update()
                    elif action == u'家谱':
                        pos = self.frame.GetPosition()+wx.Point(20, 20)
                        familytree.FamilyTree(self.frame.parent, mid, self.frame.farm, pos)
            except:
                pos = self.frame.GetPosition()+wx.Point(20, 20)
                mid = e_obj.GetLabel()
                mousecard.MouseCard(self.frame.parent, mid, self.frame.farm, pos=pos)

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
                elif isinstance(child, cagecard.CageCard):
                    child.Update()
                elif isinstance(child, mousecard.MouseCard):
                    child.Update()
            except:
                pass

    def OnChoice(self, evt):
        house = self.house.GetStringSelection()
        rows = [str(i) for i in range(1, self.rowinfo[house]+1)]
        row = str(min(int(self.row.GetStringSelection()), self.rowinfo[house]))
        self.row.SetItems(rows)
        self.row.SetStringSelection(row)

        cids = self.getCages(house, row)
        gs = self.getView(cids)

        self.sizer.Hide(6)
        self.sizer.Hide(5)
        self.sizer.Remove(6)
        self.sizer.Remove(5)
        self.sizer.Add(gs, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        self.sizer.Add((-1, 10))

        self.sizer.Layout()
        self.frame.SetMinSize((1, 1))
        x0, y0 = self.frame.GetSizeTuple()
        x1, y1 = self.frame.GetBestSizeTuple()
        self.frame.SetMinSize((x1, y1))
        x, y = max(x0, x1), max(y0, y1)
        self.frame.SetSize((x, y))


class Overview(wx.Frame):

    def __init__(self, parent, farm):
        wx.Frame.__init__(self, parent)
        self.statusbar = self.CreateStatusBar()
        self.parent = parent
        self.farm = farm
        self.SetTitle(SymList.nlist[3])
        self.InitUI()
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Center()
        self.Show()

    def InitUI(self):
        self.panel = OverviewPanel(self)

        self.sizer = sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.exitID = exitID = wx.NewId()
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)
        self.Bind(wx.EVT_MENU, self.panel.OnMenu)

    def Update(self, flag=0):
        if not flag:
            house = self.panel.house.GetStringSelection()
            row = self.panel.row.GetStringSelection()
            self.panel.info, self.panel.rowinfo = self.panel.getInfo()
            houses = sorted(self.panel.info.keys())
            try:
                rows = [str(i) for i in range(1, self.panel.rowinfo[house]+1)]
            except:
                try:
                    house = houses[0]
                    rows = [str(i) for i in range(1, self.panel.rowinfo[house]+1)]
                    row = rows[0]
                except:
                    rows = []
            self.panel.house.SetItems(houses)
            self.panel.row.SetItems(rows)
            try:
                self.panel.house.SetStringSelection(house)
                self.panel.row.SetStringSelection(row)
                cids = self.panel.getCages(house, row)
            except:
                cids = []
            gs = self.panel.getView(cids)

            self.panel.sizer.Hide(6)
            self.panel.sizer.Hide(5)
            self.panel.sizer.Remove(6)
            self.panel.sizer.Remove(5)
            self.panel.sizer.Add(gs, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
            self.panel.sizer.Add((-1, 10))

            self.panel.sizer.Layout()
            self.SetMinSize((1, 1))
            x0, y0 = self.GetSizeTuple()
            x1, y1 = self.GetBestSizeTuple()
            self.SetMinSize((x1, y1))
            x, y = max(x0, x1), max(y0, y1)
            self.SetSize((x, y))
        else:
            pb = self.panel.cagedict[flag]
            if self.farm.cages[flag].channel == u'关':
                pb.SetForegroundColour('GREY')
                pb.SetPressColor(wx.Colour(33, 33, 33))
            else:
                pb.SetForegroundColour('BLACK')
                pb.SetPressColor(wx.RED)

    def OnMouseCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        mousecard.MouseCard(self.parent, pb.GetLabel(), self.farm, pos=pos)

    def OnCageCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        cagecard.CageCard(self.parent, pb.GetLabel(), self.farm, pos=pos)

if __name__ == '__main__':

    app = wx.App()
    Overview(None)
    app.MainLoop()


