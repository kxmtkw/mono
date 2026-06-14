#!/bin/bash
case $1 in
set) brightnessctl set $2 ;; inc) brightnessctl set +$2 ;; dec) brightnessctl set $2- ;; save) brightnessctl save ;; restore) brightnessctl restore ;;
esac
