Output gif/basic.gif
Output webm/basic.webm

Set Shell "zsh"
Set FontSize 18
Set Width 1200
Set Height 800
Set TypingSpeed 60ms
Set Padding 24

Hide
Type `precmd_functions=(); unsetopt prompt_subst; PROMPT="❯ "; RPROMPT=""`
Enter
Wait+Line@10s /❯$/
Type "rm -rf -- ./my/new/project"
Enter
Wait+Line@30s /❯$/
Type "clear"
Enter
Wait+Line@10s /❯$/
Show

Type `uvx python-project-foundry ./my/new/project`
Sleep 500ms
Enter

# uvx may need to download the package before Copier displays its first
# question. Wait for the prompt instead of relying on a fixed delay.
Wait+Screen /Human-readable project name/
Sleep 4s

# Project identity and package shape
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter

# Supported Python versions and coverage target
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter

Wait+Screen /Initialize a Git repository/
Sleep 4s
Ctrl+M
Sleep 4s
Ctrl+M

# Repository and documentation metadata
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter

# Maintainer metadata
Sleep 4s
Enter
Sleep 4s
Enter
Sleep 4s
Enter

# Wait for the shell prompt so long setup output cannot scroll the completion
# message past a screen-scoped match.
Wait+Line@120s /❯$/
Sleep 8s

# Leave the working tree ready for the next recording.
Hide
Type "rm -rf -- ./my/new/project"
Enter
Wait+Line@30s /❯$/
