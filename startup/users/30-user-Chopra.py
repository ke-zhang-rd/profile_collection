import sys
import time


det = [pil1M, pdcurrent, pdcurrent1, pdcurrent2]

def bu(user_name, start_y, end_y, acq_t=2, meas_t=2):
    for i, y_val in enumerate(range(start_y, end_y+1, 50)):
        yield from bps.mv(piezo.y, y_val)
        name_fmt = 'nb{i}_pd_{pd}'
        det_exposure_time(acq_t, meas_t)
        
        yield from bps.mv(att1_10, 'Insert') 
        fs.open()
        time.sleep(0.3)
        pd_curr = pdcurrent2.value
        fs.close()
        yield from bps.mv(att1_10, 'Retract') 
        time.sleep(0.5)
        sample_name= name_fmt.format(i='%2.2d'%(1+i), pd='%5.5d'%pd_curr)
        sample_id(user_name=user_name, sample_name=sample_name)
        
        print(f'\n\t=== Sample:{user_name}_{sample_name} ===\n')

        yield from bp.count(det, num=1)
    



        
