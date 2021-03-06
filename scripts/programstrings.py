# -*- coding: utf-8 -*-

# programstrings.py - This python "script" holds general texts for the other scripts

# Copyright (c) 2012-2013 Harry van der Wolf. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# This file is part of pyexiftoolgui.
# pyexiftoolgui is a pySide script program that reads and writes  
# gps tags from/to files. It can use a "reference" image to write the
# gps tags to a multiple set of files that are taken at the same
# location.
# pyexiftoolgui is a graphical frontend for the open source
# command line tool exiftool by Phil Harvey, but it's not
# a complete exiftool gui: not at all.


# SUPPORTEDIMAGES is the list of exiftool supported images. If a new image format is added to exiftool, simply add it to this (alphabetical) list
# This list should only contain images and not other formats like videos, music and so on
SUPPORTEDIMAGES     = ("*.3fr "
                       "*.acr *.ai *.ait .arw "
                       "*.bmp *.dib *.btf "
                       "*.cos *.cr2 *.crw *.ciff *.cs1 "
                       "*.dcm *.dc3 *.dic *.dicm *.dcp *.dcr *.djvu *.djv *.dng "
                       "*.eip *.erf *.exif *.exr "
                       "*.fff *.fpx "
                       "*.gif *.hdp *.wdp *.hdr "
                       "*.icc *.icm *.idml *.iiq *.ind *.indd *.indt *.inx *.itc "
                       "*.j2c *.jpc *.jp2 *.jpf *.j2k *.jpm *.jpx *.jpeg *.jpg "
                       "*.k25 *.kdc "
                       "*.mef *.mie *.miff *.mif "
                       "*.mos *.mpo *.mrw *.mxf "
                       "*.nef *.nrw "
                       "*.orf "
                       "*.pcd *.pdf *.pef *.pgf *.pict *.pct *.pmp *.png *.jng *.mng "
                       "*.ppm *.pbm *.pgm *.psp *.pspimage "
                       "*.qtif *.qti *.qif "
                       "*.raf *.raw *.rw2 *.rwl *.rwz "
                       "*.sr2 *.srf *.srw *.svg "
                       "*.thm *.tiff *.tif "
                       "*.webp "
                       "*.x3f *.xcf *.xmp")
# SUPPORTEDFORMATS is the list of exiftool supported formats. If a new format is added to exiftool, simply add it to this (alphabetical) list
SUPPORTEDFORMATS     = ("*.3fr *.3g2 *.3gp2 *.3gp *.3gpp "
                       "*.acr *.afm *.acfm *.amfm *.ai *.ait *.aiff *.aif *.aifc *.ape *.arw *.asf *.avi "
                       "*.bmp *.dib *.btf "
                       "*.chm *.cos *.cr2 *.crw *.ciff *.cs1 "
                       "*.dcm *.dc3 *.dic *.dicm *.dcp *.dcr *.dfont *.divx *.djvu *.djv *.dng *.doc *.dot "
                       "*.docx *.docm *.dotx *.dotm *.dylib *.dv *.dvb "
                       "*.eip *.eps *.epsf *.ps *.erf *.exe *.dll *.exif *.exr "
                       "*.f4a *.f4b *.f4p *.f4v *.fff *.fla *.flac *.flv *.fpx "
                       "*.gif *.gz *.gzip *.hdp *.wdp *.hdr *.html *.htm *.xhtml "
                       "*.icc *.icm *.idml *.iiq *.ind *.indd *.indt *.inx *.itc "
                       "*.j2c *.jpc *.jp2 *.jpf *.j2k *.jpm *.jpx *.jpeg *.jpg "
                       "*.k25 *.kdc *.key *.kth *.la *.lnk "
                       "*.m2ts *.mts *.m2t *.ts *.m4a *.m4b *.m4p *.m4v *.mef *.mie *.miff *.mif *.mka *.mkv *.mks "
                       "*.mos *.mov *.qt *.mp3 *.mp4 *.mpc *.mpeg *.mpg *.m2v *.mpo *.mqv *.mrw *.mxf "
                       "*.nef *.nmbtemplate *.nrw *.numbers "
                       "*.odb *.odc *.odf *.odg *.odi *.odp *.ods *.odt *.ofr *.ogg *.ogv *.orf *.otf "
                       "*.pac *.pages *.pcd *.pdf *.pef *.pfa *.pfb *.pfm *.pgf *.pict *.pct *.pmp *.png *.jng *.mng "
                       "*.ppm *.pbm *.pgm *.ppt *.pps *.pot *.potx *.potm *.ppsx *.ppsm *.pptx *.pptm *.psd *.psb *.psp *.pspimage "
                       "*.qtif *.qti *.qif "
                       "*.ra *.raf *.ram *.rpm *.rar *.raw *.raw *.riff *.rif *.rm *.rv *.rmvb *.rsrc *.rtf *.rw2 *.rwl *.rwz "
                       "*.so *.sr2 *.srf *.srw *.svg *.swf "
                       "*.thm *.thmx *.tiff *.tif *.ttf *.ttc "
                       "*.vob *.vrd *.vsd *.wav *.webm *.webp *.wma *.wmv *.wv "
                       "*.x3f *.xcf *.xls *.xlt *.xlsx *.xlsm *.xlsb *.xltx *.xltm *.xmp")

# Renaming options for the second "Do it yourself"tab
d01 = { 'option' : 'YYYYMMDDHHMMSS', 'tag' : '${CreateDate}', 'format': '%Y%m%d%H%M%S' }
d02 = { 'option' : 'YYYYMMDD_HHMMSS', 'tag' : '${CreateDate}', 'format': '%Y%m%d_%H%M%S' }
d03 = { 'option' : 'YYYYMMDD-HHMMSS', 'tag' : '${CreateDate}', 'format': '%Y%m%d-%H%M%S' }
d04 = { 'option' : 'YYYY_MM_DD_HH_MM_SS', 'tag' : '${CreateDate}', 'format': '%Y_%m_%d_%H_%M_%S' }
d05 = { 'option' : 'YYYY-MM-DD-HH-MM-SS', 'tag' : '${CreateDate}', 'format': '%Y-%m-%d-%H-%M-%S' }
d06 = { 'option' : 'YYYYMMDD', 'tag' : '${CreateDate}', 'format': '%Y%m%d' }
d07 = { 'option' : 'YYYY_MM_DD', 'tag' : '${CreateDate}', 'format': '%Y_%m_%d' }
d08 = { 'option' : 'YYYY-MM-DD', 'tag' : '${CreateDate}', 'format': '%Y-%m-%d' }


# End of strings 

