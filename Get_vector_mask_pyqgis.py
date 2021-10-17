import os


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
    
    
def Get_fcs_shps(Folder):
    list_shp = []
    for root, dirs, files in os.walk(Folder):
        for file in files:
            if file.endswith(".shp"):
                list_shp.append(root + '\\' +file)
    return list_shp
    
    
def Create_mask_layer():
    vl = QgsVectorLayer(str('Polygon?crs='+'2039'), "polygon", "memory")
    pr      = vl.dataProvider()
    # add fields
    pr.addAttributes([QgsField("name", QVariant.String),
                      QgsField("age",  QVariant.Int)])
    vl.updateFields() # tell the vector layer to fetch changes from the provid
    return vl
#  #  #    S T A R T   #  #  #

Folder = r'C:\Users\Administrator\Desktop\medad\layers\SHP_Files'

shps         = Get_fcs_shps(Folder)
vl           = Create_mask_layer()


for shp in shps:
    print (shp)
    data_list    = [shp,20]
    Create_Mask(vl,shp,data_list)


QgsProject.instance().addMapLayer(vl)