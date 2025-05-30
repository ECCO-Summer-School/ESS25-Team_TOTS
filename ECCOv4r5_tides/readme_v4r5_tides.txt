Instructions on how to reproduce ECCO Version 4 Release 5 (V4r5) with tides enabled and using total atmospheric forcing (first guess plus plus control adjustment)

1. Get the code 
mkdir WORKINGDIR
cd WORKINGDIR

git clone https://github.com/MITgcm/MITgcm.git -b checkpoint68g

cd MITgcm
mkdir -p ECCOV4/release5
cd ECCOV4/release5
# Clone the repo
git clone https://github.com/ECCO-Summer-School/ESS25-Team_TOTS.git
# Move the 'tides' folder into the desired location and rename it
mv ESS25-Team_TOTS/tides/ ../../pkg/.
# Move only the folder you want to keep into current directory
mv ESS25-Team_TOTS/ECCOv4r5_tides .
# Remove the rest of the cloned repo
rm -rf ESS25-Team_TOTS
cd ECCOv4r5_tides/

2. Compile
module purge
module load comp-intel/2020.4.304
module load mpi-hpe/mpt
module load hdf4/4.2.12

module load hdf5/1.8.18_mpt
module load netcdf/4.4.1.1_mpt
module list

mkdir build
cd build
../../../../tools/genmake2 -mods=../code -optfile=../code/linux_amd64_ifort+mpi_ice_nas -mpi
make depend
make all
cd ..

3. Run
qsub run_script.csh

