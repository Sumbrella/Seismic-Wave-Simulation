cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py run --conf configs/test.cfg