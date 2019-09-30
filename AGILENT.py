from serial import Serial
import time

from Socket2Serial import Socket2Serial
from Hardware.SCPI import SCPI_parameter,GeneratorBase
import visa

rm = visa.ResourceManager()

class Agilent_E4422B(GeneratorBase):
    mod_sources   = ('EXT1','EXT2')
    coupling_types = ('DC','AC')
    frequency     = SCPI_parameter('FREQ', data_type=float)  #Frequency
    power         = SCPI_parameter('POWEr',data_type=float)  #Amplitude of RF (Type-N Output) in dBm + dBm!!!!!!!!
    temperature   = SCPI_parameter('TEMP',read_only=True,data_type=float)  #tempearture
    output_en     = SCPI_parameter('OUTP:STAT', restrict_values=(0,1),data_type=int)  # On/Off
    mod_en        = SCPI_parameter('OUTP:MOD:STAT', restrict_values=(0,1),data_type=int)  # On/Off
    fm_dev        = SCPI_parameter('FM:DEV', data_type=float)  # Frequency
    fm_en         = SCPI_parameter('FM:STAT', restrict_values=(0,1),data_type=int)  # On/Off
    fm_source     = SCPI_parameter('FM:SOUR', restrict_values=mod_sources,data_type=str)  # FM source
    am_dev        = SCPI_parameter('AM:DEV', data_type=float)
    am_en         = SCPI_parameter('AM:STAT', restrict_values=(0,1),data_type=int)  # On/Off
    am_source     = SCPI_parameter('AM:SOUR', restrict_values=mod_sources,data_type=str)  #AM source

    fm_ext1_coupling = SCPI_parameter('FM:EXT1:COUP', restrict_values=coupling_types, data_type=str)
    fm_ext2_coupling = SCPI_parameter('FM:EXT2:COUP', restrict_values=coupling_types, data_type=str)
    am_ext1_coupling = SCPI_parameter('AM:EXT1:COUP', restrict_values=coupling_types,data_type=str)
    am_ext2_coupling = SCPI_parameter('AM:EXT2:COUP', restrict_values=coupling_types,data_type=str)
    has_list_mode = False
    has_fm_modulation = True
    output = False
    verbose = False
    def log(self,*args):
        if self.verbose:
            print(args)

    def __init__(self, comport=None, host=None, port=None):
        # priority to IP connection
        if host is not None and port is not None:
            dev = rm.open_resource('TCPIP0::' + host + '::' + str(port) + '::SOCKET', read_termination='\n')
        elif comport is not None:
            assert False
            p = Serial(comport, baudrate=19200, timeout=10, rtscts=True, stopbits=2)
        else:
            raise Exception('No interface defined for DS345')
        self.dev = dev
        self.dev.timeout = 2000
    def FMext(self, depth):
        self.fm_source = 'EXT1'
        self.fm_ext1_coupling = 'DC'
        self.fm_dev = depth
        self.fm_en = 1
        self.mod_en = 1
    def AMext(self, depth):
        self.am_source = 'EXT2'
        self.am_ext2_coupling = 'DC'
        self.am_dev = depth
        self.am_en = 1
        self.mod_en = 1


