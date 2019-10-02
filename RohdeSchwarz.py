__author__ = 'Vladimir Soshenko'

import numpy
import time
import visa

    
from pyscpi.SCPI import SCPI_parameter,GeneratorBase

class lastList:
    lastFreqList=numpy.array([])
    lastPowerList=numpy.array([])

class RohdeSchwarz_SMA100A(GeneratorBase):
    rm = visa.ResourceManager()
    has_fm_modulation = True
    has_list_mode = False
    frequency     = SCPI_parameter(':FREQ', data_type=float)  #Frequency
    power         = SCPI_parameter(':POW',data_type=float)  #Amplitude of RF (Type-N Output) in dBm
    output_en     = SCPI_parameter(':OUTP', restrict_values=(0,1),data_type=int)  # On/Off

#     mod_type      = SCPI_parameter('TYPE', restrict_values=(0,1,2,3,4,5,6),data_type=int)  #Modulation Type AM/FM/ΦM/Sweep/Pulse/Blank/IQ (if option 3 is installed)

    fmod_dev      = SCPI_parameter('FM1:DEV',data_type=float)  #FM Deviation
    fmod_en       = SCPI_parameter('FM1:STAT', data_type=int  , restrict_values=(0,1))  # modulation disabled/enable
    fmod_source   = SCPI_parameter('FM1:EXT:SOUR', restrict_values=('INT','EXT','INT,EXT','EDIG'),data_type=str)
    fmod_couple   = SCPI_parameter('FM1:EXT:COUP', restrict_values=('DC','AC'),data_type=str)  # modulation coupling
    
    amod_en       = SCPI_parameter('AM:STAT', data_type=int  , restrict_values=(0,1))  # modulation disabled/enable
    amod_depth    = SCPI_parameter('AM:DEPT',data_type=float)  #FM Deviation
    amod_source   = SCPI_parameter('AM:EXT:SOUR', restrict_values=('INT','EXT','INT,EXT'),data_type=str)
    amod_couple   = SCPI_parameter('AM:EXT:COUP', restrict_values=('DC','AC'),data_type=str)  # modulation coupling
