import time
import numpy as np
import socket
from Socket2Serial import Socket2Serial
from serial import Serial

from Hardware.SCPI import SCPI_parameter,GeneratorBase
import visa


                 
class SRS_DS345(GeneratorBase):
    frequency     = SCPI_parameter('FREQ', data_type=float)  #Frequency
    power         = SCPI_parameter('AMPL',data_type=float,units='DB')  #Amplitude of RF (Type-N Output) in dBm
    temperature   = SCPI_parameter('TEMP',read_only=True,data_type=float)  #tempearture
    output_en     = SCPI_parameter('ENBR', restrict_values=(0,1),data_type=int)  # On/Off
    has_list_mode = False
    has_fm_modulation = False
    def __init__(self, comport=None,host=None,port=None):
        #priority to IP connection
        rm = visa.ResourceManager()
        if host is not None and port is not None:
            dev = rm.open_resource('TCPIP0::'+host+'::'+str(port)+'::SOCKET',read_termination='\r\n')
        elif comport is not None:
            assert False
            p = Serial(comport,baudrate=19200,timeout=10, rtscts=True, stopbits=2)
        else:
            raise Exception('No interface defined for DS345')
        self.dev = dev
        self.dev.timeout=2000
    def FMext(self,val):
        if abs(val)>1e2:
            raise NotImplemented

class SRS_SG382(GeneratorBase):
    rm = visa.ResourceManager()
    has_fm_modulation = True
    has_list_mode = False
    frequency     = SCPI_parameter('FREQ', data_type=float)  #Frequency
    power         = SCPI_parameter('AMPR',data_type=float)  #Amplitude of RF (Type-N Output) in dBm
    power_bnc     = SCPI_parameter('AMPL',data_type=float)  #Amplitude of LF (BNC Output) in dBm
    temperature   = SCPI_parameter('TEMP',read_only=True,data_type=float)  #tempearture
    output_en     = SCPI_parameter('ENBR', restrict_values=(0,1),data_type=int)  # On/Off
    mod_dccouple  = SCPI_parameter('COUP', restrict_values=(0,1),data_type=int)  # DC copling, recomended value is 1
    mod_type      = SCPI_parameter('TYPE', restrict_values=(0,1,2,3,4,5,6),data_type=int)  #Modulation Type AM/FM/ΦM/Sweep/Pulse/Blank/IQ (if option 3 is installed)
    mod_rate      = SCPI_parameter('RATE',data_type=float)  #Modulation Rate for AM/FM/ΦM
    mod_fdev      = SCPI_parameter('FDEV',data_type=float)  #FM Deviation
    mod_en        = SCPI_parameter('MODL', data_type=int  , restrict_values=(0,1))  # modulation disabled/enable
    mod_func      = SCPI_parameter('MFNC', data_type=int  , restrict_values=(0,1,2,3,4,5)) # modulation function : Sine/Ramp/Triangle/Square/Noise/EXT

    def __init__(self, ipadress='192.168.10.89'):
        self.ip = ipadress
        self.dev = self.rm.open_resource('TCPIP0::'+ipadress+'::inst0::INSTR')

    def Temp(self):
        return self.temp
    def mod_rate_(self):
#         return self.dev.ask('RATE?')
        return self.mod_rate
    def mod_depth_(self):
        return self.mod_fdev
    def FMext(self, depth):
        if depth==0:
#             self.dev.write('FDEV 0')
#             self.dev.write('MODL 0')  # modulation disabled
            self.mod_fdev = 0
            self.mod_en   = 0
        else:
#             self.dev.write('FDEV {0}'.format(depth))
#             self.dev.write('COUP 1')  # DC coupling
#             self.dev.write('MFNC 5')  # External
#             self.dev.write('MODL 1')  # modulation enabled
#             self.dev.write('TYPE 1')  # modulation enabled
            self.mod_fdev     = depth 
            self.mod_dccouple = 1     #DC
            self.mod_func     = 5     #EXT
            self.mod_en       = 1     #Enable modulation
            self.mod_type     = 1     #FM
    def FMint(self, freq, depth):
        self.mod_fdev = depth
        self.mod_func = 0
        self.mod_rate = freq
        self.mod_type = 1
#         self.dev.write('FDEV {0}'.format(depth))
#         self.dev.write('MFNC 0') # internal modulation Sine
#         self.dev.write('RATE {0}'.format(freq))
#         self.dev.write('TYPE 1') # modulation enabled

    def CW(self, freq = None, power = None):
        """
        states freq and power and makes CW regime
        :param freq:
        :param power:
        :return:
        """
        if freq is not None:
            self.frequency = freq
        if power is not None:
            self.power     = power
        if freq is None and power is None:
            self.output_en = 0
        else:
            self.output_en = 1
        return
