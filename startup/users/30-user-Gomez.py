def NEXAFS_Fe_edge(t=0.5, name='sample1'):
        dets = [pil300KW]
        #name = 'Kapton_NEXAFS_1_gvopen_wa70_'
        #x = [8800]

        energies = np.linspace(7100, 7150, 51)

        #for name, x in zip(names, x):
        #bps.mv(piezo.x, x)
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV_xbpm{xbpm}'
        for e in energies:                              
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
            sample_id(user_name='SR', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 7100)
        #name_fmt = '{sample}_2430eV_postmeas_xbpm{xbpm}'
        #sample_name = name_fmt.format(sample=name, xbpm = '%3.1f'%xbpm3.sumY.value)
        #sample_id(user_name='GF', sample_name=sample_name)
        #print(f'\n\t=== Sample: {sample_name} ===\n')
        #yield from bp.count(dets, num=1)


def SAXS_Fe_edge(t=0.5):
        dets = [pil1M]
        names = ['Ca10_2_SAXS_sdd5_1s_redo_','Ca2_2_SAXS_sdd5_1s_redo_', 'Ca2_4_SAXS_sdd5_1s_redo_', 'PBS_2_SAXS_sdd5_1s_redo_']
        names1 = ['Ca10_2_NEXAFS_wa0_redo_','Ca2_2_NEXAFS_wa0_redo_', 'Ca2_4_NEXAFS_wa0_redo_', 'PBS_2_NEXAFS_wa0_redo_']

        xs = [-36600, -10600, 15400, 41100]
        ys = [-1050, -1050, -1050, -1050]
        energies = [7100, 7110, 7114, 7115, 7118, 7120, 7125, 7140]

        for i, (name, name1, x, y) in enumerate(zip(names, names1, xs, ys)):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            
            yield from NEXAFS_Fe_edge(t=1, name=name1)
            dets = [pil1M]

            det_exposure_time(t,t) 
            xsss = [x+400, x + 900, x + 1200]
            for j, xss in enumerate(xsss):
                yield from bps.mv(piezo.x, xss)
                for e in energies: 
                    name_fmt = '{sample}_pos{pos}_{energy}eV_xbpm{xbpm}'
                             
                    yield from bps.mv(energy, e)
                    sample_name = name_fmt.format(sample=name, pos = '%2.2d'%j, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
                    sample_id(user_name='SR', sample_name=sample_name)
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 7100)
                name_fmt = '{sample}_pos{pos}_7100eV_postmeas_xbpm{xbpm}'
                sample_name = name_fmt.format(sample=name, pos = '%2.2d'%j, xbpm = '%3.1f'%xbpm3.sumY.value)
                sample_id(user_name='GF', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)



def NEXAFS_Ag_edge(t=0.5):
        dets = [pil300KW]
        name = 'N2_redo_GINEXAFS_wa75_'
        #x = [8800]

        energies = np.linspace(3340, 3390, 51)

        #for name, x in zip(names, x):
        #bps.mv(piezo.x, x)
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV_xbpm{xbpm}'
        for e in energies:                              
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
            sample_id(user_name='SR', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)
            yield from bps.sleep(2)


        yield from bps.mv(energy, 3340)
        yield from bps.sleep(10)




