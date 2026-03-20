# ECCO Version 4 Release 5 (V4r5) with tides and self-attraction and loading based on:
# https://github.com/MITgcm-contrib/llc_hires/blob/master/llc_90/ecco_v4r5/readme_v4r5_68y.txt

# 1. These instructions are specific to NASA Ames athena
  ssh athfe01
  WORKDIR=/nobackup/$USER/WORKINGDIR

# 2. Get code
  mkdir $WORKDIR
  cd $WORKDIR
  git clone --depth 1 -b checkpoint68y https://github.com/MITgcm/MITgcm.git
  git clone https://github.com/ECCO-Summer-School/ESS25-Team_TOTS.git
  cd $WORKDIR/MITgcm/pkg
  ln -sf ../../ESS25-Team_TOTS/sal .
  ln -sf ../../ESS25-Team_TOTS/tides .

# 3. Build executable
  mkdir $WORKDIR/MITgcm/build
  cd $WORKDIR/MITgcm/build
  source /opt/cray/pe/modules/3.2.11.7/init/bash
  module swap PrgEnv-cray PrgEnv-intel
  module use /u/ojahn/software/modulefiles
  module load jahn/shtns/3.4.5_intel-2023.2.1_cray-fftw
  MOD=$WORKDIR/ESS25-Team_TOTS/ECCOv4r5_tides_sal
  ../tools/genmake2 -mpi -mods $MOD/code \
   -of $MOD/code/linux_amd64_ifort+mpi_cray_nas_shtns
  make depend
  make -j

# 4. Run simulation (1992-2019 period)
  mkdir $WORKDIR/MITgcm/run
  cd $WORKDIR/MITgcm/run
  mkdir -p diags
  ln -sf ../build/mitgcmuv .
  INPUTDIR='/nobackup/hzhang1/pub/Release5'
  ln -s $INPUTDIR/input_bin/* .
  ln -s $INPUTDIR/TBADJ .
  cp -r $MOD/input/* .
  qsub job_v4r5
