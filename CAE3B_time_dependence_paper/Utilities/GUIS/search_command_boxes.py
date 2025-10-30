dummy=root['SETTINGS']['SETUP'].setdefault('last_command_box_search_query','')
def do_search(location=''):
    query=root['SETTINGS']['SETUP']['last_command_box_search_query']
    gui=OMFITaux['GUI']
    foundNone=True
    print(f'***Searching Command boxes for instances of "{query}".')
    for icmd,cmd in enumerate(gui.command):
        if query in cmd.get().lower():
            foundNone=False
            cmdnm=gui.commandNames[icmd]
            print(f'=== Command box "{cmdnm}" === ')
            lns = cmd.get().split('\n')
            ilnmx = len(lns)-1
            ilnsz = np.floor(np.log10(ilnmx)).astype(int)
            for iln,ln in enumerate(lns):
                if query in ln.lower():
                    print(f'{iln+1:{ilnsz}d}: {ln}')
    if foundNone: print(f'No instances of "{query}" found.')

#root['SETTINGS']['SETUP']['last_command_box_search_query']=input('find string in command boxes')
#do_search(location="root['SETTINGS']['SETUP']['last_command_box_search_query']")
OMFITx.Entry("root['SETTINGS']['SETUP']['last_command_box_search_query']",
             lbl='find string in command boxes',postcommand=do_search)
