from serial import Serial
import time
import numpy as np

# *CLS
# *ESE
# *ESR
# *IDN
# *LRN
# *OPC
# *RST
# *SRE
# *STB
# *WAI
# *PSC
# *TRG
# SYSTem:DATE
# SYSTem:DATE?
# SYSTem:TIME
# SYSTem:TIME?
# SYSTem:NAME?
# SYSTem:ERRor?
# SYSTem:ERRor:NEXT?
# SYSTem:ERRor:ALL?
# SYSTem:ELISt?
# SYSTem:SNUM?
# SYSTem:SOFTware?
# SYSTem:HARDware?
# SYSTem:LANGuage
# SYSTem:LANGuage?
# 8
# 2.2 Trigger commands
# TRIGger:SOURce { IMMediate | EXTernal | VIDeo }
# TRIGger:SOURce?
# TRIGger:SLOPe { POSitive | NEGative }
# TRIGger:SLOPe?
# TRIGger:SOFTware Only valid in single sweep mode
# 2.3	 Configuration of the parameters
# SYSTem:AUTotune
# SYSTem:PRESet
# SYSTem:REFerence { INTernal | EXTernal }
# SYSTem:REFerence?
# MEASure:TGENerator { ON | OFF | 0 | 1 } Only valid for HMS1010 and HMS3010
# MEASure:TGENerator?
# MEAS:PAMP { ON | OFF | 0 | 1 } Only valid with option HO3011
# MEAS:PAMP?
# MEASure {CFRX | M1RX}
# MEASure:UNCAl?
# BANDwidth:RBW { 100 | 300 | 100 | 3000 | 10000 | 30000 | 100000 | 200000 | 300000 | 1000000 | C200 | C9k | C120k | C1M }
# BANDwidth:RBW?
# BANDwidth:RBW:AUTO { ON | OFF | 0 | 1 }
# BANDwidth:RBW:AUTO?
# BANDwidth:VBW { 10 | 30 | 100 | 300 | 1000 | 3000 | 10000 | 30000 | 100000 | 300000 | 1000000 }
# BANDwidth:VBW?
# BANDwidth:VBW:AUTO { ON | OFF | 0 | 1 }
# BANDwidth:VBW:AUTO?
# AMPLitude:ATTenuation {LNOIse| LDIStortion}
# AMPLitude: ATTenuation?
# AMPLitude:ATTenuation:LEVel?
# AMPLitude:RLEVel { <value in dBm/dBuV> | MINimum | MAXimum }
# AMPLitude:RLEVel? [ MINimum | MAXimum ]
# AMPLitude:UNIT {dBm | dBuV | V | W}
# AMPLitude:UNIT?
# AMPLitude:RANGe { LINear, 0.5, 1, 2, 5, 10 }
# AMPLitude:RANGe?
# AMPLitude:TGATtenuation <value>
# AMPLitude:TGATtenuation?
# FREQuency:CENTer { <value in Hz> | MARKer[n] | MINimum | MAXimum }
# FREQuency:CENTer? [ MINimum | MAXimum ]
# FREQuency:CENTer:STEPsize { <value> | SPAN01 | SPAN05 | STC | MINimum | MAXimum }
# FREQuency:CENTer:STEPsize?
# 9

