# simple demo for simulate 2D wave field on homogeneous isotropic medium.

cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py \
    run \
    --run_with_show \
    --show_times 10 \
    --simulate_time 0.2 \
    --simulate_delta_t 2e-4 \
    \
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type I \
    --c11 24300000 \
    --c12 6075000 \
    \
    --source_x 300 \
    --source_z 300 \
    --source_x_type ricker \
    --source_x_args 40 \
    --source_z_type ricker \
    --source_z_args 40 \
    \
    --x_outfile data/test_x.sfd \
    --z_outfile data/test_z.sfd \
