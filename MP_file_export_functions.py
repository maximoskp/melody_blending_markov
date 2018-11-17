#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 15:59:37 2018

@author: maximoskaliakatsos-papakostas

Functions included:
- write_stream_to_midi

"""

import music21 as m21
import os

def write_stream_to_midi(s, filePath=os.getcwd()+"/", appendToPath="", fileName='test_midi_export.mid'):
    ''' exports stream s in midi file saved in filepath with fileName '''
    mf = m21.midi.translate.streamToMidiFile(s)
    mf.open(filePath + appendToPath + fileName, 'wb')
    mf.write()
    mf.close()
# end get_minimum_pitch