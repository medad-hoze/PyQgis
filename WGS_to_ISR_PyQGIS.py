
import math

def Tran_WGS_to_ISR(longitude,latitude):

    def degreesToRadians(degrees):
        return degrees * math.pi / 180
    def pow2(x):
        return pow(x, 2)
    def pow3(x):
        return pow(x, 3)
    def pow4(x):
        return pow(x, 4)

    longitude       = degreesToRadians(longitude)
    latitude        = degreesToRadians(latitude)
    centralMeridian = degreesToRadians(35.2045169444444);  # central meridian of ITM projection
    k0              = 1.0000067;  # scale factor

    # Ellipsoid constants (WGS 80 datum)

    a    = 6378137      #equatorial radius
    b    = 6356752.3141 # polar radius
    e    = math.sqrt(1 - b*b/a/a);  ## eccentricity
    e1sq = e*e/(1-e*e)
    n    = (a-b)/(a+b)

    tmp = e*math.sin(latitude)
    nu  = a/math.sqrt(1 - tmp*tmp)

    ## Meridional arc length

    n3 = pow3(n)
    n4 = pow4(n)

    A0 = a*(1-n+(5*n*n/4)*(1-n) +(81*n4/64)*(1-n))
    B0 = (3*a*n/2)*(1 - n - (7*n*n/8)*(1-n) + 55*n4/64)
    C0 = (15*a*n*n/16)*(1 - n +(3*n*n/4)*(1-n))
    D0 = (35*a*n3/48)*(1 - n + 11*n*n/16)
    E0 = (315*a*n4/51)*(1-n)

    S = A0*latitude - B0*math.sin(2*latitude) + C0*math.sin(4*latitude)- D0*math.sin(6*latitude) + E0*math.sin(8*latitude);

    ## Coefficients for ITM coordinates

    p    = longitude-centralMeridian
    Ki   = S*k0
    Kii  = nu*math.sin(latitude)*math.cos(latitude)*k0/2
    Kiii = ((nu*math.sin(latitude)*pow3(math.cos(latitude)))/24)*(5-pow2(math.tan(latitude))+9*e1sq*pow2(math.cos(latitude))+4*e1sq*e1sq*pow4(math.cos(latitude)))*k0;
    Kiv  = nu*math.cos(latitude)*k0
    Kv   = pow3(math.cos(latitude))*(nu/6)*(1-pow2(math.tan(latitude))+e1sq*pow2(math.cos(latitude)))*k0;

    easting  = round(219529.58+ Kiv*p+Kv*pow3(p) - 60)
    northing = round(Ki+Kii*p*p+Kiii*pow4(p) - 3512424.41+ 626907.39 - 45)

    return easting,northing


path = r'C:\temp\building.shp'

new_layer = r'C:\temp\new_layer.shp'

layer           = QgsVectorLayer(path, "Cut_gush_", "ogr")

road_type_index = layer.fields().indexFromName('JOIN_FID')

print (road_type_index)

    

for feature in layer.getFeatures():
    geometry = feature.geometry().asQPolygonF()
    print (geometry)
    new_list = []
    for i in geometry:
        x,y = Tran_WGS_to_ISR(i.x(),i.y())
        point = QgsPointXY(x,y)
        new_list.append(point)

    polygon = QgsGeometry.fromPolygonXY([new_list])
    print (polygon)

    vl    = QgsVectorLayer(str('Polygon?crs='+'2039'), "polygon", "memory")
    pr    = vl.dataProvider()
    fet   = QgsFeature()
    fet.setGeometry(polygon)
    #fet.setAttributes(data_list)
    pr.addFeatures([fet])

    vl.updateExtents()
QgsProject.instance().addMapLayer(vl)
    

#layer = QgsProject.instance().addMapLayer(layer)
#for i in layer.fields():
#    print (i)