from serial import Serial
import time

from pyscpi.SCPI import SCPI_parameter,GeneratorBase
import visa

rm = visa.ResourceManager()


class CurrentDAC_LTC2662_nano():
    idn = SCPI_parameter('*IDN', read_only=True)
    current0      = SCPI_parameter('CUR0', data_type=float)
    range0        = SCPI_parameter('RANGE0', data_type=float)
    mode0         = SCPI_parameter('MODE0', restrict_values=(0,1),data_type=int)
    start0        = SCPI_parameter('SWEEP0:START', data_type=float)
    step0         = SCPI_parameter('SWEEP0:STEP', data_type=float)
    step_idx0     = SCPI_parameter('SWEEP0:IDX', data_type=int)
    step_count0   = SCPI_parameter('SWEEP0:COUNT', data_type=float)
    prescale0     = SCPI_parameter('SWEEP0:PSC', data_type=float)

    current1      = SCPI_parameter('CUR1', data_type=float)
    range1        = SCPI_parameter('RANGE1', data_type=float)
    mode1         = SCPI_parameter('MODE1', restrict_values=(0,1),data_type=int)
    start1        = SCPI_parameter('SWEEP1:START', data_type=float)
    step1         = SCPI_parameter('SWEEP1:STEP', data_type=float)
    step_idx1     = SCPI_parameter('SWEEP1:IDX', data_type=int)
    step_count1   = SCPI_parameter('SWEEP1:COUNT', data_type=float)
    prescale1     = SCPI_parameter('SWEEP1:PSC', data_type=float)

    current2      = SCPI_parameter('CUR2', data_type=float)
    range2        = SCPI_parameter('RANGE2', data_type=float)
    mode2         = SCPI_parameter('MODE2', restrict_values=(0,1),data_type=int)
    start2        = SCPI_parameter('SWEEP2:START', data_type=float)
    step2         = SCPI_parameter('SWEEP2:STEP', data_type=float)
    step_idx2     = SCPI_parameter('SWEEP2:IDX', data_type=int)
    step_count2   = SCPI_parameter('SWEEP2:COUNT', data_type=float)
    prescale2     = SCPI_parameter('SWEEP2:PSC', data_type=float)

    current3      = SCPI_parameter('CUR3', data_type=float)
    range3        = SCPI_parameter('RANGE3', data_type=float)
    mode3         = SCPI_parameter('MODE3', restrict_values=(0,1),data_type=int)
    start3        = SCPI_parameter('SWEEP3:START', data_type=float)
    step3         = SCPI_parameter('SWEEP3:STEP', data_type=float)
    step_idx3     = SCPI_parameter('SWEEP3:IDX', data_type=int)
    step_count3   = SCPI_parameter('SWEEP3:COUNT', data_type=float)
    prescale3     = SCPI_parameter('SWEEP3:PSC', data_type=float)

    current4      = SCPI_parameter('CUR4', data_type=float)
    range4        = SCPI_parameter('RANGE4', data_type=float)
    mode4         = SCPI_parameter('MODE4', restrict_values=(0,1),data_type=int)
    start4        = SCPI_parameter('SWEEP4:START', data_type=float)
    step4         = SCPI_parameter('SWEEP4:STEP', data_type=float)
    step_idx4     = SCPI_parameter('SWEEP4:IDX', data_type=int)
    step_count4   = SCPI_parameter('SWEEP4:COUNT', data_type=float)
    prescale4     = SCPI_parameter('SWEEP4:PSC', data_type=float)

    
    altcurrent0      = SCPI_parameter('ALTCURrent0', data_type=float)
    altcurrent1      = SCPI_parameter('ALTCURrent1', data_type=float)
    altcurrent2      = SCPI_parameter('ALTCURrent2', data_type=float)
    altcurrent3      = SCPI_parameter('ALTCURrent3', data_type=float)
    altcurrent4      = SCPI_parameter('ALTCURrent4', data_type=float)
    
    toggle0        = SCPI_parameter('TOGGLE0', data_type=int)
    toggle1        = SCPI_parameter('TOGGLE1', data_type=int)
    toggle2        = SCPI_parameter('TOGGLE2', data_type=int)
    toggle3        = SCPI_parameter('TOGGLE3', data_type=int)
    toggle4        = SCPI_parameter('TOGGLE4', data_type=int)
    
    toggle_enable  = SCPI_parameter('TOGGLEENABLE', data_type=int)
    output = False
    verbose = False
    open_resource_kwargs = dict(read_termination='\n')
    save_mandatory_fields = ['idn', 'current0','range0','mode0',
                                    'current1','range1','mode1',
                                     'current2','range2','mode2',
                                     'current3','range3','mode3',
                                     'current4','range4','mode4',]
    def __init__(self,host=None, port=None,serial_no=None,baud_rate=115200):
        # priority to IP connection
        self.param_cash = dict()
        rm = visa.ResourceManager()
        kwargs = self.open_resource_kwargs.copy()
        if serial_no is not None:
            resource = f'ASRL{serial_no}'
            kwargs['baud_rate']=baud_rate
            #open_resource_kwargs['flow_control'] = visa.
        elif host is not None:
            if port is not None:
                resource = 'TCPIP0::' + host + '::' + str(port) + '::SOCKET'
            else:
                resource = 'TCPIP0::' + host + '::inst0::INSTR'
        else:
            raise Exception('No VISA resource specified')
        self.dev = rm.open_resource(resource, **kwargs)
        self.dev.timeout = 2000
    def to_dict(self):
        out = {}
        for f in self.save_mandatory_fields:
            if f not in self.param_cash:
                out[f] = getattr(self,f)
        out.update(self.param_cash)
        return out