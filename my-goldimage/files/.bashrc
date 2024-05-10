alias ls='ls -Fhstr --color=auto --group-directories-first'
alias ll='ls -Al'

complete -A directory cd
complete -D -A file

export TMOUT=300
