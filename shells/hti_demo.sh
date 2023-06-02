# simple demo for simulate 2D wave field on homogeneous HTI medium.

cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py run\
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type HTI \
    --rho 2.8 \
    --c11 15.6e6 \
    --c12 6.11e6 \
    --c33 26.4e6 \
    --c55 4.38e6 \
    \
    --source_x_type ricker \
    --source_z_type none \
    --source_x_args 40 \
    --source_z_args 40 \
    \
    --simulate_time 0.2 \
    --simulate_delta_t 2e-4 \
    --save_times 10 \
    \
    --save \
    --x_outfile data/test_x.sfd \
    --z_outfile data/test_z.sfd
