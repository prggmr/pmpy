#!/bin/bash
#
# Open new Terminal tabs from the command line
#
# Original Author: Justin Hileman (http://justinhileman.com)
# 
# This has been modified to allow it to run as a single bash script.
#
# Usage:
#     iterm.bash                   Opens the current directory in a new tab
#     iterm.bash [PATH]            Open PATH in a new tab
#     iterm.bash [CMD]             Open a new tab and execute CMD
#     iterm.bash [PATH] [CMD] ...  You can prob'ly guess

# Only for teh Mac users
[ `uname -s` != "Darwin" ] && return

osascript &>/dev/null <<EOF
    tell application "iTerm"
        tell current terminal
            launch session "Default Session"
            tell the last session
                write contents of file "$1"
                return
            end tell
        end tell
    end tell
EOF