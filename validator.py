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
        
        if self.flag == 0: # 0: int only; 1: mid; 2: cid; 3: mid or none            
            for x in val:
                if x not in string.digits:
                    return False
        elif self.flag == 1:
            try:
                if [x for x in val[:2] if x not in string.ascii_uppercase] or \
                   [x for x in val[2:] if x not in string.digits]:
                    return False
            except:
                return False
        elif self.flag == 2:
            parts = var.split('-')
            if (len(parts) == 2) and (not parts[1]):
                return False
        elif self.flag == 3:
            try:
                if [x for x in val[:2] if x not in string.ascii_uppercase] or \
                   [x for x in val[2:] if x not in string.digits]:
                    return False
            except:
                if val != ' ':
                    return False
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if self.flag == 0:
            tc = self.GetWindow()
            var = tc.GetValue()
            if self.ifHouse(var, key):
                event.Skip()
                return
        elif self.flag == 1:
            tc = self.GetWindow()
            var = tc.GetValue()
            if self.ifMid(var, key):
                event.Skip()
                return
        elif self.flag == 2:
            tc = self.GetWindow()
            var = tc.GetValue()
            if self.ifCid(var, key):
                event.Skip()
                return
        elif self.flag == 3:
            tc = self.GetWindow()
            var = tc.GetValue()
            if self.ifMidPlus(var, key):
                event.Skip()
                return                
        if not wx.Validator_IsSilent():
            wx.Bell()
        return

    def ifHouse(self, var, key):
        if var:
            return (chr(key) in string.digits)
        else:
            return (chr(key) in '123456789')
        
    def ifMid(self, var, key):
        if len(var) >= 2:
            return (chr(key) in string.digits)
        else:
            return (chr(key) in string.ascii_uppercase)

    def ifMidPlus(self, var, key):
        if len(var) >= 2:
            return (chr(key) in string.digits)
        elif not var:
            return (chr(key) in string.ascii_uppercase+' ')
        elif var == ' ':
            return False
        else:
            return (chr(key) in string.ascii_uppercase)
            
    def ifCid(self, var, key):
        if (len(var.split('-')) == 1) and var and (var != '1'):
            return (chr(key) in string.digits+'-')
        elif not var:
            return (chr(key) in '123456789')
        else:
            return (chr(key) in string.digits)
            
            