def GISAXS_Ca_edge(t=0.5):
        dets = [pil300KW]
        names = ['O_9_gisaxs','O_8_gisaxs','O_7_gisaxs','O_6_gisaxs','O_5_gisaxs','O_4_gisaxs','O_3_gisaxs','O_2_gisaxs','O_1_gisaxs','Si_last_gisaxs']
        xs = [-50000, -38500, -22500, -11500, 500, 15000, 27000, 41000, 50000, 31400]
        zs = [700, 0, -800, 400, 1900, -2000, -1000, 300, -600, -800]

        
        energies = [4030, 4050, 4055, 4075]
        det_exposure_time(t,t) 
       
        name_fmt = '{sample}_{energy}eV_ai{ai}_xbpm{xbpm}_wa{wa}'
        angles = [0.38, 0.4]
        wax = [0, 6.5, 13]
        
        th_0 = piezo.th.position
        for x, z, name in zip(xs, zs, names):
            yield from bps.mv(piezo.th, th_0)    

            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.z, z)

            yield from bps.mv(GV7.open_cmd, 1 )
            time.sleep(5)

            yield from bps.mv(GV7.open_cmd, 1 )
            yield from alignement_gisaxs(0.3)
            yield from bps.mv(att2_11, 'Insert')

            yield from bps.mv(GV7.close_cmd, 1 )
            time.sleep(5)
            yield from bps.mv(att2_11, 'Insert')

            yield from bps.mv(GV7.close_cmd, 1 )

            th_0 = piezo.th.position
            for wa in wax:
                yield from bps.mv(waxs, wa)            
                for k, e in enumerate(energies): 
                    yield from bps.mv(energy, e) 
                    for alpha_i in angles:
                        yield from bps.mv(piezo.th, th_0 + alpha_i)    
                        sample_name = name_fmt.format(sample=name, energy=e, ai='%3.2f'%alpha_i, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wa)
                        sample_id(user_name='SR', sample_name=sample_name)
                        print(f'\n\t=== Sample: {sample_name} ===\n')
                        yield from bp.count(dets, num=1)                                
                
                yield from bps.mv(energy, 4050)
                yield from bps.mv(energy, 4030)




