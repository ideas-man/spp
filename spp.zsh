# /usr/share/spp/spp.zsh

autoload -Uz add-zsh-hook

# Load plugins (aliases + completions)
_spp_plugin_dirs=(/usr/share/spp/plugins ~/.config/spp/plugins ${0:A:h}/plugins)

for plugin in ${(s: :)SPP_PLUGINS}; do
    for dir in $_spp_plugin_dirs; do
        if [[ -d "$dir/$plugin" ]]; then
            [[ -f "$dir/$plugin/aliases.zsh" ]]     && source "$dir/$plugin/aliases.zsh"
            [[ -f "$dir/$plugin/completions.zsh" ]] && source "$dir/$plugin/completions.zsh"
            break
        fi
    done
done

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
