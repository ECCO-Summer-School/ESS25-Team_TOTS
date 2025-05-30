#PBS -W group_list=s2907
#PBS -S /bin/csh
#PBS -q debug
#PBS -l select=3:ncpus=40:model=sky_ele
#PBS -l walltime=1:00:00
#PBS -j oe
#PBS -o ./
#PBS -m bea

limit stacksize unlimited
module purge
module load comp-intel/2020.4.304
module load mpi-hpe/mpt
module load hdf4/4.2.12
module load hdf5/1.8.18_mpt
module load netcdf/4.4.1.1_mpt
module load python3/3.9.12
module list

setenv FORT_BUFFERED 1
setenv MPI_BUFS_PER_PROC 128
setenv MPI_DISPLAY_SETTINGS
setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${HOME}/lib
unsetenv MPI_IB_RECV_MSGS
unsetenv MPI_UD_RECV_MSGS

set nprocs  = 113
set basedir = ./
set inputdir = /nobackup/owang/runs/V4r5/PO.DAAC/ancillary_data/ancillary_data_orig/

if ( -d ${basedir}/run) then
 echo 'Directory "run" exists.'
 echo 'Please rename/remove it and re-submit the job.'
 exit 1
endif

mkdir ${basedir}/run
cd ${basedir}/run

cp -r ../namelist/* .
ln -s ${inputdir}/input_init/* .
ln -s ${inputdir}/misc/tools/mkdir_subdir_diags.py .
ln -s ${inputdir}/data_constraints/data_error/*/* .
ln -s ${inputdir}/data_constraints/*/* .
ln -s ${inputdir}/input_forcing/adjusted/eccov4r5* .
ln -s ${inputdir}/input_forcing/other/*.bin .
ln -s ${inputdir}/input_forcing/control_weights/* .
ln -s ${inputdir}/native_grid_files/tile*.mitgrid .

python mkdir_subdir_diags.py
cp -p ../build/mitgcmuv .
mpiexec -np ${nprocs} /u/scicon/tools/bin/mbind.x ./mitgcmuv
