#
# ~/.bashrc
#

source /usr/share/doc/pkgfile/command-not-found.bash

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias ls="ls --color"
alias +="git add"
alias ?="git status"
alias commit="git commit -am"
alias push="git push"
alias pull="git pull"
alias clone="git clone"
alias sup="python2 ~/.custom/update.py"

function code { cd $HOME/Dropbox/code/$@; }
function db { cd $HOME/Dropbox/$@; }
function cd { builtin cd "$@" && ls; }
function aur { python2 $HOME/.custom/aur.py "$@"; }
function comp { commit "$@" && push; }
function sysup { sudo pacman -Syu; 
				 aur -u; 
				 sudo pkgfile -u;
				 sup; }
function lscmds
{
    echo -n $PATH | xargs -d : -I {} find {} -maxdepth 1 \
        -executable -type f -printf '%P\n' | sort -u
}


# If not running interactively, don't do anything
[[ $- != *i* ]] && return

#alias ls='ls --color=auto'
#PS1='[\u@\h \W]\$ '

[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion

default_username='tsx525'
default_hostname='525'

if [[ $COLORTERM = gnome-* && $TERM = xterm ]] && infocmp gnome-256color >/dev/null 2>&1; then
	export TERM=gnome-256color
elif infocmp xterm-256color >/dev/null 2>&1; then
	export TERM=xterm-256color
fi

if tput setaf 1 &> /dev/null; then
	tput sgr0
	if [[ $(tput colors) -ge 256 ]] 2>/dev/null; then
		MAGENTA=$(tput setaf 5)
		ORANGE=$(tput setaf 172)
		GREEN=$(tput setaf 4)
		PURPLE=$(tput setaf 141)
		WHITE=$(tput setaf 252)
	else
		MAGENTA=$(tput setaf 5)
		ORANGE=$(tput setaf 4)
		GREEN=$(tput setaf 2)
		PURPLE=$(tput setaf 1)
		WHITE=$(tput setaf 7)
	fi
	BOLD=$(tput bold)
	RESET=$(tput sgr0)
else
	MAGENTA="\033[1;31m"
	ORANGE="\033[1;33m"
	GREEN="\033[1;32m"
	PURPLE="\033[1;35m"
	WHITE="\033[1;37m"
	BOLD=""
	RESET="\033[m"
fi

# Fastest possible way to check if repo is dirty. a savior for the WebKit repo.
function parse_git_dirty() {
   git diff --quiet --ignore-submodules HEAD 2>/dev/null; [ $? -eq 1 ] && echo '*'
}

function parse_git_branch() {
	git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/\1$(parse_git_dirty)/"
}

# Only show username/host if not default
function usernamehost() {
	if [ $USER != $default_username ]; then echo "${MAGENTA}$USER${WHITE}|"; fi
	if [ $HOSTNAME != $default_hostname ]; then echo "${ORANGE}$HOSTNAME$WHITE:"; fi
}

# iTerm Tab and Title Customization and prompt customization
# http://sage.ucsc.edu/xtal/iterm_tab_customization.html

# Put the string " [bash]   hostname::/full/directory/path"
# in the title bar using the command sequence
# \[\e]2;[bash]   \h::\]$PWD\[\a\]

# Put the penultimate and current directory
# in the iterm tab
# \[\e]1;\]$(basename $(dirname $PWD))/\W\[\a\]

PS1="\[\e]2;$PWD\[\a\]\[\e]1;\]$(basename "$(dirname "$PWD")")/\W\[\a\]${BOLD}\$(usernamehost)\[$GREEN\]\w\[$WHITE\]\$([[ -n \$(git branch 2> /dev/null) ]] && echo \" - \")\[$PURPLE\]\$(parse_git_branch)\[$WHITE\]\n\$ \[\033[0;37m\]"
