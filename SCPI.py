
import visa
class SCPI_parameter(object):
    out_formatters = {
        str: '{0}'.format,
        float: '{0}'.format,
        int: '{0}'.format
    }
    def __init__(self,string,restrict_values=None,data_type=str,out_formatter = None, in_formatter = None,read_only=False,cached=True,units='',name_in_obj=None):
        self.units = units
        self.param_string = string
        self.restricted_values = restrict_values
        self.data_type = data_type
        self.out_formatter = self.out_formatters[self.data_type] if out_formatter is None else out_formatter
        self.in_formatter = data_type if in_formatter is None else in_formatter
        self.read_only = read_only
        self.cached = cached
        self.name = name_in_obj or string
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not self.cached or self.param_string not in obj.param_cash:
            data = obj.dev.query((self.param_string + '?'))  # changes here
            if len(self.units) and data.endswith(self.units):
                data = data[:-len(self.units)]
            data =self.in_formatter(data)
            obj.param_cash[self.name] = data
        else:
            data = obj.param_cash[self.name]
        return data
    def __set__(self, obj, val):
        if self.read_only:
            raise Exception('Error when trying to write to {0} that is read only'.format(self.param_string))
        if not isinstance(val,self.data_type):
            val = self.data_type(val)
        if self.restricted_values and val not in self.restricted_values:
            raise Exception('Try to write {0} that have restricted value range {1} with value {2}'.format(self.param_string,self.restricted_values,val))
        obj.dev.write(self.param_string+' '+self.out_formatter(val)+self.units)
        obj.param_cash[self.name] = val  # changes here
    def __set_name__(self, owner, name):
        self.name = name
class GeneratorBase:
    has_list_mode     = False
    has_fm_modulation = False
    idn = SCPI_parameter('*IDN',read_only=True)
    open_resource_kwargs = {}
    save_mandatory_fields = ['idn','frequency','power','output_en']
    def __init__(self,visa_resource=None,host=None,port=None,**kwargs):
        self.param_cash = dict()
        rm = visa.ResourceManager()
        if visa_resource is not None:
            resource = visa_resource
        elif host is not None:
            if port is not None:
                resource = 'TCPIP0::' + host + '::' + str(port) + '::SOCKET'
            else:
                resource = 'TCPIP0::' + host + '::inst0::INSTR'
        else:
            raise Exception('No VISA resource specified')
        self.dev = rm.open_resource(resource, **self.open_resource_kwargs)
        self.Off()
    def Power(self, powerf=None):
        if powerf != None:
            self.power=powerf
        return self.power
    def On(self):
        self.output_en=1
        return 1
    def Off(self):
        self.output_en=0
        return 0

    def Freq(self,freqf):
        if freqf != None:
            self.frequency=freqf
        return self.frequency
    def CW(self, freq = None, power = None):
        """
        states freq and power and makes CW regime
        :param freq:
        :param power:
        :return:
        """
        if freq is not None:
            self.Freq(freq)
        if power is not None:
            self.Power(power)
        if freq is None and power is None:
            self.On()
        else:
            self.Off()
        return
    def to_dict(self):
        out = {}
        for f in self.save_mandatory_fields:
            if f not in self.param_cash:
                out[f] = getattr(self,f)
        out.update(self.param_cash)
        return out