# -*- coding: utf-8 -*-

import geopandas as gpd
import math
from shapely.ops import transform

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

def Transform(path,Out_put):

    layer = gpd.read_file(path)
    crs   = layer.crs
    gdf = layer
    gdf.to_crs(crs)
    gdf['geometry'] =  layer['geometry'].apply(lambda poly: transform(lambda y, x: Tran_WGS_to_ISR(x,y), poly))
    gdf.to_file(Out_put)


path    = r''
Out_put = r''

Transform(path,Out_put)


#####-------UPDATE cursor  geopandas

# import geopandas as gpd

# shp = '/path/to/your/shapefile.shp'

# # Read shp
# data = gpd.read_file(shp)

# # Iterate over rows and update buffer_distance field
# for row in data.itertuples():
#     data.at[row.Index, 'buffer_distance'] = row.road_type *100

# # Write to shapefile
# data.to_file('/path/to/your/shapefile_updated.shp')