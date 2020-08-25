#!/usr/bin/env python3

import numpy as np
import configargparse
from pathlib import Path
from pdb import set_trace

# MDEs
from .mde import MDE

from ..data.nyu_depth_v2.nyuv2_dataset import NYUV2_CROP
from ..experiment import ex


@ex.config('MDEMedian')
def cfg():
    parser = configargparse.ArgParser(default_config_files=[str(Path(__file__).parent/'mde_median.cfg')])
    parser.add('--gt-key', default='depth_cropped')
    args, _ = parser.parse_known_args()
    return vars(args)

@ex.setup('MDEMedian')
def setup(config):
    mde_model = ex.get_and_configure('MDE')
    return MDEMedian(mde_model, gt_key=config['gt_key'])

@ex.entity
class MDEMedian:
    def __init__(self, mde_model, gt_key, crop=NYUV2_CROP):
        self.mde_model = mde_model
        self.gt_key = gt_key
        self.crop = crop

    def __call__(self, data):
        init = self.mde_model(data)
        if self.crop is not None:
            # Set median based on crop (makes a big difference)
            init_median = np.median(init[...,
                                         self.crop[0]:self.crop[1],
                                         self.crop[2]:self.crop[3]])
        else:
            init_median = np.median(init)
        pred = init * (np.median(data[self.gt_key])/init_median)
        return pred

if __name__ == '__main__':
    from pdb import set_trace
    model = ex.get_and_configure('MDEMedian')
