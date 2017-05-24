from ophyd import ( Component as Cpt, ADComponent,
                    EpicsSignal, EpicsSignalRO,
                    ROIPlugin, StatsPlugin, ImagePlugin,
                    SingleTrigger, PilatusDetector)

from ophyd.areadetector.filestore_mixins import FileStoreBulkWrite

from ophyd.utils import set_and_wait
from filestore.handlers_base import HandlerBase
import fabio
import os


class PilatusFilePlugin(Device, FileStoreBulkWrite):
    file_path = ADComponent(EpicsSignalWithRBV, 'FilePath', string=True)
    file_number = ADComponent(EpicsSignalWithRBV, 'FileNumber')
    file_name = ADComponent(EpicsSignalWithRBV, 'FileName', string=True)
    file_template = ADComponent(EpicsSignalWithRBV, 'FileTemplate', string=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._datum_kwargs_map = dict()  # store kwargs for each uid

    def stage(self):
        global proposal_id
        global run_id
        current_sample = 'test1'
        data_path = '/data/images/'
        set_and_wait(self.file_template, '%s%s_%6.6d_'+self.parent.detector_id+'.tif', timeout=99999)

        set_and_wait(self.file_path, data_path, timeout=99999)
        set_and_wait(self.file_name, current_sample, timeout=99999)
        
        super().stage()
        res_kwargs = {'template': self.file_template.get(),
                      'filename': self.file_name.get(),
                      'frame_per_point': self.get_frames_per_point(),
                      'initial_number': self.file_number.get()}
        self._resource = self.fs.insert_resource('AD_CBF', data_path, res_kwargs, root="/")
        
       
    def unstage(self):
        super().unstage()
        
    def get_frames_per_point(self):
        return 1


class SMIPilatus(SingleTrigger, PilatusDetector):
    file = Cpt(PilatusFilePlugin, suffix="cam1:",
               write_path_template="", fs=db.fs)

    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')

    stats1 = Cpt(StatsPlugin, 'Stats1:')
    stats2 = Cpt(StatsPlugin, 'Stats2:')
    stats3 = Cpt(StatsPlugin, 'Stats3:')
    stats4 = Cpt(StatsPlugin, 'Stats4:')

    file_num = ADComponent(EpicsSignalWithRBV, 'cam1:FileNumber')
    # last_file_num = file_num.get() - 1

    def __init__(self, *args, **kwargs):
        self.detector_id = kwargs.pop('detector_id')
        super().__init__(*args, **kwargs)
'''
def pil300KW_number_reset(val):
    pil300KW.file.file_number.put(val)

def pil300KW_ct_time(exp):
    pil300KW.cam.acquire_time.put(exp)
'''
def set_pilatus_defaults(det):
    "Choose which attributes to read per-step (read_attrs) or per-run (configuration attrs)."
    det.file.read_attrs = []
    det.read_attrs = ['file', 'stats1', 'stats2', 'stats3', 'stats4']  # , 'last_file_num']
    for stats in [det.stats1, det.stats2, det.stats3, det.stats4]:
        stats.read_attrs = ['total']
    det.cam.read_attrs = []
    det.cam.configuration_attrs = ['acquire_time', 'acquire_period', 'num_images', 'threshold_energy']

#pil300KW = SMIPilatus("XF:12IDC-ES:2{Det:300KW}", name="pil300KW", detector_id="WAXS")
pil1M = SMIPilatus("XF:12IDC-ES:2{Det:1M}", name="pil1M", detector_id="SAXS")
#pilatus_detectors = [pil300KW, pil1M]
pilatus_detectors = [pil1M]


for det in pilatus_detectors:
    set_pilatus_defaults(det)
