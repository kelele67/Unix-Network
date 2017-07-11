#!/bin/bash

# Require gcc 4.7+

SRCS="Acceptor.cc InetAddress.cc TcpStream.cc Socket.cc"

set -x
CC=${CC:-g++}

$CC -std=c++11 -Wall -Wextra -g -O2 $SRCS ttcp.cc -o ttcp /usr/lib -lboost_program_options