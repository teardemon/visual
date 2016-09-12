#!/usr/bin/env bash

type ntpdate|| apt-get install ntpdate -y
type ntpdate|| exit

ntpdate time.nist.gov
