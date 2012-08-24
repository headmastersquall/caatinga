#!/usr/bin/env bash

VERSION=`python caat.py --version | cut -d ' ' -f 3`
CAAT_DIR=caatinga-$VERSION

find . -name "__pycache__" -exec rm -rf {} \;
find . -name "*.pyc" -exec rm -rf {} \;

mkdir $CAAT_DIR
cp -r setup.py caatinga docs $CAAT_DIR
cp caat.py $CAAT_DIR/caat
cp lscaat.py $CAAT_DIR/lscaat
cp caatinga.conf.sample $CAAT_DIR

gzip $CAAT_DIR/docs/*
chmod 644 $CAAT_DIR/docs/*
chmod 755 $CAAT_DIR/docs
chmod 644 $CAAT_DIR/caatinga.conf.sample

tar czvf caatinga-$VERSION.tar.gz $CAAT_DIR
rm -rf $CAAT_DIR
