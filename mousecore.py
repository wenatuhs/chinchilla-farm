# -*- coding: utf-8 -*-
# Filename: mousecore.py


import time, datetime
import types
import cPickle
import json
import os


class YearId(object):
    """ 年份编号类

    主要作用是自动生成新出生鼠的鼠号前缀。 """
    dict = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'H',
        7: 'J',
        8: 'K',
        9: 'L',
        10: 'M',
        11: 'N',
        12: 'P',
        13: 'R',
        14: 'S',
        15: 'T',
        16: 'V',
        17: 'X',
        18: 'Z'
    }
    origin = 2011

    @classmethod
    def get_code(cls, date):
        if date:
            year = int(date.split('-')[0])
        else:
            year = int(time.strftime("%Y", time.localtime(time.time())))
        return cls.dict[(year - cls.origin) % 19]

    
class SymList(object):
    """ 符号列表

    主要作用是给出各种属性的可取值。 """
    try:
        with open('prefs.json', 'r') as f:
            prefs = json.load(f)
        glist = prefs['gender']
        llist = prefs['level']
        clist = prefs['color']
        slist = prefs['status']
        nlist = prefs['title']
        blist = prefs['custom']
        alist = prefs['age']
    except:
        prefs = {}
        glist = prefs['gender'] = [u"公", u"母"]
        llist = prefs['level'] = [u"无分级", u"种鼠 A", u"种鼠 B", u"种鼠 C", 'A', 'B', 'C']
        clist = prefs['color'] = []
        slist = prefs['status'] = [u"正常", u"已售", u"死亡"]
        nlist = prefs['title'] = [u"枫丹龙猫管理系统", u"鼠列表", u'新鼠出生', u'鼠厂总览']
        blist = prefs['custom'] = []
        alist = prefs['age'] = [60, 210]
        with open('prefs.json', 'w') as f:
            json.dump(prefs, f, sort_keys=False, indent=4, separators=(',', ': '))

    @classmethod
    def add(cls, item):
        with open('prefs.json', 'r') as f:
            prefs = json.load(f)
        prefs[item[0]].append(item[1])
        with open('prefs.json', 'w') as f:
            json.dump(prefs, f, sort_keys=False, indent=4, separators=(',', ': '))
        SymList.glist = prefs['gender']
        SymList.llist = prefs['level']
        SymList.clist = prefs['color']
        SymList.slist = prefs['status']
        SymList.nlist = prefs['title']
        SymList.blist = prefs['custom']
        SymList.alist = prefs['age']
        
    @classmethod
    def adds(cls, items):
        with open('prefs.json', 'r') as f:
            prefs = json.load(f)
        prefs[items[0]] += items[1:]
        with open('prefs.json', 'w') as f:
            json.dump(prefs, f, sort_keys=False, indent=4, separators=(',', ': '))
        SymList.glist = prefs['gender']
        SymList.llist = prefs['level']
        SymList.clist = prefs['color']
        SymList.slist = prefs['status']
        SymList.nlist = prefs['title']
        SymList.blist = prefs['custom']
        SymList.alist = prefs['age']


class Mouse(object):
    """ 鼠类（龙猫类）

    有 id，gender，color 和 mother 等属性，比较重要的有：
    id 是鼠号，独一无二；
    mother 和 father 是鼠的父母的鼠号；
    cage 是鼠目前所在笼的笼号；
    status 是鼠的状态（健康，生病，死亡，已售出）；
    level 是鼠的级别（种鼠，A，B，C 档宠物鼠/皮鼠）。"""

    def __init__(self, id, gender, color, mother, father, borndate=None):
        object.__init__(self)
        # unchangeable
        self.id = id
        self.gender = gender
        self.color = color
        self.mother = mother
        self.father = father
        if borndate:
            self.borndate = borndate
        else:
            today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            self.borndate = today
        # changeable
        self.deathdate = None
        self.cage = None
        self.status = u'正常' # G(ood), I(ll), D(eath), S(old)
        self.level = u'无分级' # S(eed)A, SB, SC, A, B, C
        self.comment = u''

    def age(self, date=None):
        """ 根据出生日期计算年龄

        从出生日期 borndate 到 date 为止，若不给 date，则到计算当天为止。
        返回天数。 """
        bd = time.strptime(self.borndate, "%Y-%m-%d")
        if self.status == u'死亡':
            dd = time.strptime(self.deathdate, "%Y-%m-%d")
            return (datetime.datetime(dd[0], dd[1], dd[2]) - datetime.datetime(bd[0], bd[1], bd[2])).days
        elif date:
            d = time.strptime(date, "%Y-%m-%d")
            return (datetime.datetime(d[0], d[1], d[2]) - datetime.datetime(bd[0], bd[1], bd[2])).days
        else:
            return (datetime.datetime.now() - datetime.datetime(bd[0], bd[1], bd[2])).days

    def die(self, date=None):
        """ 设置鼠的死亡状态

        将鼠的状态 status 设置为死亡（D），并记录死亡日期 deathdate。
        返回操作是否成功，若操作前鼠的状态已经是 D，则返回失败（0）。 """
        if self.status == u'死亡':
            return 0
        elif date:
            self.deathdate = date
        else:
            self.deathdate = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.status = u'死亡'
        return 1


