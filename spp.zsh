# /usr/share/spp/spp.zsh

# autoload -Uz add-zsh-hook

_spp_preexec() {
    export SECONDS_START=$SECONDS
}

add-zsh-hook preexec _spp_preexec

_spp_precmd() {
    PROMPT=$(SECONDS=$SECONDS EXIT_STATUS=$? spp)
}

add-zsh-hook precmd _spp_precmd
