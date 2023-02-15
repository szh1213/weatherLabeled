# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:28:07 2022

@author: xiaoqingtech01
"""

import sys, os, json, pickle, datetime, re
from PySide6.QtCore import (QCoreApplication, Signal, QPoint, Qt,QRectF,
                             )
from PySide6.QtWidgets import (QApplication, QMainWindow, QCheckBox,
                               QRadioButton, QHBoxLayout, QGraphicsPixmapItem,
                               QGraphicsScene, QGraphicsView, QButtonGroup,
                                QFileDialog,QFrame, QTableView,QSplitter,
                                QAbstractItemView, QHeaderView, QDockWidget)
from PySide6.QtGui import ( QPixmap, QFont, QIcon,QColor,QBrush,
                           QStandardItemModel,QStandardItem,QPen)
from ui_weather import Ui_MainWindow as weather_mainwindow

from Crypto.Cipher import AES
from math import log as mathlog


def center2cor(rects):
    m = [[0 for i in range(5)]for j in range(len(rects))]
    for i,rect in enumerate(rects):
        m[i][2] = rect[2]-rect[4]/2
        m[i][4] = rect[4]
            
    if len(rects)==3:
        step = (m[1][4]+m[2][4])/10
        for i in range(10):
            m.append((0,0,m[1][2]+step*(10+i*2),0,step*2,0))
        
    return sorted(m,key=lambda x:x[2])


def getMarks():
    mark = {}
    _CALI_PATH = os.path.join(r'\\Xqdata\沈正豪\雪深识别', 'resources/data')
    try:
        for dat in os.listdir(_CALI_PATH):
            if dat.endswith('.pkl'):
                tmp=pickle.load(open(_CALI_PATH+'/'+dat,'rb'))
                for p in tmp:
                    st = re.findall('([0-9]{5})_20', p)[0]
                    date = re.findall('([0-9]{14})', p)[0]
                    if len(tmp[p]) not in [3,13]:continue
                    if st not in mark:mark[st]={}
                    tmp[p] = sorted(tmp[p], key=lambda x:x[2])
                    mark[st][int(date)] = center2cor(tmp[p])
    except:
        pass
    return mark


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


'''
AES对称加密算法
'''
# 需要补位，str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += b'\x00'
    return value  # 返回bytes
# 加密方法
def encrypt(bbb):
    aes = AES.new(add_to_16(b'yyds'*4), AES.MODE_ECB)  # 初始化加密器
    encrypt_aes = aes.encrypt(add_to_16(bbb))  # 先进行aes加密
    #encrypted = base64.encodebytes(encrypt_aes) # 执行加密并转码返回bytes
    return encrypt_aes
# 解密方法
def decrypt(bbb):
    aes = AES.new(add_to_16(b'yyds'*4), AES.MODE_ECB)  # 初始化加密器
    #base64_decrypted = base64.decodebytes(bbb)  # 优先逆向解密base64成bytes
    decrypted_text = aes.decrypt(bbb)  # 执行解密密并转码返回str
    return decrypted_text[:-16]+decrypted_text[-16:].replace(b'\x00',b'')

class PhotoViewer(QGraphicsView):
    photoClicked = Signal(QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        DashLinePen = QPen(Qt.darkGreen, 1, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        DotLinePen = QPen(Qt.green, 1, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin)
        self.picInfo = self._scene.addText('',QFont('KaiTi',50,Qt.green))
        self.picInfo.setPos(100,100)
        self.lines = [self._scene.addLine(0,-10,2560,-10,DashLinePen)]
        self.lines += [self._scene.addLine(0,-10,2560,-10,DotLinePen)for i in range(13)]
        self.lines += [self._scene.addLine(0,-10,2560,-10,DashLinePen)for i in range(3)]
        self.lines += [self._scene.addLine(0,-10,2560,-10,DotLinePen)for i in range(10)]
        
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)
        self.setVisible(False)
        self.setMinimumWidth(300)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.setVisible(True)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.position().toPoint()))
        super(PhotoViewer, self).mousePressEvent(event)
    
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = weather_mainwindow()
        self.ui.setupUi(self)
        _translate = QCoreApplication.translate
        cloud = '''none-无云
        Cb-积雨云
        Tcu-浓积云
        Cu-淡积云
        Fc-碎积云
        St-层云
        Fs-碎层云
        Sc-层积云
        Ns-雨层云
        Fn-碎雨云
        As-高层云
        Ac-高积云
        Cs-卷层云
        Cc-卷积云
        Ci-卷云
        other-其他'''.split()
        self.QBTNG = QButtonGroup()
        self.ACOVERG = QButtonGroup()
        self.HCOVERG = QButtonGroup()
        self.MCOVERG = QButtonGroup()
        self.LCOVERG = QButtonGroup()
        self.picDir = None
        self.pics = []
        self.mark = getMarks()
        self.fileTable = QTableView()
        self.fileSim = QStandardItemModel()
        self.fileTable.setModel(self.fileSim )
        self.fileTable.clicked.connect(self.clickedlist)
        self.fileTable.setMinimumWidth(100)
        self.fileTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.hisTable = QTableView()
        self.hisSim = QStandardItemModel()
        self.hisTable.setModel(self.hisSim )
        self.hisTable.clicked.connect(self.clickedlist)
        self.hisTable.setMinimumWidth(100)
        self.hisTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.picLables = {
            'cloud':{},
            'cover':{},
            'deep':{},
            'snow':{},
            'ice':{},
            'frost':{},
            'dew':{},
            'glaze':{},
            'sori':{},
            'vis':{},
            }
        self.historyLabels = {
            'cloud':{},
            'cover':{},
            'deep':{},
            'snow':{},
            'ice':{},
            'frost':{},
            'dew':{},
            'glaze':{},
            'sori':{},
            'vis':{},
            }
        self.historyPath = r'\\Xqdata\公用\标注文件'
        self.picSeed = -1
        self.picNum = 0
        self.lastKey = None
        self.lastValue = None
        self.operateTime = {
            'cloud':{},
            'cover':{},
            'deep':{},
            'snow':{},
            'ice':{},
            'frost':{},
            'dew':{},
            'glaze':{},
            'sori':{},
            'vis':{}
            }
        
        self.loadHistory()
        from socket import gethostname
        self.auth = gethostname()
        self.lastSaveTime = self._now()
        
        def styleChange(btn):
            def f():
                if btn.text() == 'macOS风':
                    self.setStyleSheet(open(resource_path('qss/ubuntu.qss')).read())
                    btn.setText(QCoreApplication.translate("MainWindow",
                                                           'ubuntu风', None))
                else:
                    self.setStyleSheet(open(resource_path('qss/macOS.qss')).read())
                    btn.setText(QCoreApplication.translate("MainWindow",
                                                           'macOS风', None))
            return f
        
        self.ui.styleBTN.clicked.connect(styleChange(self.ui.styleBTN))
        self.ui.styleBTN.setToolTip('切换界面风格')
        
        
        def shortCutChange(btn):
            def f():
                if btn.text() == 'a-z':
                    self.ui.yesRBTN.setShortcut('1')
                    self.ui.noRBTN.setShortcut('2')
                    self.ui.otherRBTN.setShortcut('3')
                    btn.setText(QCoreApplication.translate("MainWindow",
                                                           '0-9', None))
                else:
                    self.ui.yesRBTN.setShortcut('y')
                    self.ui.noRBTN.setShortcut('n')
                    self.ui.otherRBTN.setShortcut('o')
                    btn.setText(QCoreApplication.translate("MainWindow",
                                                           'a-z', None))
                self.ui.yesRBTN.setToolTip(self.ui.yesRBTN.shortcut().toString())
                self.ui.noRBTN.setToolTip(self.ui.noRBTN.shortcut().toString())
                self.ui.otherRBTN.setToolTip(self.ui.otherRBTN.shortcut().toString())
            return f
        
        self.ui.shortcutBTN.clicked.connect(shortCutChange(self.ui.shortcutBTN))
        self.ui.shortcutBTN.setToolTip('切换快捷方式')
        
        
        self.cloudCBs = [QCheckBox(self.ui.cloudTab) for i in cloud]
        for b,c in zip(self.cloudCBs[:8],cloud[:8]):
            b.setText(_translate("MainWindow", c.split('-')[1], None))
            self.ui.cloudVLL.addWidget(b)
            b.clicked.connect(self.makeCloudCBfun(b))
            
        for b,c in zip(self.cloudCBs[8:],cloud[8:]):
            b.setText(_translate("MainWindow", c.split('-')[1], None))
            self.ui.cloudVLR.addWidget(b)
            b.clicked.connect(self.makeCloudCBfun(b))
        
            
        self.ACoverRBs = [QRadioButton(self.ui.coverTab) for i in range(10)]
        self.HCoverRBs = [QRadioButton(self.ui.coverTab) for i in range(10)]
        self.MCoverRBs = [QRadioButton(self.ui.coverTab) for i in range(10)]
        self.LCoverRBs = [QRadioButton(self.ui.coverTab) for i in range(10)]
        
        for i,r in enumerate(self.ACoverRBs):
            if i<9:
                r.setText(_translate("MainWindow", str(i), None))
            else:
                r.setText(_translate("MainWindow", str(-1), None))
            self.ui.ACoverVL.addWidget(r)
            r.clicked.connect(self.makeCoverRBfun(r, 'total'))
            self.ACOVERG.addButton(r)
        for i,r in enumerate(self.HCoverRBs):
            if i<9:
                r.setText(_translate("MainWindow", str(i), None))
            else:
                r.setText(_translate("MainWindow", str(-1), None))
            self.ui.HCoverVL.addWidget(r)
            r.clicked.connect(self.makeCoverRBfun(r, 'high'))
            self.HCOVERG.addButton(r)
        for i,r in enumerate(self.MCoverRBs):
            if i<9:
                r.setText(_translate("MainWindow", str(i), None))
            else:
                r.setText(_translate("MainWindow", str(-1), None))
            self.ui.MCoverVL.addWidget(r)
            r.clicked.connect(self.makeCoverRBfun(r, 'middle'))
            self.MCOVERG.addButton(r)
        for i,r in enumerate(self.LCoverRBs):
            if i<9:
                r.setText(_translate("MainWindow", str(i), None))
            else:
                r.setText(_translate("MainWindow", str(-1), None))
            self.ui.LCoverVL.addWidget(r)
            r.clicked.connect(self.makeCoverRBfun(r, 'low'))
            self.LCOVERG.addButton(r)
        
        
        self.QBTNG.addButton(self.ui.noRBTN)
        self.QBTNG.addButton(self.ui.yesRBTN)
        self.QBTNG.addButton(self.ui.otherRBTN)
        
        self.ui.qTab.currentChanged.connect(self.initRBs)
        
        self.curimg = QPixmap()
        
        
        self.viewer = PhotoViewer(self)
        
        self.spliter = QSplitter(Qt.Horizontal)
        self.pglayout = QHBoxLayout()
        
        
        self.spliter.addWidget(self.viewer)
        self.spliter.addWidget(self.fileTable)
        
        self.pglayout.addWidget(self.spliter)
        
        self.ui.openBTN.clicked.connect(self.openPicDir)
        self.ui.openBTN.setToolTip('打开文件夹ctrl+o')
        self.ui.openBTN.setShortcut('ctrl+o')
        self.ui.loadBTN.clicked.connect(self.loadPicLables)
        self.ui.loadBTN.setToolTip('载入历史记录ctrl+l')
        self.ui.loadBTN.setShortcut('ctrl+l')
        self.ui.saveBTN.clicked.connect(self.savePicLabelsToPath)
        self.ui.saveBTN.setToolTip('保存标注结果ctrl+s')
        self.ui.saveBTN.setShortcut('ctrl+s')
        self.ui.setLastDeepBTN.clicked.connect(self.setLastValue)
        self.ui.setLastDeepBTN.setToolTip('设置为上一张图的状态ctrl+r')
        self.ui.setLastDeepBTN.setShortcut('space')
        
        self.ui.lastBTN.clicked.connect(self.setLastPic)
        self.ui.nextBTN.clicked.connect(self.setNextPic)
        self.ui.lastBTN.setShortcut('a')
        self.ui.lastBTN.setToolTip('上一张a')
        self.ui.nextBTN.setShortcut('d')
        self.ui.nextBTN.setToolTip('下一张d')
        self.ui.noRBTN.clicked.connect(self.makeRBfun(self.ui.noRBTN))
        self.ui.noRBTN.setShortcut('2')
        self.ui.yesRBTN.clicked.connect(self.makeRBfun(self.ui.yesRBTN))
        self.ui.yesRBTN.setShortcut('1')
        self.ui.otherRBTN.clicked.connect(self.makeRBfun(self.ui.otherRBTN))
        self.ui.otherRBTN.setShortcut('3')
        
        self.ui.deepLE.returnPressed.connect(self.enterVis)
    
        self.initRBs(0)    
        
     
        self.hisDock = QDockWidget(self.tr("历史标签"), self)
        self.hisDock.setFeatures(QDockWidget.DockWidgetFloatable | 
                          QDockWidget.DockWidgetMovable | Qt.WindowMinimizeButtonHint)
        self.hisDock.setWidget(self.hisTable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.hisDock)
        
        
        self.fileDock = QDockWidget(self.tr("文件列表"), self)
        self.fileDock.setFeatures(QDockWidget.DockWidgetFloatable | 
                          QDockWidget.DockWidgetMovable | Qt.WindowMinimizeButtonHint)
        self.fileDock.setWidget(self.fileTable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.fileDock)
     
    
    def initRBs(self, index):
        ctab = self.ui.qTab.currentWidget()
        if not ctab.layout():
            ctab.setLayout(self.pglayout)
            
        self.QBTNG.setExclusive(False)
        self.ACOVERG.setExclusive(False)
        self.HCOVERG.setExclusive(False)
        self.MCOVERG.setExclusive(False)
        self.LCOVERG.setExclusive(False)
    
        #self.ui.setLastDeepBTN.setVisible(False)
        self.ui.noRBTN.setChecked(False)
        self.ui.noRBTN.setVisible(index>3)
        self.ui.yesRBTN.setChecked(False)
        self.ui.yesRBTN.setVisible(index>3)
        self.ui.otherRBTN.setChecked(False)
        self.ui.otherRBTN.setVisible(index>3)
        self.QBTNG.setExclusive(True)
        self.ACOVERG.setExclusive(True)
        self.HCOVERG.setExclusive(True)
        self.MCOVERG.setExclusive(True)
        self.LCOVERG.setExclusive(True)
        
        for c in self.cloudCBs:
            c.setVisible(index==0)
        
        self.ui.ACoverLB.setVisible(index==1)
        self.ui.HCoverLB.setVisible(index==1)
        self.ui.MCoverLB.setVisible(index==1)
        self.ui.LCoverLB.setVisible(index==1)
        
        for r in self.ACoverRBs:
            r.setVisible(index==1)
        
        for r in self.HCoverRBs:
            r.setVisible(index==1)
        
        for r in self.MCoverRBs:
            r.setVisible(index==1)
        
        for r in self.LCoverRBs:
            r.setVisible(index==1)
        
        if index==2:
            self.ui.deepVS.valueChanged.connect(self.deepfun)
            self.ui.deepVS.setMinimum(-1)
            self.ui.deepVS.setMaximum(99)
            self.ui.deepVS.setSingleStep(1)
            self.ui.deepVS.setPageStep(1)
        elif index==3:
            self.ui.deepVS.sliderMoved.connect(self.visfun)
            self.ui.deepVS.setMinimum(0)
            self.ui.deepVS.setMaximum(990000)
            self.ui.deepVS.setSingleStep(10000)
            self.ui.deepVS.setPageStep(10000)
        
        self.ui.deepVS.setVisible(index in [2,3])
        self.ui.deepLE.setVisible(index in [2,3])
        self.ui.visLB.setVisible(index in [3])
        self.showPicLabel()
        if self.picSeed >=0:
            picName = self.pics[self.picSeed]
            for wea in self.picLables:
                if picName in self.picLables[wea]:
                    del self.picLables[wea][picName]
        
        
    def openPicDir(self):
        
        self.picDir = QFileDialog.getExistingDirectory(self,'打开图片文件夹')
        self.picDir = os.path.normpath(self.picDir)
        if os.path.exists(self.picDir):
            self.pics.clear()
            for a,b,c in os.walk(self.picDir):
                for p in c:
                    if p.endswith('.jpg'):
                        self.pics.append(os.path.normpath(os.path.join(a,p)))
                        
        
        self.pics = sorted(set(self.pics))
        self.picNum = len(self.pics)
        if self.picNum:
            self.picSeed = 0
            self.setPic(0)
        else:
            self.picSeed = -1
        self.initRBs(self.ui.qTab.currentIndex())
        try:
            cat,pics,seed,lbs = pickle.load(open(os.path.expanduser('~')+
                                        '/.weatherLabeled.pkl','rb'))
           
            if cat == self.picDir and pics == self.pics:
                self.picSeed = seed
                self.picLables = lbs
                self.setPic(self.picSeed)
                
        except:
            pass
        
        self.fileSim.clear()
        self.fileSim.setHorizontalHeaderLabels(['地址'])
        for i,p in enumerate(self.pics):
            self.fileSim.appendRow(QStandardItem(p))
            
        self.showPicLabel()
        self.fileTable.resizeColumnsToContents()
        self.hisTable.resizeColumnsToContents()
        self.spliter.setStretchFactor(0,6)
        self.spliter.setStretchFactor(1,4)
        # self.fileTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.fileTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hisTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    
    def savePicLabels(self, path='labels.xq'):
    
        result = {}
        for wea in self.picLables:
            result[wea] = {}
            for p in self.picLables[wea]:
                name = os.path.split(p)[1]
                date = re.findall('([0-9]{12})', name)
                st = re.findall('([0-9]{5})_20', name)
                ca = re.findall('[^0-9]([0-9]{2}-[0-9]{2})[^0-9]', name)
                if date and st and ca:
                    st, date, ca = st[0],date[0],ca[0]
                    name = (st, date, ca)
                    if name in self.historyLabels[wea]:
                        val = self.historyLabels[wea][name][-1][0]
                        if self.picLables[wea][p] == val:
                            continue
                                
                try:
                    clock = self.operateTime[wea][p]
                    result[wea][p] = (self.picLables[wea][p], self.auth, clock)
                except:
                    pass
                
        with open(path,'wb')as f:
            txt = json.dumps(result, ensure_ascii=False, 
                               indent=4, separators=(',', ': '))
            entxt = encrypt(pickle.dumps(txt))
            f.write(entxt)
            
        strfNow = self._now()
        name = strfNow+'_'+self.auth+'.json'
        jsonPath = os.path.join(self.historyPath,name)
        name = self.lastSaveTime+'_'+self.auth+'.json'
        lastPath = os.path.join(self.historyPath,name)
        self.lastSaveTime = strfNow
        try:
            if os.path.exists(lastPath):os.remove(lastPath)
            with open(jsonPath,'w')as f:
                f.write(json.dumps(result, ensure_ascii=False, 
                                   indent=4, separators=(',', ': ')))
        except:
            pass
       
    
    def savePicLabelsToPath(self):
        path = QFileDialog.getSaveFileName(self,'保存到','.',"标签文件 (*.xq)")
        try:
            self.savePicLabels(path[0])
        except:
            pass
    
    
    def loadPicLables(self):
        path = QFileDialog.getOpenFileName(self,'打开','.',"标签文件 (*.xq *.json)")
        file = path[0]
        if file.endswith('.json'):
            with open(path[0])as f:
                self.picLables = json.load(f)
        elif path[0].endswith('.xq'):
            with open(path[0], 'rb')as f:
                detxt = decrypt(f.read())
                one = json.loads(pickle.loads(detxt))
        else:
            return
        for wea in one:
            for p in one[wea]:
                name = os.path.split(p)[1]
                date = re.findall('([0-9]{12})', name)
                st = re.findall('([0-9]{5})_20', name)
                ca = re.findall('[^0-9]([0-9]{2}-[0-9]{2})[^0-9]', name)
                if date and st and ca:
                    st, date, ca = st[0],date[0],ca[0]
                    name = (st, date, ca)
                if name not in self.historyLabels[wea]:
                    self.historyLabels[wea][name] = []
                item = [self._is_lb_auth_time(one[wea][p]) ,file]
                self.historyLabels[wea][name].append(item)
                self.historyLabels[wea][name].sort(key=lambda x:x[1])
                  
                self.operateTime[wea][p] = '0'*14
                
        self.showPicLabel()
        print('load ',path[0])
            
            
    def showPicLabel(self):
        self.hisSim.clear()
        self.hisSim.setHorizontalHeaderLabels(['标签'])
        wea = self.ui.qTab.currentWidget().objectName()[:-3]
        self.QBTNG.setExclusive(False)
        self.ACOVERG.setExclusive(False)
        self.HCOVERG.setExclusive(False)
        self.MCOVERG.setExclusive(False)
        self.LCOVERG.setExclusive(False)
        if self.pics:
            picPath = self.pics[self.picSeed]
            picName = os.path.split(picPath)[1]
            date = re.findall('([0-9]{12})', picName)
            st = re.findall('([0-9]{5})_20', picName)
            ca = re.findall('[^0-9]([0-9]{2}-[0-9]{2})[^0-9]', picName)
            if date and st and ca:
                st, date, ca = st[0],date[0],ca[0]
                picName = (st, date, ca)
            self.operateTime[wea][picPath] = self._now()
            
        else:
            for btn in self.cloudCBs:
                btn.setChecked(False)
            for btn in self.ACoverRBs:
                btn.setChecked(False)
                
            for btn in self.HCoverRBs:
                btn.setChecked(False)
                
            for btn in self.MCoverRBs:
                btn.setChecked(False)
                
            for btn in self.LCoverRBs:
                btn.setChecked(False)
                
            for btn in [self.ui.noRBTN,self.ui.yesRBTN,self.ui.otherRBTN]:
                btn.setChecked(False)
            self.ui.deepVS.setValue(-1)
            self.ui.deepLE.setText('-1')
            self.QBTNG.setExclusive(True)
            self.ACOVERG.setExclusive(True)
            self.HCOVERG.setExclusive(True)
            self.MCOVERG.setExclusive(True)
            self.LCOVERG.setExclusive(True)
            return 0
            
        if picPath in self.picLables[wea]:
            picLb = self.picLables[wea][picPath]
            if wea == 'cloud':
                for btn in self.cloudCBs:
                    btn.setChecked(btn.text() in picLb)
            elif wea == 'cover':
                if 'total' in picLb:
                    for btn in self.ACoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['total'])
                if 'high' in picLb:
                    for btn in self.HCoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['high'])
                if 'middle' in picLb:
                    for btn in self.MCoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['middle'])
                if 'low' in picLb:
                    for btn in self.LCoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['low'])
            elif wea == 'deep':
                self.deepfun(picLb)
            elif wea == 'vis':
                vis, _ = picLb
                cm = -1 if vis<10 else (mathlog(vis,10)-1)*300000
                self.visfun(cm)
            else:
                for btn in [self.ui.noRBTN,self.ui.yesRBTN,self.ui.otherRBTN]:
                    btn.setChecked(btn.text() == picLb)
            
                
        elif picName in self.historyLabels[wea]:
            picLb,_from = self.historyLabels[wea][picName][-1]
            _from = 'from:'+_from
            self.viewer.picInfo.setPlainText(_from)
            if wea == 'cloud':
                for btn in self.cloudCBs:
                    btn.setChecked(btn.text() in picLb)
            elif wea == 'cover':
                if 'total' in picLb:
                    for btn in self.ACoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['total'])
                if 'high' in picLb:
                    for btn in self.HCoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['high'])
                if 'middle' in picLb:
                    for btn in self.MCoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['middle'])
                if 'low' in picLb:
                    for btn in self.LCoverRBs:
                        btn.setChecked(int(btn.text()) == picLb['low'])
            elif wea == 'deep':
                self.deepfun(picLb)
            elif wea == 'vis':
                vis, _ = picLb
                cm = -1 if vis<10 else (mathlog(vis,10)-1)*300000
                self.visfun(cm)
            else:
                for btn in [self.ui.noRBTN,self.ui.yesRBTN,self.ui.otherRBTN]:
                    btn.setChecked(btn.text() == picLb)
        else:
            for btn in self.cloudCBs:
                btn.setChecked(False)
            for btn in self.ACoverRBs:
                btn.setChecked(False)
            for btn in self.HCoverRBs:
                btn.setChecked(False)
            for btn in self.MCoverRBs:
                btn.setChecked(False)
            for btn in self.LCoverRBs:
                btn.setChecked(False)
            for btn in [self.ui.noRBTN,self.ui.yesRBTN,self.ui.otherRBTN]:
                btn.setChecked(False)
            self.ui.deepVS.setValue(-1)
            self.ui.deepLE.setText('-1')
            
        picInfo = ''
        if picName in self.historyLabels[wea]:
            picLb,_from = self.historyLabels[wea][picName][-1]
            picInfo += 'from:'+_from
            
            for item in self.historyLabels[wea][picName][::-1]:
                self.hisSim.appendRow(QStandardItem(str(item)))
            
        
        if wea == 'deep' and st in self.mark:
            station = st
            try:
                def f(x):
                    return abs(date-x)
                best = sorted(self.mark[station], key=f)[0]
                stmk = self.mark[station][best]
            except:
                best = sorted(self.mark[station], key=lambda x:-x)[0]
                stmk = self.mark[station][best]
            picInfo += ' '+str(best)
            d = (stmk[0][2]-stmk[1][2])/819
            for i in range(len(self.viewer.lines)-13):
                self.viewer.lines[i].setPos(0,
                    int((stmk[0][2]-d*65*i+d*i*(i-1)/2)*1440)+8)
            
            for i in range(14,len(self.viewer.lines)-1):
                self.viewer.lines[i].setPos(0,int(stmk[i-13][2]*1440)+8)
            
            self.viewer.lines[-1].setPos(0,int((stmk[12][2]+stmk[12][4])*1440)+8)
        else:
            for i in range(len(self.viewer.lines)):
                self.viewer.lines[i].setPos(0,-10)
        
            
        self.viewer.picInfo.setPlainText(picInfo)
        
        self.QBTNG.setExclusive(True)
        self.ACOVERG.setExclusive(True)
        self.HCOVERG.setExclusive(True)
        self.MCOVERG.setExclusive(True)
        self.LCOVERG.setExclusive(True)
        
        self.hisTable.resizeColumnsToContents()
        self.hisTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        
    def setPic(self, index):
        if not 0<=index<self.picNum:return
        self.curimg.load(self.pics[index])
        self.viewer.setPhoto(self.curimg)
        text = '进度：{}/{}   当前图片：{}'.format(index+1,self.picNum, 
                                           os.path.split(self.pics[index])[1])
        
        self.setWindowTitle(text)
        self.showPicLabel()
        
        
    def setLastPic(self):
        self.picSeed -= 1
        if self.picSeed<0:self.picSeed = self.picNum - 1
        self.setPic(self.picSeed)
        self.savePicLabels()
            
    
    def setNextPic(self):
        self.picSeed += 1
        if self.picSeed>=self.picNum:self.picSeed = 0
        self.setPic(self.picSeed)
        self.savePicLabels()
           
    
    # 添加云状多选
    def makeCloudCBfun(self, btn):
        wea = 'cloud'
        cloudName = btn.text()
        def f():
            if self.picSeed<0:return
            picName = self.pics[self.picSeed]
            if btn.isChecked():
                if picName not in self.picLables[wea]:
                    self.picLables[wea][picName] = []
                self.picLables[wea][picName].append(cloudName)
                
            elif picName in self.picLables[wea]:
                if cloudName in self.picLables[wea][picName]:
                    self.picLables[wea][picName].remove(cloudName)
                    
                if not self.picLables[wea][picName]:
                    del self.picLables[wea][picName]
                
            if picName in self.picLables[wea]:
                self.lastKey = (self.pics[self.picSeed], wea)
                self.lastValue = self.picLables[wea][picName]
            
        return f
    
    
    # 添加云量单选
    def makeCoverRBfun(self, btn, level):
        wea = 'cover'
        cloudNum = int(btn.text())
        def f():
            if self.picSeed<0:return
            picName = self.pics[self.picSeed]
            if btn.isChecked():
                if picName not in self.picLables[wea]:
                    self.picLables[wea][picName] = {}
                self.picLables[wea][picName][level] = cloudNum
                    
            elif picName in self.picLables[wea]:
                del self.picLables[wea][picName][level]
            
            if picName in self.picLables[wea]:
                self.lastKey = (self.pics[self.picSeed], wea)
                self.lastValue = self.picLables[wea][picName]
            
        return f
    

    # 添加其它天气
    def makeRBfun(self, btn):
        picClass = btn.text()
        def f():
            if self.picSeed<0:return
            wea = self.ui.qTab.currentWidget().objectName()[:-3]
            picName = self.pics[self.picSeed]
            if btn.isChecked():
                self.picLables[wea][picName] = picClass
            elif picName in self.picLables[wea]:
                del self.picLables[wea][picName]
                
            if picName in self.picLables[wea]:
                self.lastKey = (self.pics[self.picSeed], wea)
                self.lastValue = self.picLables[wea][picName]
            
        return f
        
        
    def deepfun(self,cm):
        self.ui.deepVS.setValue(cm)
        self.ui.deepLE.setText(str(cm))
        if self.picSeed<0:return
        picName = self.pics[self.picSeed]
        self.picLables['deep'][picName] = cm
        if cm!=-1:
            self.lastKey = (self.pics[self.picSeed], 'deep')
            self.lastValue = cm
        
            
    def visfun(self,cm):
        vis = int(10**(cm/300000+1))
        self.ui.deepVS.setValue(cm)
        self.ui.deepLE.setText(str(vis))
        if vis<800:
            self.ui.visLB.setText('50 米')
        elif vis<5000:
            self.ui.visLB.setText('100 米')
        elif vis<10000:
            self.ui.visLB.setText('1000 米')
        else:
            self.ui.visLB.setText('10KM')
            
            
        if self.picSeed<0:return
        picName = self.pics[self.picSeed]
        self.picLables['vis'][picName] = [vis,self.ui.visLB.text()]
        if cm!=-1:
            self.lastKey = (self.pics[self.picSeed], 'vis')
            self.lastValue = [vis,self.ui.visLB.text()]
        
        
    def enterVis(self):
        try:
            vis = int(self.ui.deepLE.text())
            cm = -1 if vis<10 else (mathlog(vis,10)-1)*300000
            self.visfun(cm)
        except:
            pass
        
        
    def setLastValue(self):
        wea = self.ui.qTab.currentWidget().objectName()[:-3]
        self.QBTNG.setExclusive(False)
        self.ACOVERG.setExclusive(False)
        self.HCOVERG.setExclusive(False)
        self.MCOVERG.setExclusive(False)
        self.LCOVERG.setExclusive(False)
        picLb = self.lastValue
        if wea == 'cloud':
            for btn in self.cloudCBs:
                btn.setChecked(btn.text() in picLb)
                
        elif wea == 'cover':
            if 'total' in picLb:
                for btn in self.ACoverRBs:
                    btn.setChecked(int(btn.text()) == picLb['total'])
            if 'high' in picLb:
                for btn in self.HCoverRBs:
                    btn.setChecked(int(btn.text()) == picLb['high'])
            if 'middle' in picLb:
                for btn in self.MCoverRBs:
                    btn.setChecked(int(btn.text()) == picLb['middle'])
            if 'low' in picLb:
                for btn in self.LCoverRBs:
                    btn.setChecked(int(btn.text()) == picLb['low'])
                
        elif wea == 'deep':
            self.deepfun(picLb)
        elif wea == 'vis':
            vis, _ = picLb
            cm = -1 if vis<10 else (mathlog(vis,10)-1)*300000
            self.visfun(cm)
        else:
            if picLb != None:
                for btn in [self.ui.noRBTN,self.ui.yesRBTN,self.ui.otherRBTN]:
                    btn.setChecked(btn.text() == picLb)
               
            
        self.QBTNG.setExclusive(True)
        self.ACOVERG.setExclusive(True)
        self.HCOVERG.setExclusive(True)
        self.MCOVERG.setExclusive(True)
        self.LCOVERG.setExclusive(True)
        wea = self.ui.qTab.currentWidget().objectName()[:-3]
        self.picLables[wea][self.pics[self.picSeed]] = picLb
        
        self.setNextPic()
        
        
    def clickedlist(self,qModelIndex):
        self.setPic(qModelIndex.row())
        self.picSeed = qModelIndex.row()
        
        
    def closeEvent(self, e):
        with open(os.path.expanduser('~')+'/.weatherLabeled.pkl','wb')as f:
            pickle.dump([self.picDir,self.pics,self.picSeed,self.picLables],f)
            
        self.savePicLabels()
        print('exit')
    
    
    def loadHistory(self):
        if not os.path.exists(self.historyPath):return 0
        for file in os.listdir(self.historyPath):
            if not file.endswith('.json'):continue
            try:
                with open(self.historyPath+'/'+file,'r')as f:
                    one = json.load(f, strict=False)
                for wea in one:
                    for p in one[wea]:
                        name = os.path.split(p)[1]
                        date = re.findall('([0-9]{12})', name)
                        st = re.findall('([0-9]{5})_20', name)
                        ca = re.findall('[^0-9]([0-9]{2}-[0-9]{2})[^0-9]', name)
                        if date and st and ca:
                            st, date, ca = st[0],date[0],ca[0]
                            name = (st, date, ca)
                        
                        if name not in self.historyLabels[wea]:
                            self.historyLabels[wea][name] = []
                        item = [self._is_lb_auth_time(one[wea][p]) ,file]
                        self.historyLabels[wea][name].append(item)
                        self.historyLabels[wea][name].sort(key=lambda x:x[1])
                        
            except Exception as e:
                print(e, file)
    
    
    def _now(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    
    def _is_lb_auth_time(self, val):
        if not isinstance(val, list):
            return val
        elif len(val)!=3 or not (isinstance(val[2], str) and len(val[2])==14):
            return val
        elif isinstance(val[0], list):
            return self._is_lb_auth_time(val[0])
        return val[0]
        
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet(open(resource_path('qss/macOS.qss')).read())
    window.setWindowIcon(QIcon(resource_path('img/logo.ico')))
    window.showMaximized()
    # window.setVisible(False)
    lbs=window.historyLabels
    sys.exit(app.exec())