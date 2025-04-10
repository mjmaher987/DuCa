#! /bin/bash

CONFIGS=(
# Without skipping
# (f t s)
  "6 2 1"
  "6 4 1"
  "8 2 1"
  "8 4 1"
  "10 4 1"

# With skipping
  "5 4 10"
  "6 4 6"
  "6 4 12"
  "6 5 12"
  "7 3 14"
)

for config in "${CONFIGS[@]}"; do
  echo $config
  IFS=' ' read -r -a params <<< "$config"
  f=${params[0]}
  t=${params[1]}
  s=${params[2]}
  echo "Running with f=$f, t=$t, s=$s"
  CUDA_VISIBLE_DEVICES=7 torchrun --nnodes=1 --nproc_per_node=1 --rdzv_endpoint=localhost:29502 sample_ddp.py --model DiT-XL/2 --num-fid-samples 3000 --per-proc-batch-size 12 --sample-dir samples-single-forward-f$f-t$t-s$s --test-FLOPs -f $f -t $t -s $s &> out-f$f-t$t-s$s.log
done
