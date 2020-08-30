# -*- coding: utf-8 -*-
# Filename: familytree.py


import wx
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn
import wx.lib.scrolledpanel as scrolled
    
from mousecore import *
import mousecard
import addnew


class TreePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, level):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.frame = parent.frame
        self.pics = self.getPics()
        self.delta = 2 if (os.name == 'posix') else 1
        self.plist = []
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
        self.color = 'STEEL BLUE'

        gs = self.genTree(self.frame.mid, level)
        self.SetSizer(gs)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def skip(self, gs, n):
        for i in range(n): gs.Add(wx.StaticText(self))
        
    def genTree(self, mid, n):
        if n > 1:
            gs = wx.FlexGridSizer(2, 3, 0, 0)
            gs.AddGrowableRow(0, 1)
            gs.AddGrowableRow(1, n-1)
            for i in range(3): gs.AddGrowableCol(i, 1)
            self.skip(gs, 1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            try:
                m = self.frame.farm.mouses[mid]
                pb = self.getPB(mid)
                vbox.Add(pb, 0, wx.ALIGN_CENTER_HORIZONTAL)
                info = wx.StaticText(self, -1, m.comment, size=(-1, 80))
                info.SetFont(self.yfont)
                info.SetForegroundColour('GREY')
                vbox.Add(info, 0, wx.ALIGN_CENTER_HORIZONTAL)
            except KeyError:
                pb = platebtn.PlateButton(self, -1, mid)
                pb.SetPressColor(wx.Colour(33, 33, 33))
                if mid == u'?':
                    pb.SetForegroundColour('GREY')
                else:
                    pb.Bind(wx.EVT_BUTTON, self.frame.OnAddNew)
                vbox.Add(pb, 0, wx.ALIGN_CENTER_HORIZONTAL)
                info = wx.StaticText(self, size=(-1, 80))
                vbox.Add(info, 0, wx.ALIGN_CENTER_HORIZONTAL)
            gs.Add(vbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
            self.skip(gs, 1)
            try:
                m = self.frame.farm.mouses[mid]
                father = m.father if m.father[:1].isupper() else u'?'
                mother = m.mother if m.mother[:1].isupper() else u'?'
            except KeyError:
                father = u'?'
                mother = u'?'
            fa = self.genTree(father, n-1)
            gs.Add(fa, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
            self.skip(gs, 1)
            mo = self.genTree(mother, n-1)
            gs.Add(mo, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
        else:
            gs = wx.FlexGridSizer(1, 1, 0, 0)
            gs.AddGrowableRow(0, 1)
            gs.AddGrowableCol(0, 1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            try:
                m = self.frame.farm.mouses[mid]
                pb = self.getPB(mid)
                vbox.Add(pb, 0, wx.ALIGN_CENTER_HORIZONTAL)
                info = wx.StaticText(self, -1, m.comment, size=(-1, 80))
                info.SetFont(self.yfont)
                info.SetForegroundColour('GREY')
                vbox.Add(info, 0, wx.ALIGN_CENTER_HORIZONTAL)
            except KeyError:
                pb = platebtn.PlateButton(self, -1, mid)
                pb.SetPressColor(wx.Colour(33, 33, 33))
                if mid == u'?':
                    pb.SetForegroundColour('GREY')
                else:
                    pb.Bind(wx.EVT_BUTTON, self.frame.OnAddNew)
                vbox.Add(pb, 0, wx.ALIGN_CENTER_HORIZONTAL)
                info = wx.StaticText(self, size=(-1, 80))
                vbox.Add(info, 0, wx.ALIGN_CENTER_HORIZONTAL)
            gs.Add(vbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.plist.append(pb)
        return gs
        
    def OnPaint(self, evt=None):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.Colour(180, 180, 180), 1))
        
        def draw(pb0, pb1, pb2):
            x0 = pb0.GetPosition()[0] + pb0.GetSize()[0]/2
            y0 = pb0.GetPosition()[1]
            x1 = pb1.GetPosition()[0] + pb1.GetSize()[0]/2
            y1 = pb1.GetPosition()[1]
            x2l = pb2.GetPosition()[0]
            x2r = pb2.GetPosition()[0] + pb2.GetSize()[0]
            y2 = pb2.GetPosition()[1] + pb2.GetSize()[1]/2
            dc.SetPen(wx.Pen(wx.Colour(72, 136, 208), 1))
            dc.DrawLine(x0, y0, x0, y2)
            dc.DrawLine(x0, y2, x2l, y2)
            dc.SetPen(wx.Pen(wx.Colour(210, 78, 74), 1))
            dc.DrawLine(x1, y1, x1, y2)
            dc.DrawLine(x1, y2, x2r, y2)

#        def travelDraw(plist):
#            n = len(plist)
#            if n > 1:
#                draw(plist[(n-3)/2], plist[-2], plist[-1])
#                travelDraw(plist[:(n-1)/2])
#                travelDraw(plist[(n-1)/2:-1])
#            else:
#                pass

        def get2Power(n):
            num = 0
            if n:
                while not (n % 2):
                    n /= 2
                    num += 1
            return num

        def travelDraw(plist):
            pl = plist[:]
            n = len(pl)
            while n > 1:
                left = 0
                for i in range((n+1)/4):
                    draw(pl[left], pl[left+1], pl[left+2])
                    pl.pop(left+1)
                    pl.pop(left)
                    left += (1+get2Power(i+1))
                n = len(pl)

        travelDraw(self.plist)
        
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


class FamilyTreePanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        
        self.level = 3
        self.frame = parent
        
        sb = wx.StaticBox(self, label='')
        self.tree = box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        tp = TreePanel(self, self.level)
        box.Add(tp, 1, wx.EXPAND|wx.ALL, 20)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.ALL, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.ALL^wx.TOP, 10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.back = btn = wx.Button(self, -1, u'关闭')
        self.plus = btn_p = wx.Button(self, -1, u'展开')
        self.minus = btn_m = wx.Button(self, -1, u'折叠')
        hbox.Add(btn_p, 0, wx.LEFT, 0)
        hbox.Add(btn_m, 0, wx.LEFT, 10)
        hbox.Add(wx.StaticText(self), 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        hbox.Add(btn, 0, wx.RIGHT, 0)
        vbox.Add(hbox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        
class FamilyTree(wx.Frame):
  
    def __init__(self, parent, mid, farm, pos=None):
        wx.Frame.__init__(self, parent)
        self.parent = parent
        self.farm = farm
        self.mid = mid
        self.SetTitle(u'鼠 ' + mid + u' 的家谱')
        self.InitUI()
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Centre()
                
        if pos:
            self.Move(pos)
        self.Show()
        
    def InitUI(self):
        self.panel = panel = FamilyTreePanel(self)
        self.statusbar = self.CreateStatusBar()
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnBack,id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('W'), exitID)])
        self.SetAcceleratorTable(accel_tbl)
                
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.panel.back)
        self.Bind(wx.EVT_BUTTON, self.OnPlus, self.panel.plus)
        self.Bind(wx.EVT_BUTTON, self.OnMinus, self.panel.minus)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnSize(self, evt):
        self.x0, self.y0 = self.GetSizeTuple()
        evt.Skip()
        
    def OnBack(self, event):
        self.Destroy()
        
    def OnPlus(self, event):
        self.panel.level += 1
        self.panel.tree.Hide(0)
        self.panel.tree.Remove(0)
        tp = TreePanel(self.panel, self.panel.level)
        self.panel.tree.Add(tp, 1, wx.EXPAND|wx.ALL, 20)
        self.Layout()
        self.Unbind(wx.EVT_SIZE)
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        xm, ym = 1000, 600
        x1, y1 = min(x1, xm), min(y1, ym)
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        tp.SetupScrolling()
    
    def OnMinus(self, event):
        self.panel.level -= 1
        self.panel.tree.Hide(0)
        self.panel.tree.Remove(0)
        tp = TreePanel(self.panel, self.panel.level)
        self.panel.tree.Add(tp, 1, wx.EXPAND|wx.ALL, 20)
        self.Layout()
        self.Unbind(wx.EVT_SIZE)
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        xm, ym = 1000, 600
        x1, y1 = min(x1, xm), min(y1, ym)
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        tp.SetupScrolling()
        
    def OnMouseCard(self, evt):
        pos = self.GetPosition()+wx.Point(20, 20)
        pb = evt.GetEventObject()
        mousecard.MouseCard(self.parent, pb.GetLabel(), self.farm, pos=pos)
        
    def Update(self):
        self.panel.tree.Hide(0)
        self.panel.tree.Remove(0)
        tp = TreePanel(self.panel, self.panel.level)
        self.panel.tree.Add(tp, 1, wx.EXPAND|wx.ALL, 20)
        self.Layout()
        self.Unbind(wx.EVT_SIZE)
        self.SetMinSize((1, 1))
        x1, y1 = self.GetBestSizeTuple()
        xm, ym = 1000, 600
        x1, y1 = min(x1, xm), min(y1, ym)
        self.SetMinSize((x1, y1))
        x, y = max(self.x0, x1), max(self.y0, y1)
        self.SetSize((x, y))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        tp.SetupScrolling()
        
    def OnAddNew(self, evt):
        pb = evt.GetEventObject()
        pos = self.GetPosition()+wx.Point(20, 20)
        addnew.AddNew(self.parent, self.farm, pb.GetLabel(), pos=pos)


if __name__ == '__main__':
  
    app = wx.App()
    FamilyTree(None, title=u'血统')
    app.MainLoop()
    
