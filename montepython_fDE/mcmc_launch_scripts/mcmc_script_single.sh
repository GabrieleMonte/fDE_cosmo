#!/bin/bash
#SBATCH -J launch_mcmc           # Job name
#SBATCH -o sbatch_logs/out/launcher.o%j       # Name of stdout output file
#SBATCH -e sbatch_logs/err/launcher.e%j       # Name of stderr error file
#SBATCH -p normal          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes (must be 1 for serial)
#SBATCH -c 20
#SBATCH -n 6               # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 35:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-type=all    # Send email at begin and end of job
#SBATCH -A PHY23028       # Project/Allocation name (req'd if you have more than 1)
#SBATCH --mail-user=montefalcone@utexas.edu


module load launcher

export OMP_NUM_THREADS=20

export MONTEPYTHON="work/09218/gab97/ls6/fDE_cosmo/montepython_fDE/MontePython.py"
export CHAIN_DIRECTORY=/scratch/09218/gab97/chains
export CHAIN_NAME1=desi_dr2_p18TTTEEE_lensing_w0wa_v1

export PREVIOUS_NSAMPLES=30

export NSAMPLES=300000
export PREVIOUS_CHAIN_FILE1=$(ls ${CHAIN_DIRECTORY}/${CHAIN_NAME1}/*${PREVIOUS_NSAMPLES}__1.txt)

export JUMPING_FACTOR1=2.4

export LAUNCHER_WORKDIR=/work/09218/gab97/ls6/fDE_cosmo/montepython_fDE/mcmc_launch_scripts

export LAUNCHER_JOB_FILE=$LAUNCHER_WORKDIR/mcmc_launcher_1chains_6per

${LAUNCHER_DIR}/paramrun
