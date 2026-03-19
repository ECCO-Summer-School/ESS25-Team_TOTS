Instructions on how to reproduce ECCO Version 4 Release 5 (V4r5) with tides
and self-attraction and loading enabled and using total atmospheric forcing
(first guess plus control adjustment).

0. These instructions are specific to NASA Ames athena
ssh athfe01
WORKDIR=/nobackup/$USER/WORKINGDIR

1. Get the code 
mkdir $WORKDIR
cd $WORKDIR
git clone https://github.com/MITgcm/MITgcm.git -b checkpoint68g
git clone https://github.com/ECCO-Summer-School/ESS25-Team_TOTS.git
cd $WORKDIR/MITgcm/pkg
ln -sf ../../ESS25-Team_TOTS/sal .
ln -sf ../../ESS25-Team_TOTS/tides .

2. Compile
source /opt/cray/pe/modules/3.2.11.7/init/bash
module swap PrgEnv-cray PrgEnv-intel
module use /u/ojahn/software/modulefiles
module load jahn/shtns/3.4.5_intel-2023.2.1_cray-fftw
mkdir $WORKDIR/MITgcm/build
cd $WORKDIR/MITgcm/build
MOD=$WORKDIR/ESS25-Team_TOTS/ECCOv4r5_tides
../tools/genmake2 -mpi -mods "$MOD/code_sal $MOD/code" \
  -of $MOD/code_sal/linux_amd64_ifort+mpi_cray_nas_shtns
make depend
make -j

3. Run
qsub run_script.csh
