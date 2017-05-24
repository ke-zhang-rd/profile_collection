import time as ttime
import os
from ophyd import (PVPositioner, EpicsSignal, EpicsSignalRO, EpicsMotor,
                   Device, Signal, PseudoPositioner, PseudoSingle)
from ophyd.utils.epics_pvs import set_and_wait
from ophyd.ophydobj import StatusBase, MoveStatus
from ophyd import Component as Cpt
from scipy.interpolate import InterpolatedUnivariateSpline
from epics import (caput, caget)


ring_current = EpicsSignalRO('SR:C03-BI{DCCT:1}I:Real-I', name='ring_current')
ring_ops = EpicsSignal('SR-OPS{}Mode-Sts', name='ring_ops', string=True)
mstr_shutter_enable = EpicsSignalRO('SR-EPS{PLC:1}Sts:MstrSh-Sts', name='mstr_shutter_enable')
ivu_permit = EpicsSignalRO('XF:12ID-CT{}Prmt:Remote-Sel', name='ivu_permit')
smi_shutter_enable = EpicsSignalRO('SR:C12-EPS{PLC:1}Sts:ID_BE_Enbl-Sts', name='smi_shutter_enable')

def ring_check():
	if ring_ops.value == 'Operations' and mstr_shutter_enable.value == 1 and smi_shutter_enable.value == 1 and ivu_permit.value == 1:
		ring_ok=1
		print('SR ring status: Operations, shutters and IVU enabled. All is OK')
	else:
		ring_ok=0
		print('SR ring status alert: check if shutters and/or IVU enabled! ')		
	return ring_ok

def wait_for_ring():
	ring_ok=ring_check()
	if ring_ok==0:
		while ring_ok==0:
			print('SR ring is down and/or beamline shutters and IVU not enabled...checking again in 5 minutes.')
			sleep(300)
			ring_ok=ring_check()
	if ring_ok==1: pass


class EpicsSignalOverridePrecRO(EpicsSignalRO):
    def __init__(self, *args, precision=4, **kwargs):
        self._precision = precision
        super().__init__(*args, **kwargs)

    @property
    def precision(self):
        return self._precision

class EpicsSignalOverridePrec(EpicsSignal):
    def __init__(self, *args, precision=4, **kwargs):
        self._precision = precision
        super().__init__(*args, **kwargs)

    @property
    def precision(self):
        return self._precision



class UndulatorGap(PVPositioner):
    # positioner signals
    setpoint = Cpt(EpicsSignalOverridePrec, '-Mtr:2}Inp:Pos')
    readback = Cpt(EpicsSignalOverridePrecRO, '-LEnc}Gap')
    stop_signal = Cpt(EpicsSignal, '-Mtr:2}Pos:STOP')
    actuate = Cpt(EpicsSignal, '-Mtr:2}Sw:Go')
    actuate_value = 1
    done = Cpt(EpicsSignalRO, '-Mtr:2}Sw:Serv-On')
    done_value = 0

    # correction function signals, need to be merged into single object
    corrfunc_en = Cpt(EpicsSignal, '-MtrC}EnaAdj:out')
    corrfunc_dis = Cpt(EpicsSignal, '-MtrC}DisAdj:out')
    corrfunc_sta = Cpt(EpicsSignal, '-MtrC}AdjSta:RB')

    # brake status
    # brake_on = Cpt(EpicsSignalRO, '-Mtr:2}Rb:Brk')

ivugap = UndulatorGap('SR:C12-ID:G1{IVU:1', name='ivugap',
                read_attrs=['readback', 'setpoint'],
                configuration_attrs=['corrfunc_sta',
                                     'corrfunc_dis',
                                     'corrfunc_en'])

class UndulatorElev(PVPositioner):
    # positioner signals
    setpoint = Cpt(EpicsSignalOverridePrec, '-Mtr:1}Inp:Pos')
    readback = Cpt(EpicsSignalOverridePrecRO, '-LEnc}VOffset')
    stop_signal = Cpt(EpicsSignal, '-Mtr:1}Pos:STOP')
    actuate = Cpt(EpicsSignal, '-Mtr:1}Sw:Go')
    actuate_value = 1
    done = Cpt(EpicsSignalRO, '-Mtr:1}Sw:Serv-On')
    done_value = 0

ivuelev = UndulatorElev('SR:C12-ID:G1{IVU:1', name='ivuelev',
                read_attrs=['readback', 'setpoint'],
                configuration_attrs=[])





