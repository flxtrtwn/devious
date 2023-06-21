eval "$(direnv hook zsh)"

export ZSH="${HOME}/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source $ZSH/oh-my-zsh.sh

alias ls="ls -ph --color=auto"
export LS_COLORS="di=34:ln=35:so=32:pi=33:ex=1;40:bd=34;40:cd=34;40:su=0;40:sg=0;40:tw=0;40:ow=0;40:"

if echo hello|grep --color=auto 1 >/dev/null 2>&1; then
    alias grep="grep $GREP_OPTIONS"
    export GREP_COLOR='1;32'
fi

source ~/powerlevel10k/powerlevel10k.zsh-theme

[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

HISTFILE=$USER_HOME/.cache/.zsh_history

pasteinit() {
  OLD_SELF_INSERT=${${(s.:.)widgets[self-insert]}[2,3]}
  zle -N self-insert url-quote-magic
}
pastefinish() {
  zle -N self-insert $OLD_SELF_INSERT
}
zstyle :bracketed-paste-magic paste-init pasteinit
zstyle :bracketed-paste-magic paste-finish pastefinish

if [[ -f "${WORKSPACE_FOLDER}/.devcontainer/.config/.user_aliases" ]]; then
    source "${WORKSPACE_FOLDER}/.devcontainer/.config/.user_aliases"
fi

if [[ -r "${HOME}/.cache/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${HOME}/.cache/p10k-instant-prompt-${(%):-%n}.zsh"
fi
