# -*- coding: utf-8 -*-
# Filename: main.py


import wx
import os
import wx.dataview as dv
import json

from mousecore import *
import mousecard
import cagecard
import mouselist
import overview
import addnew
import modify
import addnewcage
import newborn
import addlog
import showlog
import dialog


class SearchPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)        
        self.frame = parent

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.extra = extra = (0 if os.name == 'posix' else 5)
        
        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        self.search.ShowSearchButton(1)
        self.search.ShowCancelButton(1)
        vbox.Add(self.search, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
        
        sb = wx.StaticBox(self, label=u'日常')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.overview = b1 = wx.Button(self, label=u"全局视图")
        self.mouselist = b2 = wx.Button(self, label=u"鼠列表")
        self.born = b3 = wx.Button(self, label=u"出生登记")
        self.tobemoved = b4 = wx.Button(self, label=u"待移动鼠")
        b4.Disable()
        gs = wx.GridSizer(2, 2, 5, 5)
        gs.AddMany([(b1, 1, wx.EXPAND),
                    (b2, 1, wx.EXPAND),
                    (b3, 1, wx.EXPAND),
                    (b4, 1, wx.EXPAND)])
        box.Add(gs, 1, wx.EXPAND|wx.ALL, extra)
        vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        sb = wx.StaticBox(self, label=u'录入')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.addc = b2 = wx.Button(self, label=u"添加笼")
        self.add = b1 = wx.Button(self, label=u"添加鼠")
        self.mod = b3 = wx.Button(self, label=u"修改鼠")
        self.mod.Hide()
        gs = wx.FlexGridSizer(2, 2, 5, 5)
        gs.AddMany([(b1, 1, wx.EXPAND),
                    (b2, 1, wx.EXPAND),
                    (b3, 1, wx.EXPAND)])
        box.Add(gs, 1, wx.EXPAND|wx.ALL, extra)
        vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
        
        sb = wx.StaticBox(self, label=u'日志')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.showlog = b1 = wx.Button(self, label=u"浏览日志")
        self.addlog = b2 = wx.Button(self, label=u"添加日志")
        gs = wx.GridSizer(1, 2, 5, 5)
        gs.AddMany([(b1, 1, wx.EXPAND),
                    (b2, 1, wx.EXPAND)])
        box.Add(gs, 1, wx.EXPAND|wx.ALL, extra)
        vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        sb = wx.StaticBox(self, label=u'数据库')
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.save = b1 = wx.Button(self, label=u"保存")
        self.backup = b2 = wx.Button(self, label=u"备份")
        self.load = b3 = wx.Button(self, label=u"读取")
        gs = wx.GridSizer(2, 2, 5, 5)
        gs.AddMany([(b1, 1, wx.EXPAND),
                    (b3, 1, wx.EXPAND),
                    (b2, 1, wx.EXPAND)])
        box.Add(gs, 1, wx.EXPAND|wx.ALL, extra)
        vbox.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
        vbox.Add((-1, 10))
        
        self.Bind(wx.EVT_BUTTON, self.OnOverview, self.overview)
        self.Bind(wx.EVT_BUTTON, self.OnMouseList, self.mouselist)
        self.Bind(wx.EVT_BUTTON, self.OnNewBorn, self.born)
        self.Bind(wx.EVT_BUTTON, self.OnAddNew, self.add)
        self.Bind(wx.EVT_BUTTON, self.OnAddNewCage, self.addc)
        self.Bind(wx.EVT_BUTTON, self.OnAddLog, self.addlog)
        self.Bind(wx.EVT_BUTTON, self.OnShowLog, self.showlog)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.save)
        self.Bind(wx.EVT_BUTTON, self.OnBackup, self.backup)
        self.Bind(wx.EVT_BUTTON, self.OnLoad, self.load)
        self.Bind(wx.EVT_BUTTON, self.OnModify, self.mod)
                
    def OnOverview(self, evt):
        overview.Overview(self.frame, self.frame.farm)
        
    def OnMouseList(self, evt):
        mouselist.MouseList(self.frame, self.frame.farm)
        
    def OnNewBorn(self, evt):
        newborn.NewBorn(self.frame, self.frame.farm)
        
    def OnAddNew(self, evt):
        addnew.AddNew(self.frame, self.frame.farm)
    
    def OnModify(self, evt):
        modify.Modify(self.frame, self.frame.farm)
        self.mod.Hide()
        self.frame.Fit()
        
    def OnAddNewCage(self, evt):
        addnewcage.AddNewCage(self.frame, self.frame.farm)
        
    def OnAddLog(self, evt):
        addlog.AddLog(self.frame, self.frame.farm)
        
    def OnShowLog(self, evt):
        showlog.ShowLog(self.frame, self.frame.farm)        
        
    def OnSave(self, evt):
        feedback = self.frame.farm.save()
        self.frame.statusbar.SetStatusText(feedback, 0)
        
    def OnBackup(self, evt):
        feedback = self.frame.farm.backup()
        self.frame.statusbar.SetStatusText(feedback, 0)
        
    def OnLoad(self, evt):
        ld = dialog.LoadDialog(self)
        ld.ShowModal()
        if ld.database:
            feedback = self.frame.farm.load(ld.database)
            self.frame.statusbar.SetStatusText(feedback, 0)
            for child in self.frame.GetChildren():
                child.Update()
        ld.Destroy()


