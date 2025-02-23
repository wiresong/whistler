# Whistler: WSL Emacspeak output for NVDA
A quick hack to run emacs in WSL and pipe speech to NVDA. To make this work:

- Rename emacspeak/servers/espeak to something else, and copy the espeak script from this directory into that directory. Make it executable (chmod +x espeak)
- enable the scratchpad directory in NVDA (settings->advanced->enable loading custom code...). Copy whistler.py to scratchpad\globalPlugins. Restart NVDA.
- add "export DTK_PROGRAM=espeak" to whatever file gets sourced when your shell starts (typically .bashrc or .bash_profile, for Bash)

You should now have speech output.
