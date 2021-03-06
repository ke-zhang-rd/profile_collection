def nexafs_S_edge_terry(t=1):
    dets = [pil300KW]
    
    
    names = ['pedotpss_1_gisaxs']
    x = [0]
    y = [7169.288]
    
    #names = ['N2200_2_nexafs']
    #x = [34800]
    #y = [2000]
    #energies = np.arange(2450, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist()

    energies = np.arange(2450, 2470, 5).tolist() + np.arange(2470, 2474, 0.5).tolist() + np.arange(2474, 2482, 0.25).tolist() + np.arange(2482, 2500, 1).tolist()+ np.arange(2500, 2531, 5).tolist()
    waxs_arc = [60]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)    

            det_exposure_time(t,t) 
            name_fmt = '{sample}_{energy}eV_bpm{xbpm}'
            for e in energies: 
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%4.3f'%bpm)
                sample_id(user_name='GF', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)

       
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)



def waxs_S_edge_terry(t=1):
    dets = [pil300KW]
    

    names = ['c1_03']
    x = [-23000]
    
    energies = np.arange(2450, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist()
    waxs_arc = np.linspace(0, 26, 5)

    for name, xs in zip(names, x):
        yield from bps.mv(piezo.x, xs)

        xss = np.linspace(xs, xs - 8000, 57)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)    

            det_exposure_time(t,t) 
            name_fmt = '{sample}_{energy}eV_wa{wax}_bpm{xbpm}'
            for e, xsss in zip(energies, xss): 
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
                sample_id(user_name='GF', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)

       
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)



def waxs_S_edge_terry1(t=1):
    dets = [pil300KW, pil1M]
    

    names = ['p3HT_1_saxs', 'N2200_1_saxs', 'PCPDTBT_1_saxs', 'p3N2CN_1_saxs', 'P3N2_1_saxs', 'p3C61BM_1_saxs', 'AD0_1_saxs', 'AD1_1_saxs', 'AD1_2_saxs',
    'AD2_1_saxs', 'AD3_1_saxs', 'AD4_1_saxs', 'AD5_1_saxs', 'AD6_1_saxs', 'AD7_1_saxs']
    x = [41600, 34600, 28200, 23200, 17800, 12400, 6500, 1000, 2000, -3200, -9000, -13700, -19900, -24900, -29900]
    y = [1400,  1400,  1100,  1100,  1600,  1800,  1900, 1100, 2700, 2000,  1700,  2600,  2400, 2000, 1800]

    energies = [2450, 2474, 2475, 2477, 2484, 2530]
    waxs_arc = np.linspace(0, 78, 13)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)    
        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t,t) 
            name_fmt = '{sample}_{energy}eV_wa{wax}_bpm{xbpm}'
            for e in energies: 
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
                sample_id(user_name='TM', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)

       
            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)




def giwaxs_S_edge_terry(t=1):
    dets = [pil300KW, pil1M]
    

    names = ['pedotpss_1_gisaxs']
    x = [0 ]
    
    energies = [2450, 2474, 2475, 2477, 2484, 2530]
    waxs_arc = np.linspace(0, 78, 13)
    ais0, ys0 = [], []
    for xs in x:
        yield from bps.mv(piezo.x, xs)

        yield from alignement_gisaxs(angle = 0.35)
        ais0 = ais0 + [piezo.th.position]
        ys0 = ys0 + [piezo.y.position]
        print(piezo.th.position, piezo.y.position)


    yield from bps.mv(att2_9, 'Insert')
    yield from bps.sleep(1)
    yield from bps.mv(att2_9, 'Insert')
    yield from bps.sleep(1)


    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)    
        for name, xs, ai0, ys in zip(names, x, ais0, ys0):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.th, ai0)

            yield from bps.mv(piezo.th, ai0 + 0.7)

            det_exposure_time(t,t) 
            name_fmt = '{sample}_{energy}eV_ai0.7_wa{wax}_bpm{xbpm}'
            for e in energies: 
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
                sample_id(user_name='TM', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)

       
            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)






def WAXS_S_edge_Gomez_night(t=1):
    dets = [pil300KW, pil1M]
    names = ['PA1-3']
    x_s = [41200]
    y_s = [1300]

    energies = [2456, 2464, 2475, 2477, 2490, 2492]
    det_exposure_time(t,t) 

    wa = np.linspace(0, 45.5, 8)

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        ys = np.linspace(y, y + 500, 7)

        yield from bps.mv(piezo.y, ys[0])
        yield from NEXAFS_S_edge_Gomez_night(t=0.5, name=name)


    for wax in wa:
        yield from bps.mv(waxs, wax)

        for x, y, name in zip(x_s, y_s, names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            ys = np.linspace(y, y + 500, 7)

            for k, (e, ysss) in enumerate(zip(energies, ys[1:])):                              
                yield from bps.mv(energy, e)
                yield from bps.mv(piezo.y, ysss)
                name_fmt = '{sample}_{energy}eV_wa{wa}_xbpm{xbpm}'

                sample_name = name_fmt.format(sample=name, energy=e, wa='%2.1f'%wax, xbpm = '%3.1f'%xbpm3.sumY.value)
                sample_id(user_name='GZ', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
                                
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2456)
            yield from bps.sleep(2)
    
    wa = [0, 6.5, 13.0]
    for wax in wa[::-1]:
        yield from bps.mv(waxs, wax)
        for x, y, name in zip(x_s, y_s, names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
           
            ys = np.linspace(y, y + 500, 7)

            yield from bps.mv(piezo.y, ys[1])

            name_fmt = '{sample}_postmeas_2456eV_wa{wa}_xbpm{xbpm}'
            sample_name = name_fmt.format(sample=name, wa='%2.1f'%wax, xbpm = '%3.1f'%xbpm3.sumY.value)
            sample_id(user_name='GZ', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)
    
    sample_id(user_name='test', sample_name='test')


def NEXAFS_S_edge_Gomez_night(t=0.5, name='test'):

    yield from bps.mv(waxs, 60)
    dets = [pil300KW]

    energies = np.linspace(2430, 2500, 71)

    det_exposure_time(t,t) 
    name_fmt = 'nexafs_{sample}_{energy}eV_xbpm{xbpm}'
    for e in energies:                              
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
        sample_id(user_name='GZ', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2470)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(2)

    sample_id(user_name='test', sample_name='test')

def WAXS_S_edge_rad_dmg_test(t=1):
    dets = [pil300KW, pil1M]
    names = ['PA1-3_rad_dmg_test']

    det_exposure_time(t,t) 

    wa = np.linspace(0, 13.0, 3)

    for i in range(0, 5, 1):
        print(i)
        for wax in wa:
            print(wax)
            print(2456)

            yield from bps.mv(waxs, wax)
            yield from bps.mv(energy, 2456)
            name_fmt = '{sample}_{energy}eV_rep{rep}_wa{wa}'

            sample_name = name_fmt.format(sample=names[0], energy=2456, rep=i, wa='%2.1f'%wax)
            sample_id(user_name='GZ', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

    sample_id(user_name='test', sample_name='test')
