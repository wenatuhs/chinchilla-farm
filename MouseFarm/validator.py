# -*- coding: utf-8 -*-


import  string
import  wx


class MouseValidator(wx.PyValidator):        
    def __init__(self, flag=None, pyVar=None):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return MouseValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        
        if self.flag == 0: # int only
            for x in val:
                if x not in string.digits:
                    return False
        else:
            pass
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if self.flag == 0 and chr(key) in string.digits:
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
        return