#     mod_func      = SCPI_parameter('MFNC', data_type=int  , restrict_values=(0,1,2,3,4,5)) # modulation function : 


    has_list_mode = True
    has_fm_modulation = True
    last = lastList()
    rm = visa.ResourceManager()

    def __init__(self,**kwargs):
        super(RohdeSchwarz_SMA100A, self).__init__(**kwargs)

    def Off(self):
        if self.dev.ask(':FREQ:MODE?') == 'LIST':
            self.dev.write(':FREQ:MODE CW')
        self.dev.write(':OUTP OFF')
        self.dev.write('*WAI')

    def CW(self,f=None, power=None):
        self.dev.write(':FREQ:MODE CW')
        if f != None:
            self.dev.write(':FREQ %f' % f)
        if power != None:
            self.dev.write(':POW %f' % power)

    def checkFreqAndPowerList(self,freq,power):
        if len(self.last.lastFreqList)!=len(freq) or len(self.last.lastPowerList)!=len(power):
            return False
        for i in range(len(freq)):
            if freq[i] != self.last.lastFreqList[i]:
                return False
        for i in range(len(power)):
            if power[i]!=self.last.lastPowerList[i]:
                return False
        return True

    def List(self,freq, power):
        if numpy.iterable(power)!=0:
            powerlist=power
        else:
            powerlist=numpy.array([power for k in freq])

        self.dev.write(':FREQ:MODE CW')
        self.dev.write(':FREQ %f' % freq[0])
        self.dev.write(':POW %f' % power)
        self.dev.write('*WAI')
        if self.checkFreqAndPowerList(freq,powerlist)==False:
            self.last.lastFreqList=freq
            self.last.lastPowerList=powerlist
            self.dev.write(':LIST:DEL:ALL')
            self.dev.write('*WAI')
            self.dev.write(":LIST:SEL 'ODMR'")
            FreqString = ''
            for f in freq[:-1]:
                FreqString += ' %f,' % f
            PowerString=''
            for p in powerlist[:-1]:
                PowerString+=' %f,' % p
            FreqString += ' %f' % freq[-1]
            PowerString += ' %f' % powerlist[-1]
            self.dev.write(':LIST:FREQ' + FreqString)
            self.dev.write('*WAI')
            self.dev.write(':LIST:POW' + PowerString)
            self.dev.write('*WAI')
        self.dev.write(':TRIG1:LIST:SOUR EXT')
        self.dev.write(':TRIG1:SLOP NEG')
        self.dev.write(':LIST:MODE STEP')
        self.dev.write('*WAI')
        time.sleep(0.5)
        N = int(numpy.round(float(self.dev.ask(':LIST:FREQ:POIN?'))))
        if N != len(freq):
            raise RuntimeError('Error in SMIQ with List Mode')
        return N

    def ListCount(self):
        return self.dev.ask(':LIST:FREQ:POIN?')

    def ListOn(self):
        self.dev.write(':OUTP ON')
        self.dev.write('*WAI')
        self.dev.write(':LIST:LEAR')
        self.dev.write('*WAI')
        self.dev.write(':FREQ:MODE LIST')
        return self.dev.ask(':OUTP?')

    def ResetListPos(self):
        self.dev.write(':FREQ:MODE CW; :FREQ:MODE LIST')
        self.dev.write('*WAI')
        return self.dev.ask(':FREQ:MODE?')

    def Sweep(self,f_start, f_stop, df):
        self.dev.write(':FREQ:MODE SWE')
        self.dev.write(':SWE:MODE STEP')
        self.dev.write(':TRIG1:SOUR EXT')
        self.dev.write(':TRIG1:SLOP NEG')
        self.dev.write(':SWE:SPAC LIN')
        self.dev.write(':SOUR:FREQ:STAR %e' % f_start)
        self.dev.write(':SOUR:FREQ:STOP %e' % f_stop)
        self.dev.write(':SWE:STEP:LIN %e' % df)
        self.dev.write(':FREQ:MAN %e' % f_start)
        self.dev.write('*WAI')

        N = float(self.dev.ask(':SWE:POINTS?'))

        return int(round(N))

    def SweepPos(self,f=None):
        if f != None:
            self.dev.write(':FREQ:MAN %e' % f)
            self.dev.write('*WAI')
        return float(self.dev.ask(':FREQ?'))

    def AM(self,depth=None):
        if depth is None:
            self.dev.write(':AM:STAT OFF')
        else:
            self.dev.write('AM:SOUR EXT')
            self.dev.write('AM:EXT:COUP DC')
            self.dev.write('AM %f' % float(depth))
            self.dev.write('AM:STAT ON')
        self.dev.write('*WAI')
        return float(self.dev.ask('AM?'))

    def listmode(self,startfreq, endfreq, power, numbval):
        # freqs in Hz

        # reboot the smiq
        self.CW()
        self.Off()
        # Write new settings
        self.dev.write(':SOUR:LIST:MODE STEP')
        self.dev.write(':TRIG:LIST:SOUR EXT')
        self.dev.write(':SOUR:LIST:SEL  "GPIBLIST"')

        freqs = ''
        powers = ''
        df = (endfreq - startfreq) / float(numbval)

        for i in range(numbval-1):
            curfreq = startfreq + i*df
            freqs += str(round(curfreq/1e6,5)) + ' MHz, '
            powers += str(power) + ' dbm, '
        freqs += str(round((startfreq + (numbval-1)*df)/1e6,5)) + ' MHz'
        powers += str(power) + ' dbm'
        self.dev.write(':SOUR:LIST:FREQ ' + freqs)
        self.dev.write(':SOUR:LIST:POW ' + powers)

        #### TODO make smiq not to auto on, but list on demand.
        self.dev.write(':OUTP:STAT 1')
        self.dev.write(':OUTP:STAT?')
        print(self.dev.read())


        self.dev.write(':SOUR:LIST:LEARn')     #               %Learn previous setting
        self.dev.write(':SOUR:FREQ:MODE LIST')
        time.sleep(5)
        return

    def listmodeExplicit(self,f,p):
        # freqs in Hz

        # reboot the smiq
        self.CW()
        self.Off()


        # Write new settings
        self.dev.write(':SOUR:LIST:MODE STEP')
        self.dev.write(':TRIG:LIST:SOUR EXT')
        self.dev.write(':SOUR:LIST:DEL  "MYLIST"')
        self.dev.write(':SOUR:LIST:SEL  "MYLIST"')

        freqs = ''
        powers = ''
        pwr = p[0]
        for freq,pwr2 in zip(f[:-1],p[:-1]):
            curfreq = freq
            freqs += str(round(curfreq/1e6,5)) + ' MHz, '
            powers += str(pwr2) + ' dBm, '
        freqs += str(round(f[-1]/1e6,5)) + ' MHz'
        powers += str(pwr) + ' dBm'

        self.dev.write(':SOUR:LIST:FREQ ' + freqs)
        self.dev.write(':SOUR:LIST:POW ' + powers)
        self.dev.write(':OUTP:STAT 1')
        self.dev.write(':OUTP:STAT?')
        self.dev.read()


        self.dev.write(':SOUR:LIST:LEARn')     #               %Learn previous setting
        self.dev.write(':SOUR:FREQ:MODE LIST')
        time.sleep(2)
        return

        #self.ListOn()

        #self.On()

    def FM(self, fcentral= None, df=None, modulationfreq=None, power=None):
        assert False # DO NOT SUPPORT
#         if fcentral is None or df is None or modulationfreq is None:
#             self.smiq.write(':FM1:STAT OFF')
#         else:
#             if power < 10.0001:
#                 self.CW(fcentral,power)
#                 self.smiq.write(':FM1 '+str(df)+'kHz')
#                 self.smiq.write(':FM1:SOUR INT')
#                 self.smiq.write(':FM1:STAT ON')
#                 self.smiq.write(':FM1:INT:FREQ '+str(modulationfreq)+'Hz')

    def FMext(self, sensitivity = None):
        if sensitivity is None:
            self.fmod_en = 0
        else:
            self.fmod_source = 'EXT'
            self.fmod_couple = 'DC'
            self.fmod_dev    = sensitivity
            self.fmod_en = 1

    def FMint(self, depth = None, freq = None):
        """
        Function to initialize and turn on frequency modulation
        :param mod_depth: modulation amplitude, Hz
        :param mod_rate: modulation frequency, Hz
        :return:
        """

        if depth is not None:
            print(self.dev.ask('LFO1:FREQ?'))
            self.dev.write(':FM1:SOUR INT')
            self.dev.write(':FM1:DEV ' + str(depth))
            self.dev.write('LFO1:FREQ ' + str(freq)) # TODO check this
            self.dev.write(':FM1:STAT ON')
            print('mod lf1 set to ', self.dev.ask('LFO1:FREQ?'))

        else:
            self.dev.write(':FM1:STAT OFF')