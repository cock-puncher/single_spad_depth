#!/usr/bin/env bash
set -euo pipefail

python eval_nyuv2.py -c configs/dorn/mde.yml "$@"
python eval_nyuv2.py -c configs/densedepth/mde.yml "$@"
