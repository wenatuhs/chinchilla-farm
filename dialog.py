#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
import math
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn
from mousecore import *
from validator import *


class LoginDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.InitUI()
        self.parent = parent
        self.SetTitle(u'登陆')
        self.EnableCloseButton(False)
        self.Fit()
        self.Center()
        p = self.GetPosition()
        self.Move(p+wx.Point(0, -100))

    def InitUI(self):

        self.panel = panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)        
        
        st1 = wx.StaticText(panel, -1, u"用户名")
        st2 = wx.StaticText(panel, -1, u"密码")
        self.username = tc1 = wx.TextCtrl(panel, -1, "admin")
        self.password = tc2 = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        fgs = wx.FlexGridSizer(2, 2, 10, 10)
        fgs.AddGrowableCol(1, 1)
        fgs.AddMany([(st1, 0, wx.ALIGN_CENTER_VERTICAL, 0),
                     (tc1, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0),
                     (st2, 0, wx.ALIGN_CENTER_VERTICAL, 0),
                     (tc2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)])
        extra = (5 if os.name == 'posix' else 10)
        box.Add(fgs, 0, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_app = wx.Button(panel, -1, u'登陆')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_app, 0, wx.LEFT|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.BOTTOM|wx.ALIGN_RIGHT, 10)
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.password.SetFocus()
        self.Bind(wx.EVT_BUTTON, self.OnConfirm, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnClose, b_can)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfirm, tc2)
                
    def OnClose(self, evt):        
        self.Close()
        self.parent.Destroy()
        
    def OnConfirm(self, evt):
        username = self.username.GetValue()
        password = self.password.GetValue()
        if self.parent.check(username, password):
            self.Close()
            self.parent.Show()
        else:
            self.username.SetValue('')
            self.password.SetValue('')
            self.username.SetFocus()
            self.SetTitle(u"用户名或密码不正确！")


class SellDialog(wx.Dialog):
    
    def __init__(self, parent, mids, farm):
        wx.Dialog.__init__(self, parent) 
        
        self.farm = farm
        self.mids = mids
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
        self.InitUI()
        self.SetTitle(u'确认出售鼠')
        self.Fit()
        self.Center()
        p = self.GetPosition()        
        self.Move(p+wx.Point(0, -100))
                
    def InitUI(self):

        self.panel = panel = wx.Panel(self)
        self.sold = False
        self.extra = extra = (5 if os.name == 'posix' else 10)
        
        color = 'STEEL BLUE'
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)
                
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st0 = wx.StaticText(panel, label=u'于时间')
        self.dpc = dpc = wx.DatePickerCtrl(panel)
        st1 = wx.StaticText(panel, label=u'出售至')
        gs = self.getView()
        self.buy = tc2 = wx.ComboBox(panel, choices=SymList.blist, style=wx.CB_DROPDOWN)
        try:
            self.buy.SetValue(SymList.blist[0])
        except:
            pass
        box.Add(gs, 1, wx.EXPAND|wx.ALL, extra)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st0, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(dpc, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        hbox.Add(st1, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        hbox.Add(tc2, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        box.Add(hbox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, extra)

        line = wx.StaticLine(panel, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
        box.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 0)

        st = wx.StaticText(panel, label=u'备注')
        self.cmt = tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 100))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st, 0, wx.LEFT, 0)
        hbox.Add((5, -1))
        hbox.Add(tc, 1, wx.EXPAND|wx.RIGHT, 0)
        if os.name == 'posix': box.Add((-1, extra))
        box.Add(hbox, 0, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':            
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_app = wx.Button(panel, -1, u'确定')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_app, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnSell, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnClose, b_can)
        
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
        
    def getView(self):
        sb = wx.StaticBox(self, -1, u'下列鼠')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        pbs = []
        sts = []
        self.pics = self.getPics()
        for mid in self.mids:
            try:
                pb = self.getPB(mid)
                pbs.append(pb)
            except:
                pb = wx.StaticText(self, -1, mid)
                sts.append(pb)
        pbs = sorted(pbs, key=lambda pb: self.farm.mouses[pb.GetLabel()].age(),\
                     reverse=True)
        total = pbs + sts
        if total:
            n = int(math.ceil(len(total) / 5.0))
            cgs = wx.FlexGridSizer(n, 5, 0, 0)
            try:
                for pb in total:
                    cgs.Add(pb)
            except:
                pass
            box.Add(cgs, 1, wx.EXPAND)
        return box
        
    def getPB(self, mid):
        m = self.farm.mouses[mid]
        pb = platebtn.PlateButton(self, -1, mid)
        if m.age() <= SymList.alist[0]:
            pb.SetFont(self.cfont)
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
        elif SymList.alist[0] < m.age() <= SymList.alist[1]:
            pb.SetFont(self.yfont)
            if m.gender == SymList.glist[0]:
                pb.SetBitmap(self.pics['bl'])
                if m.status == SymList.slist[1]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GREY')
            else:
                pb.SetBitmap(self.pics['gl'])
                if m.status == SymList.slist[2]:
                    pb.SetForegroundColour('GOLD')
                elif m.status == SymList.slist[3]:
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
        pb.SetToolTipString(u"毛色："+m.color+u"\n级别："+m.level+\
                            u"\n年龄："+"{:.1f}".format(m.age()/30.0)+\
                            u" 月\n附注："+(m.comment or ''))
        return pb
                
    def OnClose(self, evt):
        self.Close()
        
    def OnSell(self, evt):
        self.sold = True
        self.buyer = self.buy.GetValue()
        self.comment = self.cmt.GetValue()
        self.date = self.dpc.GetValue().Format('%Y-%m-%d')
        self.Close()

        
