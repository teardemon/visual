#!/usr/bin/env bash

type ntpdate|| apt-get install ntpdate
type ntpdate|| exit

ntpdate time.nist.gov
