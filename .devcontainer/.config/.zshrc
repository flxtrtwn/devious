
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="${HOME}/.oh-my-zsh"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source $ZSH/oh-my-zsh.sh
POWERLEVEL10K_MODE=nerdfont-fontconfig
source ~/powerlevel10k/powerlevel10k.zsh-theme
source ~/.p10k.zsh

alias ls="ls -ph --color=auto"
export LS_COLORS="di=34:ln=35:so=32:pi=33:ex=1;40:bd=34;40:cd=34;40:su=0;40:sg=0;40:tw=0;40:ow=0;40:"

if echo hello|grep --color=auto 1 >/dev/null 2>&1; then
    alias grep="grep $GREP_OPTIONS"
    export GREP_COLOR='1;32'
fi

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

export PATH="/${HOME}/.local/bin:$PATH"

source $(poetry env info --path)/bin/activate

alias devious="python -m devious"

eval "$(direnv hook zsh)"
