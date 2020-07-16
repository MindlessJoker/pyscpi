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

    output = False
    verbose = False
    open_resource_kwargs = dict(read_termination='\n')
    save_mandatory_fields = ['idn', 'current0','range0','mode0']
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