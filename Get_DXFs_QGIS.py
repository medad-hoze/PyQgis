import os


def convert_bytes(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.lf %s" % (num,x)
        num /= 1024.0

				
def file_size(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return convert_bytes(file_info.st_size)
    else:
        return 'no file found'


def Cheak_if_exists(dxf_path,value_to_check,add_to_map = True):
        dxf_output_filename = os.path.splitext(os.path.basename(dxf_path))[0]
        dxf_vl = QgsVectorLayer(dxf_path, dxf_output_filename+'_temp', 'ogr')
        if add_to_map:
            if dxf_vl.isValid() == True:
                    registry.addMapLayer(dxf_vl)


        layer_check = []
        for feature in dxf_vl.getFeatures():
                if feature['Layer'] == value_to_check:
                        layer_check.append(feature['Layer'])

        print (len(layer_check))
        return len(layer_check)




def Create_Mask(vl,in_put_layer,data_list = []):

    pr      = vl.dataProvider()
    filter_ = QgsVectorLayer(in_put_layer, "polygon", "ogr")

    e = filter_.extent()

    x_max = e.xMaximum()
    x_min = e.xMinimum()
    y_min = e.yMinimum()
    y_max = e.yMaximum()

    fet   = QgsFeature()

    coords  = [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min), (x_min, y_min)]   
    polygon = QgsGeometry.fromPolygonXY( [[ QgsPointXY( pair[0], pair[1] ) for pair in coords ]] ) 
    fet.setGeometry(polygon)
    fet.setAttributes(data_list)
    pr.addFeatures([fet])

    vl.updateExtents()
    
    
def Get_list_of_layers(Folder,ends_with):
    list_shp = []
    for root, dirs, files in os.walk(Folder):
        for file in files:
            if file.endswith(ends_with):
                list_shp.append(root + '\\' +file)
    return list_shp
    
    
def Create_mask_layer():
    vl = QgsVectorLayer(str('Polygon?crs='+'2039'), "polygon", "memory")
    pr      = vl.dataProvider()
    # add fields
    pr.addAttributes([QgsField("name", QVariant.String),\
                      QgsField("PATH", QVariant.String),\
                      QgsField("SIZE", QVariant.String),\
                      QgsField("COUNT", QVariant.String),\
                      QgsField("ID",  QVariant.Int)])
    vl.updateFields() # tell the vector layer to fetch changes from the provid
    return vl
#  #  #    S T A R T   #  #  #

Folder = r'C:\Users\Administrator\Desktop\medad\uni_ariel\lessons\lesson2_data\data\data_dxf'

dxfs         = Get_list_of_layers(Folder,'.dxf')
vl           = Create_mask_layer()

ID = 1
for dxf_ in dxfs:
    print (dxf_)
    COUNT        = Cheak_if_exists(dxf_,'M2200',False)
    dxf          = dxf_ + '|layername=entities|geometrytype=Line'
    data_list    = [dxf,dxf_,file_size(dxf_),COUNT,ID]
    Create_Mask(vl,dxf,data_list)
    
    ID += 1



QgsProject.instance().addMapLayer(vl)
