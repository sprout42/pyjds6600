import enum


class Command(enum.IntEnum):
    # System Info
    MODEL               = 0
    SERIAL_NUMBER       = 1

    # Waveform Mode
    CHANNEL_ENABLE      = 20
    WAVEFORM_CH1        = 21
    WAVEFORM_CH2        = 22
    FREQUENCY_CH1       = 23
    FREQUENCY_CH2       = 24
    AMPLITUDE_CH1       = 25
    AMPLITUDE_CH2       = 26
    OFFSET_CH1          = 27
    OFFSET_CH2          = 28
    DUTYCYCLE_CH1       = 29
    DUTYCYCLE_CH2       = 30
    PHASE               = 31

    # System Mode and UI Control
    ACTION              = 32
    MODE                = 33
    UI_MODE             = 34
    #MODE_RO            = 35

    # Measure Mode
    MEASURE_COUPLING    = 36
    MEASURE_GATE_TIME   = 37
    MEASURE_MODE        = 38

    # Reset Counter
    RESET_COUNTER       = 39

    # Sweep Mode
    SWEEP_START_FREQ    = 40
    SWEEP_END_FREQ      = 41
    SWEEP_TIME          = 42
    SWEEP_DIRECTION     = 43
    SWEEP_MODE          = 44

    # Pulse Mode
    PULSE_TIME          = 45
    PULSE_PERIOD        = 46
    PULSE_OFFSET        = 47
    PULSE_AMPLITUDE     = 48

    # System Settings
    SYSTEM_SOUND        = 51
    SYSTEM_BRIGHTNESS   = 52
    SYSTEM_LANGUAGE     = 53
    SYSTEM_SYNC         = 54
    SYSTEM_ARB_MAX_NUM  = 55

    # Read bug system settings
    SYSTEM_READ_BUG_SOUND       = 52
    SYSTEM_READ_BUG_BRIGHTNESS  = 53
    SYSTEM_READ_BUG_LANGUAGE    = 54
    SYSTEM_READ_BUG_SYNC        = 55
    SYSTEM_READ_BUG_ARB_MAX_NUM = 56

    # Profiles
    PROFILE_SAVE        = 70
    PROFILE_LOAD        = 71
    PROFILE_CLEAR       = 72

    # Counter Mode
    COUNTER             = 80

    # Measure Mode
    MEASURE_FREQ_10HZ   = 81
    MEASURE_FREQ_1000HZ = 82
    MEASURE_PULSE_PLUS  = 83
    MEASURE_PULSE_MINUS = 84
    MEASURE_PERIOD      = 85
    MEASURE_DUTYCYCLE   = 86
    MEASURE_UNKNOWN_1   = 87
    MEASURE_UNKNOWN_2   = 88
    MEASURE_UNKNOWN_3   = 89


class Channel(enum.IntEnum):
    # TO allow a user to select which channel data should be retrieved
    CH1  = 0
    CH2  = 1
    BOTH = 2
    NONE = 3


class Output(enum.IntEnum):
    OFF = 0
    ON  = 1


class Waveform(enum.IntEnum):
    SINE              = 0
    SQUARE            = 1
    PULSE             = 2
    TRIANGLE          = 3
    PARTIAL_SINE      = 4
    CMOS              = 5
    DC                = 6
    HALF_WAVE         = 7
    FULL_WAVE         = 8
    POSITIVE_STEP     = 9
    NEGATIVE_STEP     = 10
    NOISE             = 11
    EXPONENTIAL_RISE  = 12
    EXPONENTIAL_DECAY = 13
    MULTI_TONE        = 14
    SYNC              = 15
    LORENZ            = 16
    ARBITRARY_1       = 101
    ARBITRARY_2       = 102
    ARBITRARY_3       = 103
    ARBITRARY_4       = 104
    ARBITRARY_5       = 105
    ARBITRARY_6       = 106
    ARBITRARY_7       = 107
    ARBITRARY_8       = 108
    ARBITRARY_9       = 109
    ARBITRARY_10      = 110
    ARBITRARY_11      = 111
    ARBITRARY_12      = 112
    ARBITRARY_13      = 113
    ARBITRARY_14      = 114
    ARBITRARY_15      = 115
    """
    The system settings have a setting that limits the number of arbitrary
    waveforms so the rest of these are not always supported.

    ARBITRARY_16      = 116
    ARBITRARY_17      = 117
    ARBITRARY_18      = 118
    ARBITRARY_19      = 119
    ARBITRARY_20      = 120
    ARBITRARY_21      = 121
    ARBITRARY_22      = 122
    ARBITRARY_23      = 123
    ARBITRARY_24      = 124
    ARBITRARY_25      = 125
    ARBITRARY_26      = 126
    ARBITRARY_27      = 127
    ARBITRARY_28      = 128
    ARBITRARY_29      = 129
    ARBITRARY_30      = 130
    ARBITRARY_31      = 131
    ARBITRARY_32      = 132
    ARBITRARY_34      = 134
    ARBITRARY_35      = 135
    ARBITRARY_36      = 136
    ARBITRARY_37      = 137
    ARBITRARY_38      = 138
    ARBITRARY_39      = 139
    ARBITRARY_40      = 140
    ARBITRARY_41      = 141
    ARBITRARY_42      = 142
    ARBITRARY_43      = 143
    ARBITRARY_44      = 144
    ARBITRARY_45      = 145
    ARBITRARY_46      = 146
    ARBITRARY_47      = 147
    ARBITRARY_48      = 148
    ARBITRARY_49      = 149
    ARBITRARY_50      = 150
    ARBITRARY_51      = 151
    ARBITRARY_52      = 152
    ARBITRARY_53      = 153
    ARBITRARY_54      = 154
    ARBITRARY_55      = 155
    ARBITRARY_56      = 156
    ARBITRARY_57      = 157
    ARBITRARY_58      = 158
    ARBITRARY_59      = 159
    ARBITRARY_60      = 160
    """


