#!/bin/bash

rcssserver  server::game_log_dir='~/tmp/' server::text_log_dir='~/tmp/' > server-log.txt &
~/pp/2d/helios-base/build/bin/start.sh -t t1
~/pp/2d/helios-base/build/bin/start.sh -t t2