# FREQuency:SPAN { <value in Hz> | LAST | FULL | ZERO | MINimum | MAXimum }
# FREQuency:SPAN? [ MINimum | MAXimum ]
# FREQuency:STARt { <value in Hz> | MINimum | MAXimum }
# FREQuency:STARt? [ MINimum | MAXimum ]
# FREQuency:STOP { <value in Hz> | MINimum | MAXimum }
# FREQuency:STOP? [ MINimum | MAXimum ]
# FREQuency:STEP { <value in Hz> | MINimum | MAXimum } Only valid in Receiver Mode
# FREQuency:STEP? [ MINimum | MAXimum ]
# SWEep:TIME { <value in s> }
# SWEep:TIME?
# SWEep:TIME:AUTO { ON | OFF | 0 | 1 }
# SWEep:TIME:AUTO?
# SWEep:MODE { CONTinous | SINGle }
# SWEep:MODE?
# SWEep:STATe?
# 2.4 Trace capture commands
# HCOPy?
# HCOPy:DATA
# HCOPy:FORM { BMP, GIF }
# HCOPy:FORM?
# HCOPy:SIZE:X?
# HCOPy:SIZE:Y?
# 2.5 Receiver mode - Commands
# SYSTem:MODE { SWEep | RMODe }
# SYSTem:MODE?
# RMODe:FREQuency { <value in Hz> | MINimum | MAXimum }
# RMODe:FREQuency? [ MINimum | MAXimum ]
# RMODe:FREQuency:STEP { <value in Hz> | MINimum | MAXimum }
# RMODe:FREQuency:STEP? [ MINimum | MAXimum ]
# RMODe:MTIMe { <value in s> | MINimum | MAXimum }
# RMODe:MTIMe? [ MINimum | MAXimum ]
# RMODe:DETector { PEAK | AVG | QPEak | RMS }
# RMODe:DETector?
# RMODe:AUDio:DEModulation { ON | OFF | 0 | 1 }
# RMODe:AUDio:DEModulation?
# RMODe:AUDio:MODulation { AM | FM }
# RMODe:AUDio:MODulation?
# RMODe:AUDio:VOLume { <value in %> | MINimum | MAXimum }
# RMODe:AUDio:VOLume? [ MINimum | MAXimum ]
# RMODe:LEVel?
# 10

# 2.6 Marker Commands
# MARKer[n]:STATe { OFF | ON | 0 | 1 }
# MARKer[n]:STATe?
# MARKer[n]:MODE { POSition | DELTa }
# MARKer[n]:MODE?
# MARKer:FCOunter:STATe { OFF | ON | 0 | 1 }
# MARKer:FCOunter:STATe?
# MARKer:FCOunter:VALue?
# MARKer:AOFF
# MARKer[n]:[SET]:FREQuency { <value in Hz> | MINimum | MAXimum }
# MARKer[n]:[SET]:FREQuency?
# MARKer[n][:SET]:CENTer
# MARKer[n]:NOISe { OFF | ON | 0 | 1 }
# MARKer[n]:NOISe?
# MARKer[n][:SET]:LEVel?
# MARKer[n][:SET]:REFerence
# 2.7 Peak Commands
# MARKer[n]:MAXimum:PEAK
# MARKer[n]:MAXimum:NEXTpeak
# MARKer[n]:MAXimum:LEFT
# MARKer[n]:MAXimum:RIGHt
# MARKer[n]:MINimum
# MARKer[n]:MAXimum:ALL
# 2.8 Display Commands
# DISPlay:TRACe { OFF | ON | 0 | 1 }
# DISPlay:TRACe?
# DISPlay:TRACE:INTensity { <value in percent> | MINimum | MAXimum }
# DISPlay:TRACE:INTensity?
# DISPlay:BACKlight { <value in percent> | MINimum | MAXimum }
# DISPlay:BACKlight?
# DISPlay:GRID { <value in percent> | MINimum | MAXimum }
# DISPlay:GRID?
# DISPlay:GRID:SETup { RETicle | LINE | OFF }
# DISPlay:GRID:SETup?
# DISPlay:GRID:SCALe { OFF | ON | 0 | 1 }
# DISPlay:GRID:SCALe?
# 11

# DISPlay:TRANsparancy { <value in percent> | MINimum | MAXimum }
# DISPlay:TRANsparancy? [ MINimum | MAXimum ]
# LED:BRIGhtness { HIGH | LOW }
# LED:BRIGhtness?
# 2.9 Trace Commands
# TRACe:MODE { CLR | MAXimum | MINimum | AVErage | HOLD }
# TRACe:MODE?
# TRACe:MEMory { SAVE | SHOW }
# TRACE:MEMory:SHOW { ON | OFF | 0 | 1 }
# TRACE:MEMory:SHOW?
# TRACe:DETector { AUTO | SAMPle | MAXimum | MINimum }
# TRACe:DETector?
# TRACe:MATH { OFF | TMEM | MTRACe }
# TRACe:MATH?
# TRACe:DATA?
# TRACe:DATA:FORMat {BIN | CSV}
# TRACe:DATA:FORMat?
# TRACe:DATA:BORDer {LSBFirst | MSBFirst}
# TRACe:DATA:BORDer?