def SAXS_Ca_edge_hyd(t=0.5):
        dets = [pil1M]
        name = 'hyd_cell_blank'


        energies = [4030, 4050, 4055, 4075]
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_sp{sp}'
        x_pos = piezo.x.position
        y_pos = piezo.y.position
        
        for k, e in enumerate(energies):                              
            yield from bps.mv(energy, e)
            yield from bps.mv(piezo.x, x_pos + k*500)
            
            for i in range(0, 5, 1):
                yield from bps.mv(piezo.y, y_pos + i*200)
   
                sample_name = name_fmt.format(sample=name, energy=e, sp='%2.2d'%i, xbpm = '%3.1f'%xbpm3.sumY.value)
                sample_id(user_name='JDM', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
                
            yield from bps.mv(piezo.y, y_pos)
            
        yield from bps.mv(energy, 4050)
        yield from bps.mv(energy, 4030)

def SAXS_Ca_edge_hyd_onespot(t=0.5):
        dets = [pil1M]
        name = 'hyd_cell_blank_onespot2'


        energies = [4030, 4040, 4050, 4055, 4075]
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_sp{sp}'
        y_pos = piezo.y.position
        
        for k, e in enumerate(energies):                              
            yield from bps.mv(energy, e)
            
            for i in range(0, 5, 1):
                yield from bps.mv(piezo.y, y_pos + i*200)
   
                sample_name = name_fmt.format(sample=name, energy=e, sp='%2.2d'%i, xbpm = '%3.1f'%xbpm3.sumY.value)
                sample_id(user_name='JDM', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
                
            yield from bps.mv(piezo.y, y_pos)
            
        yield from bps.mv(energy, 4050)
        yield from bps.mv(energy, 4030)



def SAXS_Ca_edge_dry1(t=1):
    dets = [pil300KW, pil1M]
    name = 'hyd_cell_blank2'

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t,t) 
    name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_wa{wa}'
    wa = [0.0, 6.5, 13.0]


    yield from bps.mv(GV7.close_cmd, 1 )
    time.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1 )

    for wax in wa:
        yield from bps.mv(waxs, wax)
        for k, e in enumerate(energies):                              
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wax)
            sample_id(user_name='JDM', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)
                        
        yield from bps.mv(energy, 4050)
        yield from bps.mv(energy, 4030)

    for wax in wa[::-1]:
        yield from bps.mv(waxs, wax)

        name_fmt = '{sample}_4030eV_postmeas_xbpm{xbpm}_wa{wa}'
        sample_name = name_fmt.format(sample=name, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wax)
        sample_id(user_name='OS', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.count(dets, num=1)
    
    sample_id(user_name='test', sample_name='test')

        


def SAXS_Ca_edge_dry_special1(t=1):
    dets = [pil300KW]
    names = ['O5_chl_4']
    x_s = [-44500]
    y_s = [-1200]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t,t) 
    name_fmt = '{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}'
    wa = [0.0, 6.5, 13.0]


    yield from bps.mv(GV7.close_cmd, 1 )
    time.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1 )

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        ys = np.linspace(y, y + 250, 5)
        xs = np.linspace(x, x - 400, 3)
               
        yss, xss = np.meshgrid(ys, xs)
        yss = yss.ravel()
        xss = xss.ravel()

        for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                yield from bps.mv(piezo.x, xsss)
                yield from bps.mv(piezo.y, ysss)
                name_new = name + 'pos%2.2d'%pos
                yield from NEXAFS_Ca_edge_special(t=0.5, name=name_new)

        for wax in wa:
            yield from bps.mv(waxs, wax)

            for k, e in enumerate(energies):                              
                yield from bps.mv(energy, e)

                for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                    yield from bps.mv(piezo.x, xsss)
                    yield from bps.mv(piezo.y, ysss)

                    sample_name = name_fmt.format(sample=name, energy=e, posi='%2.2d'%pos ,wa='%2.1f'%wax, xbpm = '%3.1f'%xbpm3.sumY.value)
                    sample_id(user_name='JDM', sample_name=sample_name)
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    yield from bp.count(dets, num=1)
                                
                yield from bps.mv(energy, 4050)
                yield from bps.mv(energy, 4030)

        for wax in wa[::-1]:
            yield from bps.mv(waxs, wax)

            for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                yield from bps.mv(piezo.x, xsss)
                yield from bps.mv(piezo.y, ysss)

                name_fmt = '{sample}_postmeas_4030eV_pos{posi}_wa{wa}_xbpm{xbpm}'
                sample_name = name_fmt.format(sample=name, posi='%2.2d'%pos, wa='%2.1f'%wax, xbpm = '%3.1f'%xbpm3.sumY.value)
                sample_id(user_name='JDM', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
    
    sample_id(user_name='test', sample_name='test')



def SAXS_Ca_edge_dry_special2(t=1):
    dets = [pil300KW, pil1M]
    names = ['O5_ut_2','O5_ut_3','O5_ut_4', 'O5_ca_1', 'O5_ca_2', 'O5_ca_3', 'O5_chl_1', 'O5_chl_2', 'O5_chl_3']
    x_s = [31500, 25000, 18000, 5400, 100, -5400, -22600, -30600, -38600]
    y_s = [-2200, -1400, -2000, -2000, -2000, -2000, -800, -2000, -2000]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t,t) 
    name_fmt = '{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}'
    wa = [0.0, 6.5, 13.0]

    yield from bps.mv(GV7.open_cmd, 1 )
    time.sleep(1)
    yield from bps.mv(GV7.open_cmd, 1 )

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        ys = np.linspace(y, y + 500, 2)
        xs = np.linspace(x, x - 500, 2)

        yss, xss = np.meshgrid(ys, xs)
        yss = yss.ravel()
        xss = xss.ravel()
        yield from NEXAFS_Ca_edge_special(t=0.5, name=name)

        for wax in wa:

            yield from bps.mv(waxs, wax)

            for k, e in enumerate(energies):                              
                yield from bps.mv(energy, e)

                for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                    yield from bps.mv(piezo.x, xsss)
                    yield from bps.mv(piezo.y, ysss)

                    sample_name = name_fmt.format(sample=name, energy=e, posi='%1.1d'%pos ,wa='%2.1f'%wax, xbpm = '%3.1f'%xbpm3.sumY.value)
                    sample_id(user_name='JDM', sample_name=sample_name)
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    yield from bp.count(dets, num=1)
                                
                yield from bps.mv(energy, 4050)
                yield from bps.mv(energy, 4030)
        
        wa = [0.0, 6.5, 13.0]
        for wax in wa[::-1]:
            yield from bps.mv(waxs, wax)

            for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                yield from bps.mv(piezo.x, xsss)
                yield from bps.mv(piezo.y, ysss)

                name_fmt = '{sample}_postmeas_4030eV_pos{posi}_wa{wa}_xbpm{xbpm}'
                sample_name = name_fmt.format(sample=name, posi='%2.2d'%pos, wa='%2.1f'%wax, xbpm = '%3.1f'%xbpm3.sumY.value)
                sample_id(user_name='JDM', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
    
    sample_id(user_name='test', sample_name='test')


def NEXAFS_Ca_edge_special(t=0.5, name='test'):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]

    energies = np.linspace(4030, 4100, 71)

    det_exposure_time(t,t) 
    name_fmt = 'nexafs_{sample}_{energy}eV_xbpm{xbpm}'
    for e in energies:                              
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
        sample_id(user_name='JDM', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4075)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 4050)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 4030)

    sample_id(user_name='test', sample_name='test')