class Search(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)

        self.farm = Farm()
        if (not SymList.clist) and self.farm.mouses:
            color = ['color'] + list(set([m.color for m in self.farm.mouses.values()]))
            SymList.adds(color)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(self.farm.info)
        self.SetTitle(SymList.nlist[0]+' V'+unicode(version))
        self.InitUI()
        self.Fit()
        self.Center()
        if os.name != 'posix':
            ld = dialog.LoginDialog(self)
            ld.ShowModal()
            ld.Destroy()
        else:
            self.Show()

    def InitUI(self):
        self.panel = panel = SearchPanel(self)
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.panel.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearch, self.panel.search)
        
        exitID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnClose,id=exitID)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('Q'), exitID)])
        self.SetAcceleratorTable(accel_tbl)

    def OnSearch(self, event):
        keyword = self.panel.search.GetValue()
        if keyword == 'ZMKM':
            self.panel.mod.Show()
            self.Fit()
            self.statusbar.SetStatusText(u'解锁「修改鼠」选项成功！')
        elif keyword[:1].isupper():
            try:
                self.farm.mouses[keyword]
                mc = mousecard.MouseCard(self, keyword, self.farm)
            except:
                ad = dialog.AddNewDialog(self, keyword)
                ad.ShowModal()
                if ad.addnew:
                    addnew.AddNew(self, self.farm, keyword)
                ad.Destroy()
        else:
            try:
                self.farm.cages[keyword]
                cc = cagecard.CageCard(self, keyword, self.farm)
            except:
                if keyword:
                    self.statusbar.SetStatusText(u'无匹配项！请输入有效鼠号、笼号或密令')
        self.panel.search.Clear()
#                ad = dialog.AddNewCageDialog(self, keyword)
#                ad.ShowModal()
#                if ad.addnew:
#                    addnew.AddNew(self, self.farm, keyword)
#                ad.Destroy()

    def OnClose(self, evt):
        qd = dialog.QuitDialog(self)
        qd.ShowModal()
        flag = qd.flag
        qd.Destroy()
        if flag == 1:
            self.farm.save()
            self.Destroy()
        elif flag == -1:
            self.Destroy()
            
#    def OnHide(self, evt):
#        self.Hide()
#        
#    def OnShow(self, evt):
#        self.Show()

    def check(self, username, password):
        if username == 'admin' and password == '841017':
            return True
        else:
            return False


if __name__ == '__main__':

    app = wx.App()
    m = Search(None)
    app.MainLoop()
