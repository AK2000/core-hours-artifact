# GPU experiments with StarPU

This repository contains the scripts used to reproduce our GPU-based experiments using StarPU

## Installation

### To install all necessary dependencies for StarPU:

```bash
~/gpu_experiments$ bash Install_packages.sh
```

### Install Starpu

After connecting to a node with an NVIDIA GPU:
```bash
~/$ git clone https://gitlab.inria.fr/starpu/starpu.git 
~/$ cd starpu/
~/starpu$ ./autogen.sh
~/starpu$ ./configure --prefix=/path/to/starpu/folder/starpu --enable-maxcudadev=<NUM_GPUS>
~/starpu$ make -j 100
~/starpu$ make install
~/starpu$ sudo ldconfig
```
Replace <NUM_GPUS> with the number of GPUs available on your node.

## Running experiments

### Calibration

Calibration must be done on every new compute node before running experiments. Run the command below:
```bash
~/$ cd starpu/
~/starpu$ N=60 ; TILE_SIZE=2880 ; STARPU_SCHED=dmdar STARPU_MINIMUM_CLEAN_BUFFERS=0 STARPU_TARGET_CLEAN_BUFFERS=0 STARPU_NCPU=0 STARPU_NCUDA=<NUM_GPUS> STARPU_CALIBRATE=1 STARPU_CALIBRATE_MINIMUM=30 STARPU_NOPENCL=0 ./examples/cholesky/cholesky_implicit -size $((TILE_SIZE*N)) -nblocks $((N)) -niter 10
```
Replace <NUM_GPUS> with the number of GPUs on the node.

### Run the experiments

Then, to start the experiments do:
```bash
~/$ bash core-hours-artifact/gpu_experiments/run.sh <NUM_GPUS>
```
Replace <NUM_GPUS> with the number of GPUs you want to evaluate.

### Gathering the results

If you are using Grid'5000 (as we did), you can gather metrics like this:
```bash
~/$ curl 'https://api.grid5000.fr/stable/sites/<site>/metrics?job_id=<job_id>' > data.txt
~/gpu_experiments$ python3 parse_bmc.py data.txt results.csv
```
And replace <site> with the site used and <job_id> with your job's ID.

Note: The example provided above for collecting metrics is specific to Grid'5000. If you are using a different resource provider, the format and method for accessing energy metrics may vary.
