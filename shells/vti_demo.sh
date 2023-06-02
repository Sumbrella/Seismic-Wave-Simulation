# simple demo for simulate 2D wave field on homogeneous VTI medium.

cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py run\
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type VTI \
    --rho 2.17 \
    --c_matrix 26.4e6 6.11e6 15.6e6 4.36e6\
    --source_x_args 40 \
    --source_z_args 40 \
    --simulate_time 0.2 \
    --simulate_delta_t 2e-4 \
    --save_times 10 \
    --source_x_type none \
    --source_z_type ricker \
    --save \
    --x_outfile data/test_x.sfd \
    --z_outfile data/test_z.sfd \
    --run_with_show