class Cage(object):
    """ 鼠笼类

    有 id，house，channel 和 guest 四个属性：
    id 是笼号；
    house 是笼所在的鼠房，一般与 id 相关；
    channel 是笼的通道开闭状态，一般只有种鼠笼通道才是打开的；
    guest 是目前笼中所有鼠的鼠号。 """

    def __init__(self, id):
        object.__init__(self)
        self.id = id
        parts = self.id.split('-')
        if len(parts) == 1:
            self.house = '1'
        else:
            self.house = parts[0]
        self.channel = u'开' # C(lose) or O(pen)
        self.guest = []
        
    def switch(self):
        if self.channel == u'开':
            self.channel = u'关'
            return u'笼 ' + self.id + u' 的通道成功关闭！'
        else:
            self.channel = u'开'
            return u'笼 ' + self.id + u' 的通道成功打开！'

    def check_in(self, id):
        """ 入住登记

        将鼠号 id 加入房客 guest 列表中。 """
        if id in self.guest:
            return u"鼠 " + id + u" 已经在笼 " + self.id + u" 中!"
        else:
            self.guest.append(id)
            return 1

    def check_out(self, id):
        """ 离房登记

        将鼠号 id 从房客 guest 列表中删除。 """
        if id in self.guest:
            self.guest.remove(id)
            return 1
        else:
            return u"鼠 " + id + u" 不在笼 " + self.id + u" 中!"


class Record(object):
    """ 记录类

    有 date，type，content 和 comment 四个属性：
    date 是记录的日期，默认为记录创建当天；
    type 是记录的种类，比如移动记录，生产记录，死亡记录等等；
    content 是记录的内容，一般是一个关键词列表，根据记录种类的不同而不同；
    comment 是备注。 """

    def __init__(self, type, content, date=None, comment=None):
        object.__init__(self)
        self.type = type
        self.content = content
        self.comment = comment
        if date:
            self.date = date
        else:
            today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            self.date = today

    def show(self):
        s = ''
        if self.type == 'M':
            s = u"移动：鼠 %s 从笼 %s 中移动至笼 %s 中。" % tuple(self.content)
        elif self.type == 'S':
            s = u"出售：卖出鼠 %s 至「%s」。" % (u'、'.join(self.content[1:]), self.content[0])
        elif self.type == 'D':
            s = u"死亡：鼠 %s 于笼 %s 中死亡。" % tuple(self.content)
        elif self.type == 'B':
            s = u"出生：鼠 %s 于笼 %s 中出生。" % tuple(self.content)
        elif self.type == 'C':
            s = u"级别：鼠 %s 的级别变为「%s」。" % tuple(self.content)
        elif self.type == 'N':
            s = u"笔记：鼠 %s 的附注更新为「%s」。" % tuple(self.content)
        if self.comment:            
            s = s + u"\n备注：" + self.comment
        return s