def night_shift_run(t=1):
    yield from SAXS_Ca_edge_dry_special1(t=0.5)
    yield from bps.sleep(10)
    yield from SAXS_Ca_edge_dry_special2(t=0.5)





def run_saxs_nexafs(t=1):
    yield from nexafs_prep_multisample(t=0.5)
    yield from bps.sleep(10)
    yield from saxs_prep_multisample(t=0.5)


def nexafs_prep_multisample(t=1):
    names = ['NEXAFS_WT_CH24_1_spot3','NEXAFS_WT_CH24_2_spot3','NEXAFS_WT_CH24_3_spot3', 'NEXAFS_xxt1xxt2_CH24_Ca_1_spot1']
    x_s = [27400, 20800, 14700, -13250]
    y_s = [300, 300, 200, -1300]

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        yield from NEXAFS_Ca_edge_multi(t=0.5, name=name)
    
    sample_id(user_name='test', sample_name='test')


def saxs_prep_multisample(t=1):
    dets = [pil300KW, pil1M]
    names = ['xxt1xxt2_CH24_Ca_1_spot1', 'xxt1xxt2_CH24_Ca_1_spot2', 'xxt1xxt2_CH24_Ca_1_spot3', 'xxt1xxt2_CH24_Ca_3_spot3', 'xxt1xxt2_CH24_Ca_3_spot2', 'xxt1xxt2_CH24_Ca_3_spot1']
    x_s = [-13250, -13250, -13250, -27550, -27250, -27490]
    y_s = [-1400, -800, 100, 300, -800, -1600]
 
    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t,t) 
    name_fmt = '{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}'
    wa = [0, 6.5, 13.0] #19.5


    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        for wax in wa:
            yield from bps.mv(waxs, wax)
            for k, e in enumerate(energies):                              
                yield from bps.mv(energy, e)
                name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_wa{wa}'

                sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wax)
                sample_id(user_name='OS', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
                            
            yield from bps.mv(energy, 4050)
            yield from bps.mv(energy, 4030)

        for wax in wa[::-1]:
            yield from bps.mv(waxs, wax)

            name_fmt = '{sample}_4030eV_postmeas_xbpm{xbpm}_wa{wa}'
            sample_name = name_fmt.format(sample=name, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wax)
            sample_id(user_name='OS', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        sample_id(user_name='test', sample_name='test')


def NEXAFS_Ca_edge_multi(t=0.5, name='test'):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]

    energies = np.linspace(4030, 4150, 121)

    det_exposure_time(t,t) 
    name_fmt = '{sample}_{energy}eV_xbpm{xbpm}'
    for e in energies:                              
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
        sample_id(user_name='OS', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4125)
    yield from bps.mv(energy, 4100)        
    yield from bps.mv(energy, 4075)
    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)

    sample_id(user_name='test', sample_name='test')