class SimpleMoveDialog(wx.Dialog):
    
    def __init__(self, parent, mouse):
        wx.Dialog.__init__(self, parent) 
            
        self.InitUI(mouse)
        self.SetTitle(u'移动鼠 '+mouse.id)
        self.Fit()
        self.Center()
        p = self.GetPosition()
        self.Move(p+wx.Point(0, -100))
                
    def InitUI(self, mouse):

        self.panel = panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)        
        
        self.move = False        
        color = 'STEEL BLUE'
        
        self.tc = tc = wx.TextCtrl(panel, -1, size=(70, -1), validator=MouseValidator(2))
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st1 = wx.StaticText(panel, label=u'将鼠 ')
        mid = wx.StaticText(panel, label=mouse.id)
        mid.SetForegroundColour(color)
        st2 = wx.StaticText(panel, label=u' 从笼 ')        
        cid = wx.StaticText(panel, label=mouse.cage)
        cid.SetForegroundColour(color)
        st3 = wx.StaticText(panel, label=u' 移动至笼 ')
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(mid, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(cid, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(st3, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add((5, -1))
        hbox.Add(tc, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        extra = (5 if os.name == 'posix' else 10)
        box.Add(hbox, 0, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_app = wx.Button(panel, -1, u'确定')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_app, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)        
        
        self.Bind(wx.EVT_BUTTON, self.OnMove, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnClose, b_can)
                
    def OnClose(self, evt):        
        self.Close()
        
    def OnMove(self, evt):
        self.move = True
        self.cid = self.tc.GetValue()
        self.Close()


class SimpleLevelDialog(wx.Dialog):
    
    def __init__(self, parent, mouse):
        wx.Dialog.__init__(self, parent) 
            
        self.InitUI(mouse)
        self.SetTitle(u'改变鼠 '+mouse.id+u' 的级别')
        self.Fit()
        self.Center()
        p = self.GetPosition()
        self.Move(p+wx.Point(0, -100))
                
    def InitUI(self, mouse):

        self.panel = panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)        
        
        self.change = False
        color = 'STEEL BLUE'
        
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st1 = wx.StaticText(panel, label=u'将鼠 ')
        mid = wx.StaticText(panel, label=mouse.id)
        mid.SetForegroundColour(color)
        st2 = wx.StaticText(panel, label=u' 的级别从 ')
        cid = wx.StaticText(panel, label=mouse.level)
        cid.SetForegroundColour(color)
        st3 = wx.StaticText(panel, label=u' 改变为 ')
        self.cho = cho = wx.Choice(panel, -1, choices=SymList.llist)
        try:
            self.cho.SetStringSelection(SymList.llist[0])
        except:
            pass
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(mid, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(cid, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(st3, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add((5, -1))
        hbox.Add(cho, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        extra = (5 if os.name == 'posix' else 10)
        box.Add(hbox, 0, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_app = wx.Button(panel, -1, u'确定')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_app, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)        
        
        self.Bind(wx.EVT_BUTTON, self.OnLevel, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnClose, b_can)
                
    def OnClose(self, evt):        
        self.Close()
        
    def OnLevel(self, evt):
        self.change = True
        self.level = self.cho.GetStringSelection()
        self.Close()


class LoadDialog(wx.Dialog):
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent) 
            
        self.InitUI()
        self.SetTitle(u'选择数据库')
        self.Fit()
        self.Center()
        p = self.GetPosition()
        self.Move(p+wx.Point(0, -100))
                
    def InitUI(self):

        panel = wx.Panel(self)        
        
        color = 'STEEL BLUE'        
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)
        
        import os
        datelist = [f.split('.')[0].split('_')[1] for f in os.listdir('./database/') \
                    if (f.startswith('farm') and f != 'farm.db')]
        datelist = [u"默认"] + sorted(datelist, reverse=True)
        self.fname = cb = wx.Choice(panel, size=(160, -1), choices=datelist)
        self.fname.SetStringSelection(u"默认")
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st = wx.StaticText(panel, label=u'请在列表中选择一个数据库进行读取：')
        extra = (5 if os.name == 'posix' else 10)
        box.Add(st, 0, wx.EXPAND|wx.ALL, extra)
        box.Add(cb, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, extra)
        if os.name == 'posix':
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)        
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_app = wx.Button(panel, -1, u'读取')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_app, 0, wx.EXPAND|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.BOTTOM|wx.ALIGN_RIGHT, 10)
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnApply, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnClose, b_can)
                
    def OnClose(self, evt):
        self.database = None
        self.Close()
        
    def OnApply(self, evt):
        choice = self.fname.GetStringSelection()
        if choice == u'默认':
            self.database = Farm.filename
        else:
            self.database = './database/farm_' + choice + '.db'
        self.Close()
                     

class AddNewDialog(wx.Dialog):
    
    def __init__(self, parent, mid):
        wx.Dialog.__init__(self, parent) 
            
        self.InitUI(mid)
        self.SetTitle(u'添加新鼠吗？')
        self.Fit()
        self.Center()
        p = self.GetPosition()
        self.Move(p+wx.Point(0, -100))
                
    def InitUI(self, mid):

        panel = wx.Panel(self)        
        
        color = 'STEEL BLUE'        
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)
        
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st1 = wx.StaticText(panel, label=u'鼠 ')
        mid = wx.StaticText(panel, label=mid)
        mid.SetForegroundColour(color)
        st2 = wx.StaticText(panel, label=u' 不存在，是否添加？')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(mid, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        hbox.Add(st2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        extra = (5 if os.name == 'posix' else 10)
        box.Add(hbox, 1, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)        
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_app = wx.Button(panel, -1, u'添加')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_app, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)
        b_app.SetDefault()
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnApply, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnClose, b_can)
                
    def OnClose(self, evt):
        self.addnew = False
        self.Close()
        
    def OnApply(self, evt):
        self.addnew = True
        self.Close()


class QuitDialog(wx.Dialog):
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)
        
        self.flag = 0
        self.InitUI()
        self.SetTitle(u'退出程序')
        self.Fit()
        self.Center()
        p = self.GetPosition()
        self.Move(p+wx.Point(0, -100))
                
    def InitUI(self):

        panel = wx.Panel(self)               
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)
        
        sb = wx.StaticBox(panel, label='')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st1 = wx.StaticText(panel, label=u'即将退出程序，是否保存更改？')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(st1, 1, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        extra = (5 if os.name == 'posix' else 10)
        box.Add(hbox, 1, wx.EXPAND|wx.ALL, extra)
        if os.name == 'posix':
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 10)
        else:
            vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)        
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        b_no = wx.Button(panel, -1, u'不保存')
        b_app = wx.Button(panel, -1, u'保存')
        b_can = wx.Button(panel, -1, u'取消')
        hbox.Add(b_no, 0, wx.EXPAND|wx.LEFT, 10)
        hbox.Add(wx.StaticText(panel, -1, '', size=(30, -1)))
        hbox.Add(b_app, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        hbox.Add(b_can, 0, wx.EXPAND|wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.BOTTOM, 10)
        b_app.SetDefault()
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnNo, b_no)
        self.Bind(wx.EVT_BUTTON, self.OnSave, b_app)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, b_can)
    
    def OnNo(self, evt):
        self.flag = -1
        self.Close()
                
    def OnCancel(self, evt):
        self.flag = 0
        self.Close()
        
    def OnSave(self, evt):
        self.flag = 1
        self.Close()

        
if __name__ == '__main__':

    class Example(wx.Frame):
        
        def __init__(self, parent, title):
        
            wx.Frame.__init__(self, parent, title=title)
                
            self.InitUI()
            self.Fit()
            self.Centre()
            self.Show()
                    
        def InitUI(self):
            
            panel = wx.Panel(self)
            vbox = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(vbox)
            
            click = wx.Button(self, -1, u'点击')
            vbox.Add(click, 0, wx.EXPAND|wx.ALL, 50)
            
            self.Bind(wx.EVT_BUTTON, self.OnClick, click)
    
        def OnClick(self, evt):        
            md = MoveDialog(None, title=u'移动鼠 AX11')
            md.ShowModal()
            md.Destroy()

    app = wx.App()
    Example(None, title=u'对话框例子')
    app.MainLoop()
    
    
