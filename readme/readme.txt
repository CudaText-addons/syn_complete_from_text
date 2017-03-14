Plugin for SynWrite.
handles auto-complete command (Ctrl+Space). gives completion listbox with list 
of words from current file, which start with the current word (before caret). 
eg, if you typed "ri", it may give "riddle", "rigther" etc.

plugin has options: 
- minimal word len (words of smaller len won't show in list)
- lexers list (for which to work), none-lexer specified as "-"
- case-sensitive

to edit options, open plugin's source (by Addon Manager) and options are 
at the top of __init__.py.

for plugin to work, turn off SynWrite's option "Auto-complete - Auto show words from current file" 
(plugin does same and better).


Author: Alexey (SynWrite)
License: MIT