def NEXAFS_Ca_edge(t=0.5,):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]
    name = 'hyd_cell_blank_sp2'
    #x = [8800]

    energies = np.linspace(4030, 4150, 121)

    #for name, x in zip(names, x):
    #bps.mv(piezo.x, x)
    det_exposure_time(t,t) 
    name_fmt = '{sample}_{energy}eV_xbpm{xbpm}'
    for e in energies:                              
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
        sample_id(user_name='JDM', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4125)
    yield from bps.mv(energy, 4100)        
    yield from bps.mv(energy, 4075)
    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)
    name_fmt = '{sample}_4030.0eV_postmeas'
    sample_name = name_fmt.format(sample=name)
    sample_id(user_name='OS', sample_name=sample_name)
    print(f'\n\t=== Sample: {sample_name} ===\n')
    yield from bp.count(dets, num=1)

    sample_id(user_name='test', sample_name='test')







def NEXAFS_P_edge(t=0.5):
        yield from bps.mv(waxs, 30)
        dets = [pil300KW]
        name = 'NEXAFS_PBS1_Pedge_nspot1'

        energies = np.linspace(2140, 2180, 41)
        energies_back = np.linspace(2180, 2140, 41)
        
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV_xbpm{xbpm}'
        for e in energies:                              
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
            sample_id(user_name='SR', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        
        for e in energies_back:                              
            yield from bps.mv(energy, e)
            time.sleep(2)


def NEXAFS_S_edge(t=0.5):
        yield from bps.mv(waxs, 30)
        dets = [pil300KW]
        name = 'NEXAFS_A12_Sedge'

        energies = np.linspace(2430, 2500, 71)
        energies_back = np.linspace(2500, 2430, 36)
        
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV_xbpm{xbpm}'
        for e in energies:                              
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value)
            sample_id(user_name='SR', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        
        for e in energies_back:                              
            yield from bps.mv(energy, e)
  
def waxs_S_edge(t=1):
    dets = [pil300KW]
    

    names = ['A41']
    x = [-28200]
    y = [1600]
    
    names1 = ['P3HT']
    x1 = [-38700]
    y1 = [900]
    
    energies = np.linspace(2456, 2500, 23)
    Ys = np.linspace(900, 2200, 23)
    waxs_arc = [0, 19.5, 4]
    
    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV'
        for e in energies:                              
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name='SR', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.scan(dets, waxs, *waxs_arc)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2480)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2460)
        yield from bps.mv(energy, 2456)

        name_fmt = '{sample}_2456eV_postmeas'
        sample_name = name_fmt.format(sample=name)
        sample_id(user_name='SR', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.scan(dets, waxs, *waxs_arc)


def waxs_S_edge(t=1):
    dets = [pil300KW]
    
    names1 = ['P3HT']
    x1 = [-38700]
    y1 = [900]
    
    energies = [2460, 2465, 2470, 2474, 2475, 2476, 2478, 2480]
    Ys = np.linspace(900, 2200, 8)

    waxs_arc = [0, 39, 7]
    for name, xs, ys in zip(names1, x1, y1):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        det_exposure_time(t,t) 
        name_fmt = '{sample}_{energy}eV'
        for e, ys in zip(energies, Ys):                              
            yield from bps.mv(energy, e)
            yield from bps.mv(piezo.y, ys)
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name='GF', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.scan(dets, waxs, *waxs_arc)


        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2460)

        
        name_fmt = '{sample}_2460eV_postmeas'
        sample_name = name_fmt.format(sample=name)
        sample_id(user_name='SR', sample_name=sample_name)
        print(f'\n\t=== Sample: {sample_name} ===\n')
        yield from bp.scan(dets, waxs, *waxs_arc)

    


        
def trans_sulf(en1, en2, step):
        eners = np.linspace(en1, en2, step)
        for e in eners:
                yield from bps.mv(energy, e)
                time.sleep(10)
                 

