#!/usr/bin/env python                                            
#
# heatmap ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os
# import importlib.metadata
import numpy as np
from matplotlib import pyplot as plt
from skimage.io import imread
from chrisapp.base import ChrisApp
import glob



Gstr_title = """
 _                _                         
| |              | |                        
| |__   ___  __ _| |_ _ __ ___   __ _ _ __  
| '_ \ / _ \/ _` | __| '_ ` _ \ / _` | '_ \ 
| | | |  __/ (_| | |_| | | | | | (_| | |_) |
|_| |_|\___|\__,_|\__|_| |_| |_|\__,_| .__/ 
                                     | |    
                                     |_|    
"""

Gstr_synopsis = """
(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)
    NAME
       heatmap.py 
    SYNOPSIS
        python heatmap.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--input1 <sample1Dir>]                                     \\
            [--input2 <sample2Dir>]                                     \\
            <inputDir>                                                  \\
            <outputDir> 
    BRIEF EXAMPLE
        * Bare bones execution
            docker run --rm -u $(id -u)                               \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing        \
                fnndsc/pl-heatmap heatmap --input1 dir1 --input2 dir2 \
                /incoming /outgoing
    DESCRIPTION
        `heatmap.py` ...
    ARGS
        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.
        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
        [--input1 <sample1Dir>]
        The name of the subdirectory of the input directory to containing either inferred or ground truth images
        [--input2 <sample2Dir>]
        The name of the subdirectory of the input directory to containing either inferred or ground truth images
"""

class Heatmap(ChrisApp):
    """
    An app to compare a set of 2 different png (256x256 px) images and generate a heatmap
    """
    PACKAGE                 = __package__
    TITLE                   = 'A heatmap generating app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = '' # url of an icon image
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument('--input1',dest='input1',type=str,optional=False,
                          help='What file do you want to upload?')
        self.add_argument('--input2',dest='input2',type=str,optional=False,
                          help='What file do you want to upload?')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        self.load_images(options)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        
        print(Gstr_synopsis)

    def load_images(self, options):
        
        img1 = []
        img2 = []

        print("Loading Images...")

        
        for file in os.scandir(os.path.join(options.inputdir,options.input1)):
            if (file.path.endswith(".jpg") or file.path.endswith(".png")) and file.is_file():
                img1.append(file.path)

        for file in os.scandir(os.path.join(options.inputdir,options.input2)):
            if (file.path.endswith(".jpg") or file.path.endswith(".png")) and file.is_file():
                img2.append(file.path)

        
        self.create_heatmap(options, sorted(img1),sorted(img2))

    def create_heatmap(self, options,img1, img2):
    

        array_length = len(img1)
        for num in range(array_length):
        
        
            single_img1 = imread(img1[num])
            single_img2 = imread(img2[num])
            heat_map = np.zeros([256,256],dtype=np.uint8)
            for i in range(0,255):
                for j in range(0,255):
                    heat_map[i][j] = abs(int(single_img2[i][j]) - int(single_img1[i][j]))

            fig = plt.figure(figsize=(14,16))
            plt.imshow(heat_map,cmap='hot')
            outputfile = options.outputdir + '/' + 'heat_map' + str(num) + '.png'
            print("Saving heatmap image number ", str(num))
            plt.savefig(outputfile)

