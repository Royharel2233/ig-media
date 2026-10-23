#!/bin/bash
cd /home/sandbox/reel
while true; do
  have=$(ls frames_fuel_hd 2>/dev/null | sed -n 's/^f_\([0-9]*\)\.jpg$/\1/p' | sort)
  n=$(echo "$have" | grep -c .)
  if [ "$n" -ge 915 ]; then echo "ALL_DONE n=$n"; break; fi
  missing=$(comm -23 <(seq 0 914 | awk '{printf "%05d\n",$1}') <(echo "$have") | head -15 | sed 's/^0*\([0-9]\)/\1/' | tr '\n' ',' | sed 's/,$//')
  echo "BATCH $(date +%H:%M:%S) have=$n: $missing"
  timeout -k 5 75 node capture_fuel.js 720 1280 frames_fuel_hd list "$missing" >> render_batch.log 2>&1
  pkill -9 -f puppeteer_dev_chrome_profile 2>/dev/null
  sleep 1
done
echo "BATCH_RENDER_COMPLETE"