import ctypes,struct
class SCPI_parameter(object):
    out_formatters = {
        str: '{0}'.format,
        float: '{0}'.format,
        int: '{0}'.format
    }
    def __init__(self,string,restricted_values=None,data_type=str,out_formatter = None, in_formatter = None,read_only=False):

        self.param_string = string
        self.restricted_values = restricted_values
        self.data_type = data_type
        self.out_formatter = self.out_formatters[self.data_type] if out_formatter is None else out_formatter
        self.in_formatter = data_type if in_formatter is None else in_formatter
        self.read_only = read_only
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        obj.dev.write((self.param_string+'? \n').encode('latin'))
        data = obj.dev.readline().decode('latin')[:-1]
        return self.in_formatter(data)
    def __set__(self, obj, val):
        if self.read_only:
            raise Exception('Error when trying to write to {0} that is read only'.format(self.param_string))
        if not isinstance(val,self.data_type):
            val = self.data_type(val)
        if self.restricted_values and val not in self.restricted_values:
            raise Exception('Try to write {0} that have restricted value range {1} with value {2}'.format(self.param_string,self.restricted_values,val))
        obj.dev.write((self.param_string+' '+self.out_formatter(val)+'\n').encode('latin'))

class SCPI_bin_data_array(object):
    def __init__(self,string,read_only=False):
        self.param_string = string
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        obj.dev.write((self.param_string+'? \n').encode('latin'))
        data = obj.dev.read(1).decode('latin')
        assert data == '#'
        data_len_len = int(obj.dev.read(1).decode('latin'))
        data_len = int(obj.dev.read(data_len_len).decode('latin'))
        data = obj.dev.read(8*data_len)

    def __set__(self, obj, val):
        assert False

class SCPI_csv_data_array(object):
    def __init__(self,string,read_only=False):
        self.param_string = string
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        obj.dev.write((self.param_string+'? \n').encode('latin'))
        get_line = lambda : obj.dev.readline().decode('latin').replace('\r','').replace('\n','')
        data = get_line()[0]
        assert data == '"'

        header = get_line().split(',')
        params_count = len(header)

        dummy = get_line()
        data = []
        while True:
            cur_l = get_line()
            if len(cur_l)==0:
                break
            d = np.fromstring(cur_l,dtype=float,sep=',')
            if len(d) == 2:
                data.append(d)
        dummy = get_line()
        #assert dummy == '"'
        return np.array(data)
    def __set__(self, obj, val):
        assert False
class HAMEG_HMS3010(object):
    idn            = SCPI_parameter('*IDN',read_only=True)
    trigger_source = SCPI_parameter('TRIG:SOUR',restricted_values=('IMM','EXT','VID'))
    freq_start     = SCPI_parameter('FREQ:STARt',data_type=float)
    freq_stop      = SCPI_parameter('FREQ:STOP', data_type=float)
    freq_step      = SCPI_parameter('FREQ:STEP', data_type=float)
    trace_data     = SCPI_csv_data_array('TRACe:DATA')
    trace_data_format = SCPI_parameter('TRACe:DATA:FORMat', restricted_values=('CSV','BIN'))
    sweep_mode     = SCPI_parameter('SWEep:MODE',restricted_values = ('CONT','SING'))
    sweep_state    = SCPI_parameter('SWEep:STATe',read_only=True)
    def __init__(self,port):
        self.dev = Serial(port,baudrate=115200,stopbits=2,timeout=2)
        self.trace_data_format = 'CSV'
    def force_trigger(self,wait=False):
        self.dev.write('TRIGger:SOFTware\n')
        while wait and self.sweep_state!='READY':
            time.sleep(0.1)

