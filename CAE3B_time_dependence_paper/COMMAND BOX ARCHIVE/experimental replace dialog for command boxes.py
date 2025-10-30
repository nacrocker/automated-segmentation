def replace(self):
    import utils_tk
    from idlelib import replace as rplc
    from idlelib.replace import ReplaceDialog
    from idlelib.search import SearchDialog
    self.tag_add(tk.SEL, "1.0", tk.END)
    from idlelib import searchengine
    engine = searchengine.get(self._root())
    if not hasattr(engine, "_replacedialog"):
        try:
            rplc.StringVar = utils_tk._orig_tkStringVar
            engine._replacedialog = ReplaceDialog(self._root(), engine)
        except Exception as exc:
            print(exc)
        finally:
            rplc.StringVar = utils_tk._tkStringVar
    s = engine._replacedialog
    try:
        s.open(self)
        s.top.grab_release()
    except tk.TclError:
        pass
    s.top.wm_transient(self._root())
    self.tag_remove(tk.SEL, "1.0", tk.END)
    return 'break'

tk.ScrolledText.replace=replace

def _patch_active_command_window_with_replace():
    self=OMFITaux['GUI'].command[OMFITaux['GUI'].commandActive]
    self.bind(f'<{ctrlCmd()}-r>', lambda event=None: self.replace())

def _patch_ScrolledText_class_init():
    cls=tk.ScrolledText
    def _init_modified(self,*args,**kw):
        self._init_orig(*args,**kw)
        self.bind(f'<{ctrlCmd()}-r>', lambda event=None: self.replace())

    cls._init_modified = _init_modified
    if not hasattr(cls,"_init_orig"): cls._init_orig = cls.__init__
    cls.__init__=cls._init_modified

_patch_active_command_window_with_replace()
_patch_ScrolledText_class_init()
#OMFITaux['GUI'].command[OMFITaux['GUI'].commandActive].bind(f'<{ctrlCmd()}-r>', lambda event=None: self.replace())
#OMFITaux['GUI'].command[OMFITaux['GUI'].commandActive].replace()
