# tp_templatefit
template fitting tool for heavy jet tags

This tool is based on Sids old fitting code here:
https://github.com/sidnarayanan/PandaAnalysis/tree/master/Tagging/SF

It still relies on his plotting tools:
https://github.com/sidnarayanan/PandaCore

There's two steps:
makeSFTemplates.py produces approprate pass/fail templates for a number of different categories

fitSimultaneousMC.py performs a maximum-likelihood fit to extract effiencies and scale factors.
