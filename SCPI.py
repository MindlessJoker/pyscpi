

class SCPI_parameter(object):
    out_formatters = {
        str: '{0}'.format,
        float: '{0}'.format,
        int: '{0}'.format
    }
    def __init__(self,string,restrict_values=None,data_type=str,out_formatter = None, in_formatter = None,read_only=False,cached=True,units=''):
        self.units = units
        self.param_string = string
        self.restricted_values = restrict_values
        self.data_type = data_type
        self.out_formatter = self.out_formatters[self.data_type] if out_formatter is None else out_formatter
        self.in_formatter = data_type if in_formatter is None else in_formatter
        self.read_only = read_only
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        data = obj.dev.query((self.param_string+'?'))
        if len(self.units) and data.endswith(self.units):
            data = data[:-len(self.units)]
        return self.in_formatter(data)
    def __set__(self, obj, val):
        if self.read_only:
            raise Exception('Error when trying to write to {0} that is read only'.format(self.param_string))
        if not isinstance(val,self.data_type):
            val = self.data_type(val)
        if self.restricted_values and val not in self.restricted_values:
            raise Exception('Try to write {0} that have restricted value range {1} with value {2}'.format(self.param_string,self.restricted_values,val))
        obj.dev.write(self.param_string+' '+self.out_formatter(val)+self.units)

class GeneratorBase:
    has_list_mode     = False
    has_fm_modulation = False
    idn = SCPI_parameter('*IDN',read_only=True)
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