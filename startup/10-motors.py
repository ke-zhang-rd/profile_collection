from ophyd import EpicsMotor, EpicsSignalRO, EpicsSignal, Device, Component as Cpt, PseudoPositioner


########## motor classes ##########
class MotorCenterAndGap(Device):
    "Center and gap using Epics Motor records"
    xc = Cpt(EpicsMotor, '-Ax:XC}Mtr')
    yc = Cpt(EpicsMotor, '-Ax:YC}Mtr')
    xg = Cpt(EpicsMotor, '-Ax:XG}Mtr')
    yg = Cpt(EpicsMotor, '-Ax:YG}Mtr')

class Blades(Device):
    "Actual T/B/O/I and virtual center/gap using Epics Motor records"
    tp = Cpt(EpicsMotor, '-Ax:T}Mtr')
    bt = Cpt(EpicsMotor, '-Ax:B}Mtr')
    ob = Cpt(EpicsMotor, '-Ax:O}Mtr')
    ib = Cpt(EpicsMotor, '-Ax:I}Mtr')
    xc = Cpt(EpicsMotor, '-Ax:XCtr}Mtr')
    yc = Cpt(EpicsMotor, '-Ax:YCtr}Mtr')
    xg = Cpt(EpicsMotor, '-Ax:XGap}Mtr')
    yg = Cpt(EpicsMotor, '-Ax:YGap}Mtr')
    
class DetMortor(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')
    
class SAXSBeamStop(Device):
    x = Cpt(EpicsMotor, 'IBB}Mtr')
    pad = Cpt(EpicsMotor, 'OBT}Mtr')
    y = Cpt(EpicsMotor, 'IBM}Mtr')    
    
 
## SAXS det position 
SAXS =   DetMortor(   'XF:12IDC-ES:2{Det:1M-Ax:', name='SAXS'   )
## stages for SAXS beamstops
SBS = SAXSBeamStop( 'XF:12IDC-ES:2{BS:SAXS-Ax:', name = 'SBS' ) 
 
  

    