class Frequency(enum.IntEnum):
    Hz  = 0
    KHz = 1
    MHz = 2
    mHz = 3
    uHz = 4


class UIMode(enum.IntEnum):
    # This enumeration is used with Command.UI_MODE (34)
    # It changes the position of the cursor on the screen

    # Waveform Screen
    WAVE_CH1             = 0
    WAVE_CH1_WAVEFORM    = 1
    WAVE_CH1_FREQUENCY   = 2
    WAVE_CH1_AMPLITUDE   = 3
    WAVE_CH1_OFFSET      = 4
    WAVE_CH1_DUTYCYCLE   = 5
    WAVE_CH1_PHASE       = 6
    WAVE_CH2             = 8
    WAVE_CH2_WAVEFORM    = 9
    WAVE_CH2_FREQUENCY   = 10
    WAVE_CH2_AMPLITUDE   = 11
    WAVE_CH2_OFFSET      = 12
    WAVE_CH2_DUTYCYCLE   = 13
    WAVE_CH2_PHASE       = 14

    # System Screen
    SYSTEM_SAVE_AND_LOAD = 32
    SYSTEM_SOUND         = 33
    SYSTEM_BRIGHTNESS    = 34
    SYSTEM_LANGUAGE      = 35
    SYSTEM_SYNC          = 36
    SYSTEM_ARB_MAX_NUM   = 37
    SYSTEM_RESTORE_DFT_SETTINGS = 38

    # Measure Screen
    MEASURE              = 64
    MEASURE_COUPLING     = 65
    MEASURE_GATE_TIME    = 66
    MEASURE_MODE         = 67

    COUNTER              = 72
    COUNTER_COUPLING     = 73
    COUNTER_MODE         = 74

    # Modulation Screen
    SWEEP_CH1            = 80
    SWEEP_CH2            = 88

    PULSE                = 96
    BURST                = 104


"""
# Get/Set ACTION doesn't seem to work super reliably and deterministically yet 
# so this is not exported
class Action(enum.Enum):
    # Weird settings, and it seems like not all of these settings are the same 
    # on all function generator models that use this JDS6600 protocol.
    #
    # As far as I can tell the 3rd value in this list controls whether the 
    # output channels (both) are enabled.
    COUNT_OFF = (1, 1, 1, 1)
    COUNT_ON  = (1, 0, 0, 0)

    SWEEP_OFF = (0, 0, 1, 0)
    SWEEP_ON  = (0, 1, 0, 0)

    PULSE_OFF = (0, 1, 1, 1)
    PULSE_ON  = (0, 0, 0, 1)

    BURST_OFF = (0, 0, 1, 1)
    BURST_ON  = (1, 0, 1, 1)
"""


class MeasureCoupling(enum.IntEnum):
    AC = 0
    DC = 1


class MeasureMode(enum.IntEnum):
    FREQUENCY = 0
    PERIOD    = 1


class SweepDirection(enum.IntEnum):
    RISE          = 0
    FALL          = 1
    RISE_AND_FALL = 2


class SweepMode(enum.IntEnum):
    LINEAR = 0
    LOG    = 1


class BurstMode(enum.IntEnum):
    MANUAL_TRIGGER = 0
    CH2_TRIGGER    = 1
    AC_TRIGGER     = 2
    DC_TRIGGER     = 3


class MeasureMode(enum.IntEnum):
    FREQUENCY = 0
    PERIOD    = 1


class MeasureMode(enum.IntEnum):
    FREQUENCY = 0
    PERIOD    = 1


__all__ = [
    'Command',
    'Channel',
    'Output',
    'Waveform',
    'Frequency',
    'UIMode',
    #'Action',
    'MeasureCoupling',
    'MeasureMode',
    'SweepDirection',
    'SweepMode',
    'BurstMode',
]
