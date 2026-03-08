# /usr/share/spp/spp.zsh

autoload -Uz add-zsh-hook

_spp_preexec() {
    export SECONDS_START=$SECONDS
}

add-zsh-hook preexec _spp_preexec

_spp_precmd() {
    local exit_status=$?
    local spp_args=()
    [[ -n "$SPP_EXPR" ]] && spp_args+=(-e "$SPP_EXPR")
    PROMPT=$(COLUMNS=$COLUMNS SECONDS=$SECONDS EXIT_STATUS=$exit_status spp --zsh "${spp_args[@]}")
}

add-zsh-hook precmd _spp_precmd
