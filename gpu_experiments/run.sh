ngpu=$1
TAILLE_TUILE=2880 ; N=50 ; STARPU_NOPENCL=0 STARPU_NCPU=0 STARPU_NCUDA=$((ngpu)) STARPU_SCHED=dmdas ./starpu/examples/cholesky/cholesky_implicit -size $((TAILLE_TUILE*N)) -nblocks $((N)) -niter 10
