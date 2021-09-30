# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction,QMessageBox


from qgis.core import QgsVectorLayer,QgsFeatureRequest,QgsVectorFileWriter
import os
import pandas as pd
import processing

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .combineData_dialog import Combine_DataDialog
import os.path


class Combine_Data:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Combine_Data_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Combine data')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):

        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Combine_Data', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):


        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/combineData/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Combine data'),
                action)
            self.iface.removeToolBarIcon(action)



    def run(self):

        def select_by_id(self,layer,select_id):
            layer.select(select_id)

            selection = layer.selectedFeatures()

            for feat in selection:
                print (feat['GUSH_NUM'])
                
            return selection
            
        def handle_csv(csv_path):

            df      = pd.read_csv(csv_path,encoding = "utf-8")
            df      = df[['TALAR_NUM', 'TALAR_YEAR', 'GUSH_NUM', 'GUSH_SUFFIX','DESCRIPTION','GUSH_STATUS','LOCALITY_NAME','REG_MUN_NAME',"ORDERER"]]

            list_          = df["GUSH_NUM"].values.tolist()
            list_to_filter = ','.join(str(i) for i in list_)[0:-1]
            
            return df,list_to_filter


        def Filter_by_field_name(layer_path,list_to_filter,out_put):

            layer   = QgsVectorLayer(layer_path, "sub_gush_all", "ogr")
            layer.selectByExpression("\"GUSH_NUM\" in ("+list_to_filter+")")

            _writer      = QgsVectorFileWriter.writeAsVectorFormat(layer,out_put,"utf-8",layer.crs(),"ESRI Shapefile",onlySelected = True)
            
            return out_put
            
            
        def spatial_join(filter_path,mun_path,fnout,fields_to_copy = []):
            processing.run("native:joinbynearest",\
            {'INPUT':filter_path,\
            'INPUT_2':mun_path,\
            'FIELDS_TO_COPY':fields_to_copy,\
            'DISCARD_NONMATCHING':True,\
            'PREFIX':'',\
            'NEIGHBORS':1,\
            'MAX_DISTANCE':0,\
            'OUTPUT':fnout})

            # iface.addVectorLayer(fnout, '', 'ogr')
            
            return fnout


        def createFolder(dic):
            try:
                if not os.path.exists(dic):
                    os.makedirs(dic)
            except OSError:
                print ("Error Create dic")
            return dic
            
        def Get_Name_to_None(REG_MUN_NA,REG_MUN_NAME):
            return REG_MUN_NA if REG_MUN_NA != u' ' else REG_MUN_NAME
            
            
        def dict_():
            dict_1 = {'TALAR_ID':'מספר_תלר','TALAR_NUM':'מספר_תצר','TALAR_YEAR':'שנת_תצר','GUSH_NUM':'גוש','MUNI_HEB':'גבולות_שיפוט',\
                    'REG_MUN_NA':'ועדה','SETL_NAME':'שם_ישוב','GUSH_SUFFIX':'תת_גוש','DESCRIPTION':'סטאטוס_תצר','GUSH_STATUS':'סטאטוס_גוש',\
                    'LOCALITY_NAME':'שם_ישוב','REG_MUN_NAME':'שם_אזור_מונציפלי','SETL_NAME':'שם_ישוב','NAME_HEB':'שם_בעברית','ORDERER':'מזמין_עבודה',\
                    'NAFA1':'נפה','SUG_MUNI':'סוג_מוניציפאלי','FIRST_Nafa':'נפה','Muni_Heb':'גבולות_שיפוט'}
            return dict_1

        """Run method that performs all the real work"""

        if self.first_start == True:
            self.first_start = False
            self.dlg = Combine_DataDialog()


        self.dlg.show()
        result = self.dlg.exec_()
        if result:

            # layer_path     = r"C:\Users\Administrator\Desktop\medad\python\Work\for_dariel\Data\sub_gush_all.shp"
            # mun_path       = r"C:\Users\Administrator\Desktop\medad\python\Work\for_dariel\Data\muni_il.shp"
            # csv_path       = r"C:\Users\Administrator\Desktop\medad\python\Work\for_dariel\files\2021-07.csv"

            lyr_gush   = self.dlg.btn_gush.currentLayer()
            layer_path = str(lyr_gush.dataProvider().dataSourceUri())

            lyr_muni   = self.dlg.btn_muni.currentLayer()
            mun_path   = str(lyr_muni.dataProvider().dataSourceUri())

            lyr_csv    = self.dlg.btn_csv.currentLayer()
            csv_path   = str(lyr_csv.dataProvider().dataSourceUri())

            csv_date   = os.path.basename(csv_path)
            folder     = createFolder(r'C:\temp')

            filter_path   = folder + '\\' + 'filter_gush4.shp'
            spatial_merge = folder + '\\' + 'spatial_merge4.shp'


            out_put = self.dlg.lineEdit.text()
            if not out_put: 
                out_put       = folder + '\\' + 'Result_' + csv_date


            #QMessageBox.information(self.dlg, "Message", str(lyr_gush.sourceName()))
            QMessageBox.information(self.dlg, "Message", str(lyr_gush.dataProvider().dataSourceUri()))

            df,list_to_filter = handle_csv(csv_path)

            Filter_by_field_name(layer_path,list_to_filter,filter_path)
            spatial_join        (filter_path,mun_path,spatial_merge,["FIRST_Nafa","Sug_Muni","Muni_Heb","FIRST_Nafa","Sug_Muni","Muni_Heb"])

            merge_lyr   = QgsVectorLayer(spatial_merge, "filter_path", "ogr")

            # merge_lyr.setProviderEncoding(u'UTF-8')
            # merge_lyr.dataProvider().setEncoding(u'UTF-8')

            dict_1  = dict_()
            data    = []
            request = QgsFeatureRequest()
            request.setFilterExpression("\"GUSH_NUM\" in ("+list_to_filter+")")
                
            data = [[lyr['GUSH_NUM'],lyr['GUSH_SUFFI'],lyr["REG_MUN_NA"],\
                    lyr["FIRST_Nafa"],lyr["SUG_MUNI"],lyr["Muni_Heb"]]\
                    for lyr in merge_lyr.getFeatures(request)]
                    
            df_shp               = pd.DataFrame(data = data, columns = ["GUSH_NUM","GUSH_SUFFIX","REG_MUN_NA","FIRST_Nafa","SUG_MUNI","Muni_Heb"])

            df['GUSH_SUFFIX']     = df    ['GUSH_SUFFIX'].fillna(value=0)
            df_shp['GUSH_SUFFIX'] = df_shp['GUSH_SUFFIX'].fillna(value=0)

            result                = df.merge(df_shp, how = 'left', left_on=['GUSH_NUM','GUSH_SUFFIX'], right_on=['GUSH_NUM','GUSH_SUFFIX'])


            result['REG_MUN_NA'] = result[['REG_MUN_NA','REG_MUN_NAME']].apply(lambda x:Get_Name_to_None(x[0],x[1]),axis = 1)

            result               = result.drop(['REG_MUN_NAME'], axis = 1)

            result               = result.rename(columns=dict_1)

            result.to_csv            (out_put,encoding='ISO-8859-8')
                

            pass