class Farm(object):
    """ 鼠厂类

    有 cages，mouses 和 logs 三个属性：
    cages 是所有笼的字典，key 是笼号，value 是笼；
    mouses 是所有鼠的字典，key 是鼠号，value 是鼠；
    logs 是日志，key 是日期，value 是记录（Record）的列表。 """
    filename = './database/farm.db'

    def __init__(self, filename=None):
        """ 初始化

        自动载入鼠厂信息。
        若不指定文件名 filename，将载入名为 'farm.db' 的文件。
        若文件不存在，则自动创建新的数据库（但不写入硬盘）。 """
        object.__init__(self)
        if not filename:
            filename = self.__class__.filename
        try:
            if not os.path.isdir('./database'):
                os.mkdir('./database')
            f = file(filename, 'rb')
            self.cages, self.mouses, self.logs = cPickle.load(f)
            f.close()
            self.info = u"数据库已载入。"
        except IOError:
            self.cages = {}
            self.mouses = {}
            self.logs = {}
            self.info = u"找不到数据库文件，重置数据库！"
        self.sep = '\n'+'-'*16+'\n'

    def load(self, filename=None):
        """ 载入鼠厂数据

        若不指定文件名 filename，将载入名为 'farm.db' 的文件。
        若文件不存在，则自动创建新的数据库（但不写入硬盘）。 """
        if not filename:
            filename = self.__class__.filename
        try:
            f = file(filename, 'rb')
            self.cages, self.mouses, self.logs = cPickle.load(f)
            f.close()
            return u"数据库已载入。"
        except IOError:
            return u"找不到数据库文件，载入失败！"

    def save(self, filename=None):
        """ 保存鼠厂数据（重要！）

        若不指定文件名 filename，保存的文件将以 'farm.db' 命名。
        若文件已存在则覆盖。 """
        if not filename:
            filename = self.__class__.filename
        try:
            f = file(filename, 'wb')
            cPickle.dump((self.cages, self.mouses, self.logs), f)
            f.close()
            return u"更改已保存。"
        except IOError:
            return u"保存失败！"

    def backup(self, filename=None):
        """ 备份鼠厂数据（重要！）

        备份文件将以 'farm_YYYY-MM-DD.db' 命名。
        若文件已存在则覆盖。 """
        if not filename:
            filename = self.__class__.filename
        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        filename = filename[:-3] + "_" + today + ".db"
        try:
            f = file(filename, 'wb')
            cPickle.dump((self.cages, self.mouses, self.logs), f)
            f.close()
            return u"数据库备份成功。"
        except IOError:
            return u"数据库备份失败！"

    def check_mouse(self, id):
        """ 检查某只鼠是否已经在鼠厂中

        id 是鼠号。
        存在的话返回 True。 """
        current = self.mouses.keys()
        return (id in current)

    def check_cage(self, id):
        """ 检查某个笼是否已经在鼠厂中

        id 是笼号。
        存在的话返回 True。 """
        current = self.cages.keys()
        return (id in current)

    def new_cages(self, ids):
        """ 在鼠厂（Farm）中新建若干笼

        ids 是笼号的列表而不是笼的列表。
        将在 Farm.cages 中添加若干新笼。 """
        fail = []
        for id in ids:
            if self.check_cage(id):
                fail.append(u"笼 " + id + u" 已存在！")
            else:
                cage = Cage(id)
                self.cages[id] = cage
        if fail:
            return ' '.join(fail)
        else:
            return u'添加鼠笼成功！'

    def add_mouses(self, mouses):
        """ 向鼠厂（Farm）中加入若干鼠

        mouses 是鼠的列表而不是鼠号的列表。
        将在 Farm.mouses 中添加若干鼠。 """
        info = []
        for mouse in mouses:
            if mouse.id:
                if self.check_mouse(mouse.id):
                    info.append(u"鼠 " + mouse.id + u" 已存在！")
                else:
                    self.mouses[mouse.id] = mouse
                    info.append(u"成功添加鼠 " + mouse.id + u'！')
            else:
                info.append(u"鼠必须有鼠号，请输入鼠号后再添加！")
        return info

    def insert(self, records):
        """ 插入若干条日志记录

        records 为记录 Record 的列表，注意插入是按照列表次序进行的。
        若若干条 Record 的日期相同，则他们将被合并到同一天的日志中。 """
        for record in records:
            if not (record.date in self.logs.keys()):
                self.logs[record.date] = []
            self.logs[record.date].append(record)

    def move(self, mid, cid, date=None, comment=None):
        """ 在笼子间移动鼠

        给出鼠号 mid，目标笼号 cid，移动日期 date 以及备注 comment，就可以实现移动。
        若原笼为 None（对应出生或引进）或目标笼为 None（对应死亡或卖出）或移动不成立，则移动不会产生日志记录；否则会被记录在日志中。
        移动成功后，鼠会自动设定新笼号。 """
        # 鼠存在
        if self.check_mouse(mid):
            m = self.mouses[mid]
            # 鼠已死亡
            if m.status == u'死亡':
                return u"鼠 " + mid + u" 已死亡，移动无效！"
            # 鼠已卖出
            elif m.status == u'已售':
                return u"鼠 " + mid + u" 已出售，移动无效！"
            # 鼠原笼和目标笼都存在
            elif m.cage and self.check_cage(cid):
                # 原笼和目标笼一致
                if m.cage == cid:
                    return u"鼠 " + mid + u" 已在笼 " + cid + u" 中，无需移动！"
                else:
                    record = Record('M', [mid, m.cage, cid], date, comment) # 鼠号, 原笼号, 目标笼号
                    self.insert([record])
                    self.cages[m.cage].check_out(mid)
                    self.cages[cid].check_in(mid)
                    m.cage = cid
                    return u"移动成功！"
            # 原笼存在但目标笼不存在
            elif m.cage:
                # 目标笼若不是 None
                if cid:
                    return u"笼 " + cid + u" 不存在！"
                else:
                    self.cages[m.cage].check_out(mid)
                    m.cage = None
                    return u"移动成功！"
            # 如果原笼不存在（则一定为 None）且目标笼存在
            elif self.check_cage(cid):
                self.cages[cid].check_in(mid)
                m.cage = cid
                return u"移动成功！"
            elif cid:
                return u"笼 " + cid + u" 不存在！"
            else:
                return u"鼠 " + mid + u" 目前无笼，请将之移动到一个有效笼子中！"
        else:
            return u"鼠 " + mid + u" 不存在！"

    def new_id(self, date):
        """ 产生新鼠 id

        返回 mid """
            
        pre = 'A' + YearId.get_code(date)
        maxnum = max([int(k[2:]) for k in self.mouses.keys() if k.startswith(pre)] + [0])
        mid = pre + str(maxnum + 1)        
        return mid

    def pre_born(self, cid, date):
        """ 出生检验

        给出笼号 cid，来看是否可能出生一只新鼠。
        若不可能，返回 [False]；
        否则，返回 [True, father, mother] """
        try:
            if self.cages[cid].house != '1':
                num = int(cid.split('-')[1])
            else:
                num = int(cid)            
            # 找到父亲
            c1 = num - ((num - 1) % 5)
            if self.cages[cid].house != '1':
                pre = self.cages[cid].house + '-'
            else:                
                pre = ''
            flag = 0
            for i in range(5):
                fcid = pre + str(c1+i)
                try:
                    guests = self.cages[fcid].guest
                except:
                    guests = None
                for g in guests:
                    if (self.mouses[g].gender == u'公') \
                        and (self.mouses[g].age(date) > SymList.alist[1]):
                        father = g
                        flag = 1
                        break
                if flag:
                    break
            # 找到母亲
            for g in self.cages[cid].guest:
                if (self.mouses[g].gender == u'母') and (self.mouses[g].age(date) > SymList.alist[1]):
                    mother = g
                    break
            if self.cages[cid].channel == u'关':
                if self.mouses[father].cage != cid:
                    return [False]
            else:
                if self.cages[self.mouses[father].cage].channel == u'关':
                    return [False]
            return [True, father, mother]
        except:
            return [False]

    def born(self, cid, mid, gender, color, date=None, comment=None):
        """ 出生登记

        给出笼号 cid，新鼠号 mid，性别 gender，颜色 color，出生日期 date 以及备注 comment，来使一只新鼠出生。
        新鼠号若为 None，则自动根据出生年份分配一个新鼠号；
        出生日期若不给，则默认为录入当天出生。 """
        try:
            if self.cages[cid].house != '1':
                num = int(cid.split('-')[1])
            else:
                num = int(cid)
            # 找到父亲
            c1 = num - ((num - 1) % 5)
            if self.cages[cid].house != '1':
                pre = self.cages[cid].house + '-'
            else:                
                pre = ''
            flag = 0
            for i in range(5):
                fcid = pre + str(c1+i)
                try:
                    guests = self.cages[fcid].guest
                except:
                    guests = None
                for g in guests:
                    if (self.mouses[g].gender == u'公') \
                        and (self.mouses[g].age(date) > SymList.alist[1]):
                        father = g
                        flag = 1
                        break
                if flag:
                    break
            # 找到母亲
            for g in self.cages[cid].guest:
                if (self.mouses[g].gender == u'母') and (self.mouses[g].age(date) >= 150):
                    mother = g
                    break
            # 验证笼的开关状态
            if self.cages[cid].channel == u'关':
                if self.mouses[father].cage != cid:
                    return u"出生失败！请检查笼 " + cid + u" 所在笼组的状态。"
            else:
                if self.cages[self.mouses[father].cage].channel == u'关':
                    return u"出生失败！请检查笼 " + cid + u" 所在笼组的状态。"
            # 是否自动产生鼠号
            if not mid:
                mid = self.new_id(date)
            # 出生
            m = Mouse(mid, gender, color, mother, father, date)
            self.add_mouses([m])
            self.move(mid, cid, date) # 这步移动不会产生记录
            m.cage = cid
            record = Record('B', [mid, cid], date, comment) # 鼠号，出生笼号
            self.insert([record])
            return u"出生成功！"
        except:
            return u"出生失败！请检查笼 " + cid + u" 所在笼组的状态。"

    def sell(self, mids, custom, date=None, comment=None):
        """ 批量出售鼠

        mids 是待出售鼠的鼠号列表。
        custom 是买家
        只有当该列表中至少有一只鼠出售成功时，才产生一条出售记录。 """
        sold = []
        info = []
        for mid in mids:
            if self.move(mid, None, date, comment) == u"移动成功！":
                self.mouses[mid].status = u'已售'
                sold.append(mid)
                info.append(u"成功出售鼠 " + mid + u"！")
            else:
                info.append(u"出售鼠 " + mid + u" 失败！请检查鼠 " + mid + u" 及其所在笼的有效性。")
        if sold:
            record = Record('S', [custom]+sold, date, comment) # 买家名字及卖出的所有鼠号列表
            self.insert([record])
        return info

    def burn(self, mid, date=None, comment=None):
        """ 鼠不幸死亡

        mid 是死亡鼠的鼠号。
        当该鼠死亡时，产生一条死亡记录。 """
        try:
            cid = self.mouses[mid].cage
        except KeyError:
            pass
        if self.move(mid, None, date, comment) == u"移动成功！":
            self.mouses[mid].die(date)
            record = Record('D', [mid, cid], date, comment)
            self.insert([record])
            return u"死亡成功！"
        else:
            return u"死亡失败！请检查鼠 " + mid + u" 及其所在笼的有效性。"

    def change(self, mid, prop, date=None, comment=None):
        """ 更改鼠的状态及级别

        mid 是待更改鼠的鼠号，prop 是更改目标值（'G', 'I', 'SA', 'SB', 'SC', 'A', 'B', 'C' 中的一个）。
        当目标状态与原状态不同时，且鼠没有死亡或售出，产生一条状态更改记录。 """
        try:
            m = self.mouses[mid]
            if m.status != u'死亡' and m.status != u'已售':
                if prop in SymList.slist:
                    if m.status != prop:
                        m.status = prop
                        record = Record('C', [mid, prop], date, comment) # 改变的鼠号及改变后的属性值
                        self.insert([record])
                        return u"更改状态成功！"
                    else:
                        return u"鼠 " + mid + u" 的状态已经是 " + prop + u"，无需更改！"
                elif prop in SymList.llist:
                    if m.level != prop:
                        m.level = prop
                        record = Record('C', [mid, prop], date, comment) # 改变的鼠号及改变后的属性值
                        self.insert([record])
                        return u"更改级别成功！"
                    else:
                        return u"鼠 " + mid + u" 的级别已经是 " + prop + u"，无需更改！"
                else:
                    return u"属性值 " + prop + u" 不存在！请重新考察待更改的属性及属性值。"
            elif m.status == u'死亡':
                return u"鼠 " + mid + u" 已死亡，不能更改其状态！"
            else:
                return u"鼠 " + mid + u" 已卖出，不能更改其状态！"
        except:
            return u"更改状态失败！请检查鼠 " + mid + u" 及其所在笼的有效性。"
            
    def comment(self, mid, note, date=None, comment=None):
        """ 更新鼠的附注

        mid 是待更改鼠的鼠号，note 是附注。
        当鼠没有死亡或售出，且附注有更改时，产生一条附注更新记录。 """
        try:
            m = self.mouses[mid]
            if m.status != u'死亡' and m.status != u'已售':
                if (m.comment or None) == (note or None):
                    return u"新附注和原附注相同，无需更改！"
                else:
                    m.comment = note
                    record = Record('N', [mid, note], date, comment) # 鼠号，附注
                    self.insert([record])
                    return u"更改附注成功！"
            elif m.status == u'死亡':
                return u"鼠 " + mid + u" 已死亡，不能更新其附注！"
            else:
                return u"鼠 " + mid + u" 已卖出，不能更新其附注！"
        except:
            return u"更新附注失败！请检查鼠 " + mid + u" 及其所在笼的有效性。"
            
    def getSiblings(self, mid):
        try:
            m = self.mouses[mid]
            bd = m.borndate
            mother = m.mother
            siblings = [m.id for m in self.mouses.values() if (m.borndate == bd)\
                        and (m.mother == mother) and (m.id != mid)]
            return siblings
        except KeyError:
            return False
        
    def getBornRecords(self, mid, flag=0):
        try:
            gender = self.mouses[mid].gender
            bornrecords = {}
            borncount = {}
            male = SymList.glist[0]
            if gender == male:
                for m in self.mouses.values():
                    if m.father == mid:
                        if not (m.borndate in bornrecords.keys()):
                            bornrecords[m.borndate] = []
                            borncount[m.borndate] = [0, 0]
                        bornrecords[m.borndate].append(m.id)
                        borncount[m.borndate][(0 if m.gender == male else 1)] += 1
            else:
                for m in self.mouses.values():
                    if m.mother == mid:
                        if not (m.borndate in bornrecords.keys()):
                            bornrecords[m.borndate] = []
                            borncount[m.borndate] = [0, 0]
                        bornrecords[m.borndate].append(m.id)
                        borncount[m.borndate][(0 if m.gender == male else 1)] += 1
            if not flag:
                return bornrecords
            else:
                if bornrecords:
                    def combine(count):
                        return str(count[0]) + 'M ' + str(count[1]) + 'F'
                    def beautier(value):
                        s = ''
                        value = sorted(value, key=lambda e: int(e[2:]))
                        for i in range(len(value)):
                            s += ('\n\t' + value[i]) if (not i % 3) else ('  ' + value[i])
                        return s
                    recs = sorted(bornrecords.items(), key=lambda e: e[0])
                    return self.sep.join([key + ': ' + combine(borncount[key])\
                                          + beautier(value) for key, value in recs])
                else:
                    return u'无生育记录'
        except KeyError:
            return False
        
    def getMoveRecords(self, mid, flag=0):
        try:
            self.mouses[mid]
            moverecords = {}
            for date, records in self.logs.items():
                trace = []
                for r in records:
                    if (r.type == 'M') and (r.content[0] == mid):
                        trace.append(r.content[1:])
                    elif (r.type == 'B') and (r.content[0] == mid):
                        trace.append([None, r.content[1]])
                    elif (r.type == 'D') and (r.content[0] == mid):
                        trace.append([r.content[1], None])
                    elif (r.type == 'S') and (mid in r.content[1:]):
                        trace.append([None, None])
                if trace:
                    moverecords[date] = trace
            if not flag:
                return moverecords
            else:
                if moverecords:
                    def combine(moves):
                        output = []
                        for m in moves:
                            if m[0] and m[1]:
                                output.append(m[0] + ' --> ' + m[1])
                            elif (not m[0]) and m[1]:
                                output.append(u'出生' + ' --> ' + m[1])
                            elif m[0] and (not m[1]):
                                output.append(m[0] + ' --> ' + u'死亡')
                            else:
                                output.append(u'出售')
                        return output
                    recs = sorted(moverecords.items(), key=lambda e: e[0])
                    return self.sep.join([key + ': \n\t' + u'\n\t'.join(combine(value))\
                                          for key, value in recs])
                else:
                    return u'无移动记录'
        except KeyError:
            return False

version = 1.01