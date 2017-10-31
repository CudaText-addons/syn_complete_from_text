Plugin for SynWrite.
handles auto-complete command (Ctrl+Space). gives completion listbox with list 
of words from current file, which start with the current word (before caret). 
eg, if you typed "ri", it may give "riddle", "rigther" etc.

plugin has options: 
- minimal word len (words of smaller len won't show in list)
- lexers list for which to work, none-lexer specified as "-"
- case sensitive
- get words from all editor-tabs
- get words from autocompletion *.acp file for current lexer

to edit options ini-file, use menu item "Plugins - Complete From Text - Config". 


Authors:
  Alexey T (SynWrite)
  iRamSoft http://github.com/iRamSoft
License: MIT
