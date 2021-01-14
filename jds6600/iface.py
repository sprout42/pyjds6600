import serial

from .types import *


class JDS6600:
    # Indicates the multipler/divider to use with frequency values being read 
    #     from/sent to the frequency generator.  This table also holds the 
    #     maximum value allowed for each mode so that we don't accidentally make 
    #     bad target frequency calculations in the search of more accuracy.
    #
    # These conversion values don't make a ton of sense, but it is what my testing 
    # has produced.
    _tgt_freq_conv = {
        # :w23=100,0. == 1.00 Hz
        # max is 30 MHz
        Frequency.Hz: (100.0, 3000000000.0),

        # :w23=100000,1. == 1.00 KHz (1000 Hz)
        # max is 30 MHz
        # So to convert from Hz to "target" KHz apply the normal KHz multiplier and 
        # this value.
        Frequency.KHz: (100.0, 3000000000.0),

        # :w23=100000000,2. == 1.00 MHz (1000000 Hz)
        # max is 30 MHz
        # So to convert from Hz to "target" MHz apply the normal MHz multiplier and 
        # this value.
        Frequency.MHz: (100.0, 3000000000.0),

        # :w23=100,3. == 1.00 mHz (0.001 Hz)
        # max is 80 kHz
        # This value is the first that behaves a little differently.  The target 
        # device must be programmed in whole numbers, so to set the target to 
        # 0.001 Hz you need to multiply the desired value by 100 * 1000:
        #   0.001 Hz * 100 * 1000 = :w100,3.
        Frequency.mHz: (100.0 * 1000.0, 80000.0),

        # :w23=100,4. == 1.00 uHz (0.000001 Hz)
        # max is 80 Hz
        # Same as the mHz seting but add an extra order of magnitude.
        Frequency.uHz: (100.0 * 1000000.0, 80.0),
    }

    def __init__(self, port, baudrate=115200, verbose=False, fix_read_bug=True, timeout=0.5, write_timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE):
        self.verbose = verbose

        # On some models the read "register" for the system settings are the 
        # write register + 1.  Setting this flag enables that workaround.
        self.fix_read_bug = fix_read_bug

        self._args = {
            'port': port,
            'baudrate': 115200,

            # Standard serial options that probably won't need to be changed
            'timeout': timeout,
            'write_timeout': write_timeout,
            'bytesize': bytesize,
            'parity': parity,
            'stopbits': stopbits,
        }

        self._serial = None
        self.open()

    def __del__(self):
        self.close()

    def open(self):
        self._serial = serial.Serial(**self._args)

    def close(self):
        if self._serial:
            if self._serial.is_open:
                self._serial.close()
            self._serial = None

    def _flush_input(self):
        if self._serial.in_waiting:
            out = self._serial.read(self._serial.in_waiting)
            if self.verbose:
                flushed = out.strip().decode()
                print(f'[flush]:\n{flushed}')

    def _command(self, cmd_str):
        if self.verbose:
            print(f'[cmd] {cmd_str}')
        self._serial.write(f'{cmd_str}\r\n'.encode())

        # Just use the default UTF-8 decode, this protocol is all ASCII text and 
        # shouldn't require latin-1 decoding.
        ret_str = self._serial.readline().strip().decode()
        if self.verbose:
            print(f'[ret] {ret_str}')

        return ret_str

    def _get(self, cmd, *args):
        # If no arguments are supplied set it to [0].  The command format 
        # requires at least one value after '='
        if len(args) == 0:
            args = [0]

        # If there is pending input read it now so the output is for the correct 
        # command
        self._flush_input()

        # Example of retrieving the model:
        #   [cmd] :r00=0.\r\n
        #   [ret] :r00=30.\r\n
        args_str = ','.join(f'{a}' for a in args)
        cmd_str = f':r{cmd:02}={args_str}.'

        ret_str = self._command(cmd_str)

        # Verify the start and end of the response looks correct
        if ret_str[:2] != ':r' or ret_str[-1] != '.':
            errmsg = f'Bad Response: [cmd] {cmd_str} [ret] {ret_str}'
            raise Exception(errmsg)

        out_cmd, rest = ret_str[2:-1].split('=')

        # Verify this output is for the correct command
        if int(out_cmd) != cmd:
            errmsg = f'Command mismatch: [cmd] {cmd_str} [ret] {ret_str}'
            raise Exception(errmsg)

        out_val = rest.split(',')
        if len(out_val) == 0:
            return None

        # Try to provide a little more details if the int() conversions fail
        try:
            if len(out_val) == 1:
                return int(out_val[0])
            else:
                return tuple(int(v) for v in out_val)
        except ValueError:
            errmsg = f'Unexpected Response Format: [cmd] {cmd_str} [ret] {ret_str}'
            raise Exception(errmsg)

    def _set(self, cmd, *args):
        # Extra arguments are required in the set function
        assert len(args) > 0

        # If there is pending input read it now so the output is for the correct 
        # command
        self._flush_input()

        # Example of retrieving the model:
        #   [cmd]  :w21=4.\r\n
        #   [ret] :ok\r\n
        args_str = ','.join(f'{a}' for a in args)
        cmd_str = f':w{cmd:02}={args_str}.'

        ret_str = self._command(cmd_str)

        # Verify the value was changed successfully
        if ret_str != ':ok':
            errmsg = f'Bad Response: [cmd] {cmd_str} [ret] {ret_str}'
            raise Exception(errmsg)

    def get_model(self):
        # I think the "model" returns the maximum frequency.  So a model of "30" 
        # means the max frequency is 30 MHz.
        return self._get(Command.MODEL)

    def get_serial_number(self):
        return self._get(Command.SERIAL_NUMBER)

    def get_channel(self, which=Channel.BOTH):
        resp = self._get(Command.CHANNEL_ENABLE)
        if which == Channel.BOTH:
            ch1, ch2 = resp
            return (Status(ch1), Status(ch2))
        else:
            # This command always returns both channel statuses
            return Status(resp[which])

    def set_channel(self, value, which=Channel.BOTH):
        assert isinstance(value, Status)
        if which == Channel.BOTH:
            self._set(Command.CHANNEL_ENABLE, value, value)
        elif which != Channel.NONE:
            # If the user is only enabling or disabling 1 channel then we need 
            # to know the current state of the channels first.
            channel_states = list(self.get_channel())

            # Change the desired channel
            channel_states[which] = value

            # Set the new values
            self._set(Command.CHANNEL_ENABLE, *channel_states)

    def config_channel(self, waveform=None, frequency=None, amplitude=None, offset=None, dutycycle=None, status=None, which=Channel.BOTH):
        # Allows setting one or more settings at the same time for one or both 
        # channels

        # Special handling of the "status" value.  If it is not None and the 
        # value is OFF, turn off the channels before changing any values.
        if status is not None and status == Status.OFF:
            self.set_channel(status, which)

        # Change the other settings now
        if waveform is not None:
            self.set_waveform(waveform, which)
        if frequency is not None:
            self.set_frequency(frequency, which)
        if amplitude is not None:
            self.set_amplitude(amplitude, which)
        if offset is not None:
            self.set_offset(offset, which)
        if dutycycle is not None:
            self.set_dutycycle(dutycycle, which)

        # Special handling of the "status" value.  If it is not None and the 
        # value is ON, turn on the channels after all of the other values have 
        # been set.
        if status is not None and status == Status.ON:
            self.set_channel(status, which)

    def _get_per_channel(self, cmds, which, convert, *args):
        # Utility function that can run _get() commands for both channels and 
        # converts the results using the function/type conversion provided.
        if which == Channel.BOTH:
            return tuple(convert(self._get(cmd, *args)) for cmd in cmds)
        elif which != Channel.NONE:
            return convert(self._get(cmds[which], *args))
        else:
            return ()

    def _set_per_channel(self, cmds, which, *args):
        # Utility function that can run _set() commands for both channels.
        if which == Channel.BOTH:
            for cmd in cmds:
                self._set(cmd, *args)
        elif which != Channel.NONE:
            self._set(cmds[which], *args)

    def get_waveform(self, which=Channel.BOTH):
        cmds = (Command.WAVEFORM_CH1, Command.WAVEFORM_CH2)
        return self._get_per_channel(cmds, which, Waveform)

    def set_waveform(self, value, which=Channel.BOTH):
        assert isinstance(value, Waveform)
        cmds = (Command.WAVEFORM_CH1, Command.WAVEFORM_CH2)
        self._set_per_channel(cmds, which, value)

    def _freq_convert_from_tgt(self, args):
        # The frequency conversion is annoying and weird, there are units which 
        # define  how to multiple/divide the value from the device, but those values 
        # are always whole numbers.
        value = args[0]
        units = Frequency(args[1])
        mult, _ = self._tgt_freq_conv[units][0]

        freq = value / mult
        return freq

    def _freq_convert_to_tgt(self, freq):
        # Input values are always in Hz, normally this is simple we just multiply by 
        # the Frequency.Hz multiplier (100), but if that value is not an integer 
        # then we will try the next more accurate unit.
        mult, max_freq = self._tgt_freq_conv[Frequency.Hz]
        hz_value = freq * mult

        if self.verbose:
            print(f'Checking Hz (mult: {mult}, max: {max_freq}) conversion for {freq}')
            print(f'\t{freq} * {mult} = {hz_value}')

        # If the value is a whole number, or the target frequency is > the max freq 
        # allowed in this mode, we found the most accurate frequency units to use.
        if hz_value.is_integer() or freq > max_freq:
            return (int(hz_value), Frequency.Hz)

        # Not enough accuracy, try mHz
        mult, max_freq = self._tgt_freq_conv[Frequency.mHz]
        mhz_value = freq * mult

        if self.verbose:
            print(f'Checking mHz (mult: {mult}, max: {max_freq}) conversion for {freq}')
            print(f'\t{freq} * {mult} = {mhz_value}')

        # If this value is greater than the max frequency allowed in this mode use 
        # the previous value
        if freq > max_freq:
            return (int(hz_value), Frequency.Hz)

        # If the value is a whole number we found the most accurate frequency units 
        # to use.
        if mhz_value.is_integer():
            return (int(mhz_value), Frequency.mHz)

        # Not enough accuracy, try uHz
        mult, max_freq = self._tgt_freq_conv[Frequency.uHz]
        uhz_value = freq * mult

        if self.verbose:
            print(f'Checking uHz (mult: {mult}, max: {max_freq}) conversion for {freq}')
            print(f'\t{freq} * {mult} = {uhz_value}')

        # If this value is greater than the max frequency allowed in this mode use 
        # the previous value
        if freq > max_freq:
            return (int(mhz_value), Frequency.mHz)

        # If we reached this point this is the most accurate value to use regardless 
        # of if this is a whole number or not.
        return (int(uhz_value), Frequency.uHz)

    def get_frequency(self, which=Channel.BOTH):
        cmds = (Command.FREQUENCY_CH1, Command.FREQUENCY_CH2)
        return self._get_per_channel(cmds, which, self._freq_convert_from_tgt)

    def set_frequency(self, value, which=Channel.BOTH):
        cmds = (Command.FREQUENCY_CH1, Command.FREQUENCY_CH2)
        args = self._freq_convert_to_tgt(value)
        self._set_per_channel(cmds, which, *args)

    def get_amplitude(self, which=Channel.BOTH):
        # Converting from mV to V
        amplitude_convert = lambda val: val / 1000
        cmds = (Command.AMPLITUDE_CH1, Command.AMPLITUDE_CH2)
        return self._get_per_channel(cmds, which, amplitude_convert)

    def set_amplitude(self, value, which=Channel.BOTH):
        # Convert from V to mV (use by the target)
        converted_value = value * 1000
        cmds = (Command.AMPLITUDE_CH1, Command.AMPLITUDE_CH2)
        self._set_per_channel(cmds, which, converted_value)

    def get_offset(self, which=Channel.BOTH):
        # Offset values from the function generator are in units of 10mV and 
        # offset by 1000 to support the possible negative range.  Convert these 
        # values to Volts.
        # The min offset is -9.99V (1) and the max offset is 9.99V (1999).
        offset_convert = lambda val: (val - 1000) / 100
        cmds = (Command.OFFSET_CH1, Command.OFFSET_CH2)
        return self._get_per_channel(cmds, which, offset_convert)

    def set_offset(self, value, which=Channel.BOTH):
        # Reverse the value conversion used in get_offset()
        converted_value = (value * 100) + 1000
        cmds = (Command.OFFSET_CH1, Command.OFFSET_CH2)
        self._set_per_channel(cmds, which, converted_value)

    def get_dutycycle(self, which=Channel.BOTH):
        # Dutycycle values from the function generator are in units of 0.1%.
        # Divide by 10 to convert these to normal % values.
        offset_convert = lambda val: val / 10
        cmds = (Command.DUTYCYCLE_CH1, Command.DUTYCYCLE_CH2)
        return self._get_per_channel(cmds, which, offset_convert)

    def set_dutycycle(self, value, which=Channel.BOTH):
        # Dutycycle values from the function generator are in units of 0.1%.
        # Multiply by 10 to convert these to the command value.
        converted_value = value * 10
        cmds = (Command.DUTYCYCLE_CH1, Command.DUTYCYCLE_CH2)
        self._set_per_channel(cmds, which, converted_value)

    def get_phase(self):
        # I like to return things in terms of SI units, but I really don't like 
        # Radians, they are awkward. Instead keep the return from this in 
        # degrees.  The units from the function generator are in 0.1 degrees so 
        # divide the retrieved value by 10 to get whole degrees.
        return self._get(Command.PHASE) / 10

    def set_phase(self, value):
        # Like get_phase() expect the input value to be in degrees and multiply 
        # by 10 to get the target value.
        converted_value = value * 10
        self._set(Command.PHASE, converted_value)

    """
    The Set/Get action commands don't work super reliably or deterministically
    yet so these are commented out

    def get_action(self):
        return Action(self._get(Command.ACTION))

    def set_action(self, action):
        assert isinstance(action, Action)

        # TODO: Ensure that the UI is in the right mode or else we will get "OK" 
        # back but no action will be performed (doesn't seem to help?)

        self._set(Command.ACTION, action)
    """

    def get_ui_mode(self):
        return UIMode(self._get(Command.UI_MODE))

    def set_ui_mode(self, value):
        assert isinstance(value, UIMode)
        self._set(Command.UI_MODE, value)

    # TODO: Lots more commands need to have set/get functions implemented.


__all__ = [
    'JDS6600',
]
