#!/bin/sh
GAME=meka
VERSION=0.80
GAME_LOCALDIR=$HOME/.$GAME
GAME_DATADIR=/usr/share/$GAME
GAME_EXECUTABLE=/usr/libexec/$GAME/$GAME
GAME_DOCDIR=/usr/share/doc/$GAME

mkdir -p $GAME_LOCALDIR
cd $GAME_LOCALDIR

# Create link to game file
ln -sf $GAME_EXECUTABLE $GAME

# Create links to files which are not (usually) modified by users
for file in meka.{blt,dat,msg,nam,pat,thm}; do
	ln -sf $GAME_DATADIR/$file $file
done

# Create links to directory which are not (usually) modified by users
for dir in {Data,Themes}; do
        ln -nsf $GAME_DATADIR/$dir $dir
done

# Remove old link
rm -rf $GAME_LOCALDIR/datafiles

# Copy files which can be modified by users
for file in meka.inp; do
	test -e $file || cp -a $GAME_DATADIR/$file $file
done

# Create links to doc files
for file in {changes.txt,compat.txt,debugger.txt,meka.txt,multi.txt}; do
        ln -sf $GAME_DOCDIR/$file $file
done

exec ./$GAME "$@"

