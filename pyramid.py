# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFile,
                       QgsMessageLog)
from qgis import processing


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):


    INPUT     = 'INPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'myscript'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('pyramid')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Example scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'examplescripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('Input folder'),
                behavior=QgsProcessingParameterFile.Folder,
                fileFilter='All files (*.*)',
                defaultValue=r"C:\Users\Administrator\Desktop\medad\python\Work\pyramid\data"
            )
        )


    def processAlgorithm(self, parameters, context, feedback):
        
        import os

        from osgeo import gdal
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context
        )
        
        
        class Pyramid():
            def __init__(self,folder):
                self.folder  = folder
                self.rasters = []
            
            def pyramids(self):
                if self.rasters:
                    for gdaladdoFile in self.rasters:
                        print ('working on: {}'.format(gdaladdoFile))
                        feedback.pushInfo('working on: {}'.format(gdaladdoFile))
                        Image = gdal.Open(gdaladdoFile, 0)  
                        gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
                        Image.BuildOverviews('NEAREST', [2,4, 8, 16, 32, 64, 128], gdal.TermProgress_nocb)
                            
                        del Image 

            def readTif(self):
                self.rasters = [root +'\\' + file for root, dirs, files in os.walk(self.folder)\
                                   for file in files if file.endswith('tif')]

        folderMe = parameters['INPUT']

        #source = r"C:\Users\Administrator\Desktop\medad\python\Work\pyramid\data"
        pyr = Pyramid(folderMe)
        pyr.readTif  ()
        pyr.pyramids ()
                    

        return {self.INPUT: 'Finish building Pyramid'}
